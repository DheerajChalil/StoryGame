from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import FluxPipeline
import torch
import io
import base64

app = FastAPI()

# Load model only once at startup
@app.on_event("startup")
def load_model():
    global pipe
    pipe = FluxPipeline.from_pretrained(
        "/home/dheeraj/flux1schnell",
        torch_dtype=torch.bfloat16
    )
    # pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power
    pipe.enable_sequential_cpu_offload() # offloads modules to CPU on a submodule level (rather than model level)

class PromptRequest(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    image_base64: str

@app.post("/generate/")
def generate_image(req: PromptRequest):
    try:
        image = pipe(
            req.prompt,
            guidance_scale=0.0,
            output_type="pil",
            num_inference_steps=4,
            max_sequence_length=256,
            generator=torch.Generator("cpu").manual_seed(0)
        ).images[0]

        # Convert image to base64 string for API response
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {"image_base64": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

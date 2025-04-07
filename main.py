from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import FluxPipeline
import torch
import io
import base64
from diffusers import DiffusionPipeline

app = FastAPI()

# Load model only once at startup
@app.on_event("startup")
def load_model():
    global pipe
    pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev")

class PromptRequest(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    image_base64: str

@app.post("/generate/")
def generate_image(req: PromptRequest):
    try:
        image = pipe(req.prompt).images[0]

        # Convert image to base64 string for API response
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {"image_base64": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

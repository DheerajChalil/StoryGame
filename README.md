# StoryGame

### 📦 Components:

1. **FastAPI** — Lightweight async web framework.
2. **Diffusers** — HuggingFace library for generative pipelines (e.g., Stable Diffusion, FluxPipeline).
3. **PyTorch (CPU)** — Neural network framework running inference on CPU.
4. **Docker** — For containerized deployment of the API.
5. **Base64** — Encoding the generated image for easy transmission in API responses.

---

## 🔄 Flow Description

1. **App Starts**  
   - On startup, the model (`FluxPipeline`) is loaded from a local path.
   - It uses `torch_dtype=torch.bfloat16` for lighter memory usage.
   - `pipe.enable_model_cpu_offload()` and `pipe.enable_sequential_cpu_offload()` are used to manage memory on CPU.

2. **Image Generation** (`POST /generate/`)  
   - Accepts a JSON payload with a `prompt`.
   - Passes the prompt into the Diffusers pipeline.
   - Runs with:
     - `guidance_scale=0.0`
     - `num_inference_steps=4`
     - `max_sequence_length=256`
     - `torch.Generator("cpu").manual_seed(0)`
   - Converts the resulting image into base64.
   - Returns it in the response.

---

## 🔌 API Endpoint

### `POST /generate/`

**Request Body:**

```json
{
  "prompt": "a serene lake surrounded by mountains"
}
To enable GPU acceleration (if a compatible GPU is available on the host system), make the following changes: 1. Dockerfile: - Use a PyTorch base image with CUDA support. - Ensure system libraries for CUDA (like `nvidia-cuda-toolkit`) are included if needed. 2. docker-compose.yml: - Add `runtime: nvidia` under the service. - Optionally include device requests to access GPU resources. - Ensure NVIDIA Container Toolkit is installed and configured. 3. main.py: - Replace `"cpu"` with `"cuda"` where torch device is set. - Remove or conditionally apply `enable_model_cpu_offload()` and similar CPU-specific logic. - Optionally call `pipe.to("cuda")` if required. 4. requirements.txt: - Make sure `torch` has GPU (CUDA) support. You may not need changes if using a CUDA-based Docker image. 5. Host System: - Must have NVIDIA drivers and Docker with GPU access. - Make sure the user running Docker has permission to access the GPU. 6. Rebuild: - Run `docker-compose build` again to rebuild the image with GPU support.

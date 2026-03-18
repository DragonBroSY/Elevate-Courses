# RTX 4070 - GPU Projects

## Hardware
- **GPU:** NVIDIA GeForce RTX 4070
- **VRAM:** 12GB

## Local LLM for Discord Bot

### What's Possible with 12GB VRAM
| Model Size | Quantization | Quality | Notes |
|------------|-------------|---------|-------|
| 7B–8B | Q8 | Excellent | Llama 3.1 8B, Mistral 7B — full quality |
| 13B | Q4/Q5 | Great | Good balance of size vs quality |
| 30B+ | Q2/Q3 | Degraded | Not recommended |

### Recommended Models
- **Llama 3.1 8B** — best all-round chat model
- **Mistral 7B / Nemo 12B** — fast, good instruction following
- **Qwen 2.5 7B** — strong multilingual support

### Stack
1. **Ollama** — run local model, exposes API at `localhost:11434`
2. **Discord bot** (discord.py or discord.js) — relay messages to Ollama API
3. Repo already started: [[discord-claude-bot]]

### Setup Steps
- [ ] Install Ollama → `ollama pull llama3.1:8b`
- [ ] Test: `ollama run llama3.1:8b`
- [ ] Wire Discord bot to hit `http://localhost:11434/api/chat`

---

## Other RTX 4070 Use Cases

### AI / Creative
- **Stable Diffusion** — already have ComfyUI installed (`~/ComfyUI`)
- **Whisper** — local speech-to-text (OpenAI Whisper via faster-whisper)
- **RVC / voice cloning** — voice synthesis for content

### Streaming / Video
- **OBS NVENC encoding** — offload stream encoding from CPU
- **DaVinci Resolve** — GPU-accelerated video rendering
- **Topaz Video AI** — AI upscaling and denoising

### ML / Development
- **PyTorch + CUDA** — train or fine-tune small models
- **ComfyUI workflows** — already installed, use for automation pipelines

---

## Related
- [[Projects/3D Tours]]
- [[Sessions/]]

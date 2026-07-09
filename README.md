### 📄 `README.md`

```markdown
# 🤖 vLLM Dual-Model Deployment Project

A production-ready setup for running **both Standard (HuggingFace) and GGUF (Quantized) Qwen2.5 models** simultaneously using vLLM, Docker, and persistent Docker volumes.

Deployed locally on a 4GB GPU (one at a time) or on Lightning AI cloud (both simultaneously).

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Architecture](#-architecture)
3. [Prerequisites](#-prerequisites)
4. [Project Structure](#-project-structure)
5. [Quick Start](#-quick-start)
6. [Detailed Setup](#-detailed-setup)
7. [Running the Models](#-running-the-models)
8. [Testing the API](#-testing-the-api)
9. [Lightning AI Cloud Deployment](#-lightning-ai-cloud-deployment)
10. [Troubleshooting](#-troubleshooting)
11. [Cleanup](#-cleanup)

---

## 🎯 Overview

This project provides:
- ✅ **Dual model support**: Run both Standard (`.safetensors`) and GGUF (`.gguf`) models
- ✅ **Persistent storage**: Models stored in Docker volumes (not lost on container restart)
- ✅ **Single Docker image**: One image serves both model formats
- ✅ **OpenAI-compatible API**: Drop-in replacement for OpenAI SDK
- ✅ **Streaming support**: Real-time token-by-token generation
- ✅ **Cloud-ready**: Deploy on Lightning AI with 16GB+ GPU

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Volume: qwen_models               │
│  ┌──────────────────────────┐  ┌──────────────────────────┐ │
│  │ Qwen2.5-0.5B-Instruct/   │  │ Qwen2.5-0.5B-Instruct-  │ │
│  │ (Standard .safetensors)  │  │ GGUF/ (.gguf file)       │ │
│  └──────────────────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
           │                              │
           ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│ qwen-vllm-standard  │      │ qwen-vllm-gguf      │
│ Port: 8000          │      │ Port: 8001          │
│ Model: qwen-standard│      │ Model: qwen-gguf    │
└─────────────────────┘      └─────────────────────┘
           │                              │
           └──────────┬───────────────────┘
                      ▼
              OpenAI-Compatible API
```

---

## 📦 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Docker Desktop** | Latest | Run containers |
| **Docker Compose** | v2.0+ | Orchestrate services |
| **NVIDIA GPU** | 4GB+ VRAM | Run models |
| **NVIDIA Drivers** | Latest | GPU passthrough |
| **Python** | 3.10+ | Download scripts |
| **Git** | Latest | Version control |

### Verify Installation
```powershell
docker --version
docker compose version
nvidia-smi
python --version
git --version
```

---

## 📁 Project Structure

```
vllm_project/
│
├── docker-compose.yml          # Service orchestration (both models)
├── Dockerfile                  # Single image with vLLM + GGUF plugin
├── README.md                   # This file
│
├── scripts/
│   ├── download_model.py       # Downloads both models from HuggingFace
│   ├── test_standard.py        # Test script using 'openai' library
│   └── test_requests.py        # Test script using 'requests' library
│
├── models/                     # Local cache (before copying to volume)
│   ├── Qwen2.5-0.5B-Instruct/
│   └── Qwen2.5-0.5B-Instruct-GGUF/
│
└── requirements-base.txt       # Python dependencies
```

---

## 🚀 Quick Start

For users who want to get running immediately:

```powershell
# 1. Clone the repository
git clone https://github.com/SuriyaPrakash1928/vllm_project.git
cd vllm_project

# 2. Create Docker volume
docker volume create qwen_models

# 3. Download models
pip install -r requirements-base.txt
python scripts/download_model.py

# 4. Copy models to volume
docker run -d --name temp-cp -v qwen_models:/models alpine tail -f /dev/null
docker cp models/Qwen2.5-0.5B-Instruct/. temp-cp:/models/Qwen2.5-0.5B-Instruct/
docker cp models/Qwen2.5-0.5B-Instruct-GGUF/. temp-cp:/models/Qwen2.5-0.5B-Instruct-GGUF/
docker stop temp-cp; docker rm temp-cp

# 5. Build and run (Local 4GB GPU - one at a time)
docker compose build
docker compose --profile standard up   # OR: docker compose --profile gguf up
```

---

## 🔧 Detailed Setup

### Step 1: Create Docker Volume

Docker volumes persist data even when containers are removed.

```powershell
docker volume create qwen_models
```

**Verify:**
```powershell
docker volume ls
```

---

### Step 2: Download Models Locally

```powershell
pip install -r requirements-base.txt
python scripts/download_model.py
```

This downloads:
- **Standard Model**: `Qwen/Qwen2.5-0.5B-Instruct` (~1GB)
- **GGUF Model**: `bartowski/Qwen2.5-0.5B-Instruct-GGUF` (~380MB)

---

### Step 3: Copy Models to Docker Volume

We use a temporary Alpine container to transfer files from your host to the volume.

```powershell
# Start temporary container with volume mounted
docker run -d --name temp-cp -v qwen_models:/models alpine tail -f /dev/null

# Copy Standard model
docker cp models/Qwen2.5-0.5B-Instruct/. temp-cp:/models/Qwen2.5-0.5B-Instruct/

# Copy GGUF model
docker cp models/Qwen2.5-0.5B-Instruct-GGUF/. temp-cp:/models/Qwen2.5-0.5B-Instruct-GGUF/

# Clean up
docker stop temp-cp; docker rm temp-cp
```

**Verify contents:**
```powershell
docker run --rm -v qwen_models:/models alpine ls -la /models
```

---

### Step 4: Build the Docker Image

```powershell
docker compose build
```

This creates a single image `qwen-llm-image:latest` with:
- vLLM OpenAI server
- GGUF plugin for quantized model support

---

## ▶️ Running the Models

### Option A: Local 4GB GPU (Run One at a Time)

Due to VRAM limitations, run only one model at a time.

**Start Standard Model:**
```powershell
docker compose --profile standard up
```

**Start GGUF Model:**
```powershell
docker compose --profile gguf up
```

**Switch Models:**
```powershell
# Stop current (Ctrl+C), then start the other
docker compose --profile gguf up
```

---

### Option B: Cloud 16GB+ GPU (Run Both Simultaneously)

On Lightning AI or any machine with 16GB+ VRAM, run both models at once:

```powershell
docker compose up
```

Both services will start on different ports:
- **Standard**: `http://localhost:8000`
- **GGUF**: `http://localhost:8001`

---

### Run in Background (Detached Mode)

```powershell
docker compose up -d
```

**View logs:**
```powershell
docker logs -f qwen_vllm_standard
docker logs -f qwen_vllm_gguf
```

---

## 🧪 Testing the API

### Method 1: Using cURL (Windows PowerShell)

**List Available Models:**
```powershell
curl http://localhost:8000/v1/models
```

**Standard Model Request:**
```powershell
curl -X POST http://localhost:8000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{"model":"qwen-standard","messages":[{"role":"user","content":"Hello!"}],"max_tokens":100}'
```

**GGUF Model Request:**
```powershell
curl -X POST http://localhost:8001/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{"model":"qwen-gguf","messages":[{"role":"user","content":"Hello!"}],"max_tokens":100}'
```

**Streaming Response:**
```powershell
curl -N -X POST http://localhost:8000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{"model":"qwen-standard","messages":[{"role":"user","content":"Tell a joke"}],"max_tokens":200,"stream":true}'
```

---

### Method 2: Using Python (`openai` library)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="empty"
)

response = client.chat.completions.create(
    model="qwen-standard",  # or "qwen-gguf"
    messages=[{"role": "user", "content": "Explain Docker"}],
    max_tokens=500,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

### Method 3: Using Python (`requests` library)

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "qwen-standard",
        "messages": [{"role": "user", "content": "Explain Docker"}],
        "max_tokens": 500
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

---

### Method 4: Using Postman

1. Create a **POST** request to `http://localhost:8000/v1/chat/completions`
2. Set header: `Content-Type: application/json`
3. Body (raw JSON):
```json
{
  "model": "qwen-standard",
  "messages": [
    {"role": "user", "content": "Write a poem about AI"}
  ],
  "max_tokens": 500,
  "stream": false
}
```

---

## ☁️ Lightning AI Cloud Deployment

### Step 1: Create Studio
1. Go to [lightning.ai](https://lightning.ai)
2. Create a new Studio
3. Select **NVIDIA T4 (16GB)** or **A10G (24GB)** GPU

### Step 2: Deploy in Cloud Terminal

```bash
# Clone repository
git clone https://github.com/SuriyaPrakash1928/vllm_project.git
cd vllm_project

# Setup volume and download models
docker volume create qwen_models
pip install -r requirements-base.txt
python scripts/download_model.py

# Copy to volume
docker run -d --name temp-cp -v qwen_models:/models alpine tail -f /dev/null
docker cp models/Qwen2.5-0.5B-Instruct/. temp-cp:/models/Qwen2.5-0.5B-Instruct/
docker cp models/Qwen2.5-0.5B-Instruct-GGUF/. temp-cp:/models/Qwen2.5-0.5B-Instruct-GGUF/
docker stop temp-cp && docker rm temp-cp

# Build and run both models
docker compose build
docker compose up
```

### Step 3: Get Public URLs
1. Click **"Ports"** or **"Endpoints"** in the Studio UI
2. Copy the URLs for ports 8000 and 8001
3. Example: `https://8000-xxxxx.lightning.space`

### Step 4: Test from Local Machine

```powershell
curl -X POST https://8000-xxxxx.lightning.space/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{"model":"qwen-standard","messages":[{"role":"user","content":"Hello from cloud!"}]}'
```

---

## 🐛 Troubleshooting

### Issue: "Temporary failure in name resolution"
**Cause**: Docker DNS glitch

**Fix**:
```powershell
# Windows PowerShell
ipconfig /flushdns
wsl --shutdown
# Restart Docker Desktop
```

---

### Issue: "No available memory for cache blocks"
**Cause**: GPU VRAM exceeded

**Fix**:
- Local (4GB): Run only one model at a time using `--profile`
- Cloud (16GB+): Lower `gpu_memory_utilization` to `0.40`

---

### Issue: "GGUF magic invalid"
**Cause**: Incomplete model download

**Fix**:
```powershell
# Delete and re-download
Remove-Item -Recurse -Force models\Qwen2.5-0.5B-Instruct-GGUF
python scripts/download_model.py
```

---

### Issue: "Exec format error" (Docker Desktop)
**Cause**: Corrupted WSL integration

**Fix**:
```powershell
wsl --shutdown
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
# Restart Docker Desktop
```

---

### Issue: Port 8000 already in use
**Fix**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill the process
taskkill /PID <PID> /F
```

---

## 🧹 Cleanup

### Stop Services
```powershell
docker compose down
```

### Remove Specific Container
```powershell
docker stop qwen_vllm_standard; docker rm qwen_vllm_standard
docker stop qwen_vllm_gguf; docker rm qwen_vllm_gguf
```

### Delete Docker Volume (Removes all models!)
```powershell
docker volume rm qwen_models
```

### Remove Docker Image
```powershell
docker rmi qwen-llm-image:latest
```

### Complete Reset
```powershell
docker compose down
docker volume rm qwen_models
docker rmi qwen-llm-image:latest
docker builder prune -a
```

---

## 📊 GPU Memory Reference

| GPU | VRAM | Configuration |
|-----|------|---------------|
| **NVIDIA T500** | 4GB | Run one model at a time (`--profile`) |
| **NVIDIA T4** | 16GB | Run both simultaneously (`gpu_memory_utilization=0.40`) |
| **NVIDIA A10G** | 24GB | Run both with high utilization (`gpu_memory_utilization=0.75`) |

---

## 🔗 Useful Links

- [vLLM Documentation](https://docs.vllm.ai/)
- [Qwen2.5 Model](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [GGUF Plugin](https://github.com/vllm-project/vllm-gguf-plugin)
- [Lightning AI](https://lightning.ai)
- [Docker Documentation](https://docs.docker.com/)

---

## 📝 License

This project is for educational purposes. Model weights are licensed under their respective licenses (Qwen: Apache 2.0).

---

## 🙏 Acknowledgments

- **vLLM Team** - For the high-performance inference engine
- **Qwen Team** - For the excellent open-source models
- **Lightning AI** - For cloud GPU access
- **HuggingFace** - For model hosting

---

**Built with ❤️ using vLLM, Docker, and Qwen**
```

---

### 📖 How to Use This README

1. **Save the file**: Replace your existing `README.md` with the content above
2. **Commit to GitHub**:
   ```powershell
   git add README.md
   git commit -m "Update README with complete documentation"
   git push origin main
   ```
3. **View on GitHub**: Your README will render beautifully on your repository's main page

This README provides everything a developer needs to understand, deploy, test, and troubleshoot your vLLM dual-model project from scratch! 🚀

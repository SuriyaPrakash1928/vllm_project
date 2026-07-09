# vLLM Local Project

A complete local setup for running vLLM with both standard HuggingFace models and GGUF models using Docker Compose.

## 📁 Folder Structure
- `docker-compose.yaml` - Standard HuggingFace model server
- `docker-compose.gguf.yaml` - GGUF model server (with custom Docker build)
- `gguf-server/Dockerfile` - Custom Dockerfile with GGUF plugin
- `models/` - Downloaded model weights
- `scripts/` - Python client scripts

## 🚀 Quick Start

### 1. Setup Python Environment (one-time)
```bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
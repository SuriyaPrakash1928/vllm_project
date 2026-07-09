from huggingface_hub import snapshot_download, hf_hub_download
import os

os.makedirs("models/Qwen2.5-0.5B-Instruct", exist_ok=True)
os.makedirs("models/Qwen2.5-0.5B-Instruct-GGUF", exist_ok=True)

print("Downloading Standard Model...")
snapshot_download(
    repo_id="Qwen/Qwen2.5-0.5B-Instruct",
    local_dir="models/Qwen2.5-0.5B-Instruct",
    ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.bin", "*.pt"]
)

print("Downloading GGUF Model...")
hf_hub_download(
    repo_id="bartowski/Qwen2.5-0.5B-Instruct-GGUF",
    filename="Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    local_dir="models/Qwen2.5-0.5B-Instruct-GGUF",
    local_dir_use_symlinks=False
)
print("✅ Models downloaded successfully!")
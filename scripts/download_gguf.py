import os
from huggingface_hub import hf_hub_download

REPO_ID = "bartowski/Qwen2.5-0.5B-Instruct-GGUF"
FILENAME = "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"

# Navigate to the models folder (one level up from scripts/)
script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, "..", "models")
os.makedirs(models_dir, exist_ok=True)

print(f"Downloading {FILENAME} from {REPO_ID}...")
local_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    local_dir=models_dir,
    local_dir_use_symlinks=False,
)
print(f"✅ Download complete! Saved to: {local_path}")
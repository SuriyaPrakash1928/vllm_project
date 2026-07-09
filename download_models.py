"""
Model Downloader for vLLM Project
Downloads and manages both Standard (HuggingFace) and GGUF models.
"""

import os
import sys
from huggingface_hub import snapshot_download, hf_hub_download

# Configuration
MODELS_DIR = "models"
STANDARD_MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
GGUF_REPO_ID = "bartowski/Qwen2.5-0.5B-Instruct-GGUF"
GGUF_FILENAME = "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"

def check_standard_model():
    """Check if the standard HuggingFace model is already downloaded."""
    model_path = os.path.join(MODELS_DIR, "standard_model")
    
    # Check for essential files
    required_files = [
        "config.json",
        "tokenizer.json",
        "tokenizer_config.json"
    ]
    
    if not os.path.exists(model_path):
        return False, "Folder does not exist"
    
    for file in required_files:
        if not os.path.exists(os.path.join(model_path, file)):
            return False, f"Missing {file}"
    
    # Check if at least one .safetensors file exists
    safetensors_files = [f for f in os.listdir(model_path) if f.endswith('.safetensors')]
    if not safetensors_files:
        return False, "No .safetensors files found"
    
    return True, f"Model complete with {len(safetensors_files)} weight file(s)"

def check_gguf_model():
    """Check if the GGUF model is already downloaded."""
    model_path = os.path.join(MODELS_DIR, GGUF_FILENAME)
    
    if not os.path.exists(model_path):
        return False, "File does not exist"
    
    # Check file size (should be around 380-400MB for Q4_K_M)
    file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    if file_size_mb < 300:  # If less than 300MB, it's probably incomplete
        return False, f"File exists but seems incomplete ({file_size_mb:.1f}MB)"
    
    return True, f"Model complete ({file_size_mb:.1f}MB)"

def download_standard_model():
    """Download the standard HuggingFace model."""
    print("\n" + "=" * 60)
    print("📥 Downloading Standard Model (HuggingFace format)")
    print("=" * 60)
    print(f"Model: {STANDARD_MODEL_ID}")
    print("This will download config files and model weights (~1GB)")
    print("Please wait, this may take several minutes...\n")
    
    model_path = os.path.join(MODELS_DIR, "standard_model")
    
    try:
        snapshot_download(
            repo_id=STANDARD_MODEL_ID,
            local_dir=model_path,
            local_dir_use_symlinks=False,
            ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.bin", "*.pt"]  # Only download safetensors
        )
        
        print("\n✅ Standard model downloaded successfully!")
        print(f"📁 Location: {os.path.abspath(model_path)}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading standard model: {e}")
        return False

def download_gguf_model():
    """Download the GGUF model."""
    print("\n" + "=" * 60)
    print("📥 Downloading GGUF Model (Quantized format)")
    print("=" * 60)
    print(f"Repository: {GGUF_REPO_ID}")
    print(f"File: {GGUF_FILENAME}")
    print("This will download the quantized model (~380MB)")
    print("Please wait, this may take several minutes...\n")
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    try:
        # Download the specific GGUF file
        hf_hub_download(
            repo_id=GGUF_REPO_ID,
            filename=GGUF_FILENAME,
            local_dir=MODELS_DIR,
            local_dir_use_symlinks=False
        )
        
        model_path = os.path.join(MODELS_DIR, GGUF_FILENAME)
        file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        
        print(f"\n✅ GGUF model downloaded successfully!")
        print(f"📁 Location: {os.path.abspath(model_path)}")
        print(f"📦 Size: {file_size_mb:.1f}MB")
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading GGUF model: {e}")
        return False

def main():
    """Main function to check and download models."""
    print("=" * 60)
    print("🤖 vLLM Model Manager")
    print("=" * 60)
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Check Standard Model
    print("\n📋 Checking Standard Model...")
    std_exists, std_msg = check_standard_model()
    if std_exists:
        print(f"✅ {std_msg}")
    else:
        print(f"⚠️  {std_msg}")
    
    # Check GGUF Model
    print("\n📋 Checking GGUF Model...")
    gguf_exists, gguf_msg = check_gguf_model()
    if gguf_exists:
        print(f"✅ {gguf_msg}")
    else:
        print(f"⚠️  {gguf_msg}")
    
    # Ask user what to download
    print("\n" + "-" * 60)
    print("Which model would you like to download?")
    print("  1. Standard Model (HuggingFace format)")
    print("  2. GGUF Model (Quantized format)")
    print("  3. Both models")
    print("  0. Exit")
    print()
    
    choice = input("Enter your choice (0-3): ").strip()
    
    if choice == "0":
        print("\n👋 Exiting...")
        sys.exit(0)
    
    elif choice == "1":
        if std_exists:
            print("\n✅ Standard model is already downloaded. No action needed.")
        else:
            download_standard_model()
    
    elif choice == "2":
        if gguf_exists:
            print("\n✅ GGUF model is already downloaded. No action needed.")
        else:
            download_gguf_model()
    
    elif choice == "3":
        if not std_exists:
            download_standard_model()
        else:
            print("\n✅ Standard model already exists, skipping...")
        
        if not gguf_exists:
            download_gguf_model()
        else:
            print("\n✅ GGUF model already exists, skipping...")
    
    else:
        print("\n❌ Invalid choice. Please run the script again.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Model management complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Download cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
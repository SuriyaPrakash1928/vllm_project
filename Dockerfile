FROM vllm/vllm-openai:latest

# Install the GGUF plugin so this single image can run GGUF files
RUN pip install vllm-gguf-plugin
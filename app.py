# import requests

# # Check if server is running
# response = requests.get("http://localhost:8000/v1/models")
# print("✅ Server is running!" if response.status_code == 200 else "❌ Server not running")

# # Send request to model
# response = requests.post(
#     "http://localhost:8000/v1/chat/completions",
#     json={
#         "model": "/model_path",
#         "messages": [{"role": "user", "content": "Explain Docker."}],
#         "max_tokens": 500,
#         "stream": True
#     }
# )

# # Print response
# print(response.json()["choices"][0]["message"]["content"])

import requests
import json

# 1. Check if server is running
response = requests.get("http://localhost:8000/v1/models")
print("✅ Server is running!" if response.status_code == 200 else "❌ Server not running")

# 2. Send request to model
response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "/model_path",  #for standard model
        # "model": "/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
        "messages": [{"role": "user", "content": "Explain Docker."}],
        "max_tokens": 500,
        "stream": True  # Tells the server to stream
    },
    stream=True  # Tells Python to process the stream chunk-by-chunk
)

# 3. Process the streaming response (Server-Sent Events format)
for line in response.iter_lines():
    if line:
        decoded = line.decode('utf-8')
        # SSE format starts with "data: " and ends with "data: [DONE]"
        if decoded.startswith("data: ") and decoded != "data: [DONE]":
            chunk = json.loads(decoded[6:]) # Remove "data: " and parse JSON
            print(chunk["choices"][0]["delta"].get("content", ""), end="", flush=True)

print() # Print a final newline when finished
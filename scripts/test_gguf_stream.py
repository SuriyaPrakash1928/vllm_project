"""Tests the GGUF model server with streaming output."""

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="empty",
)

print("🤖 Testing GGUF Model (Streaming)...")
print("-" * 50)

stream = input("You want streaming:(Default - False):")
if(stream == ''):
    stream = False

response = client.chat.completions.create(
    model="/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    messages=[{"role": "user", "content": "Write a short poem about Docker and AI."}],
    max_tokens=500,
    stream=stream,
    # Uncomment the next line to force exactly 500 tokens (ignores EOS):
    extra_body={"ignore_eos": True},
)
if stream:
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
else:
    print(response.choices[0].message.content)

print("\n" + "-" * 50)
print("✅ Generation complete!")

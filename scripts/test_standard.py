"""Tests the standard HuggingFace model server."""

import sys
from openai import OpenAI

# Configuration
BASE_URL = "http://localhost:8000/v1"
# This matches the '--model /model_path' argument in your docker-compose.yaml
MODEL_NAME = "/model_path" 

def main():
    print("=" * 60)
    print("🤖 Testing Standard Model Server")
    print("=" * 60)

    # 1. Initialize client
    client = OpenAI(
        base_url=BASE_URL,
        api_key="empty",
    )

    # 2. Check if the Docker server is running
    print("\n🔍 Checking if vLLM Docker server is running...")
    try:
        # A simple API call to check connectivity and list available models
        available_models = client.models.list()
        print("✅ Server is running and accessible!\n")
    except Exception as e:
        print("❌ Error: Cannot connect to the vLLM server.")
        print(f"Details: {e}")
        print("\n💡 Please ensure your Docker container is running:")
        print("   docker compose up vllm-standard")
        sys.exit(1)

    # 3. Get streaming preference
    stream_input = input("Do you want streaming output? (y/N): ").strip().lower()
    stream = stream_input == 'y'

    # 4. Send request
    print(f"\n📡 Sending request to model: {MODEL_NAME}")
    print("-" * 50)
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Explain Docker."}],
            max_tokens=500,
            stream=stream,
            extra_body={"ignore_eos": True},
        )

        # 5. Print response
        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="", flush=True)
        else:
            print(response.choices[0].message.content)

        print("\n" + "-" * 50)
        print("✅ Test completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
Test script to check which ZhipuAI models your API key can access
Run this locally to verify model availability
"""

import os
from zhipuai import ZhipuAI

# Get API key from environment variable
api_key = os.getenv("ZHIPU_API_KEY")

if not api_key:
    print("❌ Error: ZHIPU_API_KEY not found in environment variables")
    print("Please set it using: export ZHIPU_API_KEY='your-api-key'")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")
print("\n" + "="*60)
print("Testing available models...")
print("="*60 + "\n")

# Initialize client
client = ZhipuAI(api_key=api_key)

# Models to test
models_to_test = [
    "glm-4",
    "glm-4-plus",
    "glm-4-air",
    "glm-4-flash",
    "glm-3-turbo",
    "chatglm_turbo",
    "chatglm_std",
    "chatglm_lite"
]

test_message = "Hello, reply with 'OK' if you can read this."

available_models = []
unavailable_models = []

for model_name in models_to_test:
    try:
        print(f"Testing {model_name}...", end=" ")
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": test_message}],
            max_tokens=10
        )
        print("✅ Available")
        available_models.append(model_name)
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Not available - {error_msg[:50]}...")
        unavailable_models.append(model_name)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)

print(f"\n✅ Available models ({len(available_models)}):")
if available_models:
    for model in available_models:
        print(f"   - {model}")
else:
    print("   None")

print(f"\n❌ Unavailable models ({len(unavailable_models)}):")
if unavailable_models:
    for model in unavailable_models:
        print(f"   - {model}")
else:
    print("   None")

if available_models:
    print(f"\n💡 Recommendation: Use '{available_models[0]}' in your app.py")
else:
    print("\n⚠️ Warning: No models available. Check your API key permissions.")
    print("   Visit: https://open.bigmodel.cn/ to verify your account status")

print("\n" + "="*60)

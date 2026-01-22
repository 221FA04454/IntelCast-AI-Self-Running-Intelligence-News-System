"""
Quick D-ID API Key Test
"""
import requests
import base64

# Your API key as you entered it
api_key = "Yc3VtYW50aG9mZmljaWFsMjYyNkBnbWFpbC5jb206R0NRUWNTUHRXWE1yOVluSXZqYjRF"

print("Testing D-ID API Key...")
print(f"API Key: {api_key[:20]}...")

# Test 1: With "Basic " prefix
headers1 = {
    "Authorization": f"Basic {api_key}",
    "Content-Type": "application/json"
}

response1 = requests.get("https://api.d-id.com/talks", headers=headers1)
print(f"\nTest 1 (with 'Basic' prefix): Status {response1.status_code}")
print(f"Response: {response1.text[:200]}")

# Test 2: Decode to see what it contains
try:
    decoded = base64.b64decode(api_key).decode('utf-8')
    print(f"\nDecoded key format: {decoded[:30]}...")
except:
    print("\nCould not decode - might not be base64")

# Test 3: Check if it's email:password format and re-encode
if ":" in api_key:
    # It's already in email:password format
    encoded = base64.b64encode(api_key.encode()).decode()
    headers3 = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }
    response3 = requests.get("https://api.d-id.com/talks", headers=headers3)
    print(f"\nTest 3 (re-encoded): Status {response3.status_code}")
    print(f"Response: {response3.text[:200]}")

print("\n" + "="*60)
print("SOLUTION:")
print("="*60)
print("Please double-check your D-ID API key by:")
print("1. Going to https://studio.d-id.com/")
print("2. Click Settings > API")
print("3. Copy the EXACT API key shown there")
print("   (It should look like: email:password in base64)")
print("\nThe key should be in ONE of these formats:")
print("  - Just the base64 string (we'll add 'Basic')")
print("  - Already with 'Basic' prefix")

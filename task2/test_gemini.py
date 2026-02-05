from google import genai
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the client
client = genai.Client(api_key=api_key)

print("Testing connection with gemini-flash-latest...")

try:
    # Use the 'latest' alias which points to the best flash model you have
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="State 'System Online' if you can hear me."
    )
    print("✅ SUCCESS!")
    print(f"🤖 Response: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nAttempting Gemini 3 Preview...")
    try:
        # Second attempt using the newest model on your list
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Hello from Gemini 3!"
        )
        print("✅ SUCCESS (Gemini 3)!")
        print(f"🤖 Response: {response.text}")
    except Exception as e2:
        print(f"‼️ Still failing: {e2}")
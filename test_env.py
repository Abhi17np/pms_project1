from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(f"URL: {url[:30]}..." if url else "URL: Not found")
print(f"KEY: {key[:30]}..." if key else "KEY: Not found")
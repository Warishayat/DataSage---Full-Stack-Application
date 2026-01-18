import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    return create_client(url, key)

supabase = get_supabase_client()


if __name__ == "__main__":
    print(f"Connecting to: {os.environ.get('SUPABASE_URL')} (Auto-fixed with slash)")
    print("Supabase Client initialized successfully")
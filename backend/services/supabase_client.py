from supabase import create_client, Client
from config import get_settings

settings = get_settings()

supabase_client: Client = create_client(
    settings.supabase_url,
    settings.supabase_key
) if settings.supabase_url and settings.supabase_key else None

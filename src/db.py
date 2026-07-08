from supabase import Client, create_client

from src.config import Config


def get_supabase_client(config: Config) -> Client:
    return create_client(config.supabase_url, config.supabase_service_role_key)


def upsert_restaurants(client: Client, restaurants: list[dict]) -> None:
    if not restaurants:
        return

    (
        client.table("restaurantes")
        .upsert(restaurants, ignore_duplicates=False)
        .execute()
    )


def fetch_restaurants(client: Client) -> list[dict]:
    response = client.table("restaurantes").select("*").execute()
    return response.data or []

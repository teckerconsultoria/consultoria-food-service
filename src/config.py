import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    google_places_api_key: str
    google_geocoding_api_key: str
    supabase_url: str
    supabase_service_role_key: str


REQUIRED_ENV_VARS = [
    "GOOGLE_PLACES_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
]


def load_config() -> Config:
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return Config(
        google_places_api_key=os.getenv("GOOGLE_PLACES_API_KEY", ""),
        google_geocoding_api_key=os.getenv("GOOGLE_GEOCODING_API_KEY", ""),
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
    )

import os
import pytest

from src.config import load_config


def test_load_config_returns_required_values(monkeypatch):
    monkeypatch.setenv("GOOGLE_PLACES_API_KEY", "fake-places-key")
    monkeypatch.setenv("GOOGLE_GEOCODING_API_KEY", "fake-geocoding-key")
    monkeypatch.setenv("SUPABASE_URL", "https://fake.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "fake-service-key")

    config = load_config()

    assert config.google_places_api_key == "fake-places-key"
    assert config.google_geocoding_api_key == "fake-geocoding-key"
    assert config.supabase_url == "https://fake.supabase.co"
    assert config.supabase_service_role_key == "fake-service-key"


def test_load_config_raises_when_required_values_missing(monkeypatch):
    monkeypatch.delenv("GOOGLE_PLACES_API_KEY", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)

    with pytest.raises(RuntimeError, match="Missing required environment variables"):
        load_config()

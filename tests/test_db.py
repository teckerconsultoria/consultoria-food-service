from unittest.mock import MagicMock, patch

import pytest

from src.config import Config
from src.db import get_supabase_client, upsert_restaurants


def test_get_supabase_client_creates_client_with_config():
    config = Config(
        google_places_api_key="",
        google_geocoding_api_key="",
        supabase_url="https://fake.supabase.co",
        supabase_service_role_key="fake-key",
    )

    with patch("src.db.create_client") as mock_create_client:
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client

        client = get_supabase_client(config)

        mock_create_client.assert_called_once_with(
            "https://fake.supabase.co",
            "fake-key",
        )
        assert client is mock_client


def test_upsert_restaurants_calls_table_upsert():
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table

    restaurants = [
        {
            "place_id": "place_1",
            "nome": "Restaurante A",
            "endereco": "Rua 1",
            "bairro": "Manaíra",
            "lat": -7.115,
            "lng": -34.823,
            "tipo": "restaurant",
            "rating": 4.5,
            "price_level": 2,
            "tem_website": True,
            "permanently_closed": False,
            "data_coleta": "2026-07-08T00:00:00Z",
        }
    ]

    upsert_restaurants(mock_client, restaurants)

    mock_client.table.assert_called_once_with("restaurantes")
    mock_table.upsert.assert_called_once_with(restaurants, ignore_duplicates=False)
    mock_table.upsert.return_value.execute.assert_called_once()

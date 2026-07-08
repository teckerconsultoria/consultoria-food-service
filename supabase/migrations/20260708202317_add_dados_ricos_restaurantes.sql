-- Dados enriquecidos do place-details (MCP Google Maps)
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS telefone TEXT;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS horarios JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS dining_options JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS serves JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS atmosphere JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS payment_options JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS parking JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS accessibility JSONB;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS review_summary TEXT;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS photo_count INTEGER;
ALTER TABLE restaurantes ADD COLUMN IF NOT EXISTS editorial_summary TEXT;

COMMENT ON COLUMN restaurantes.horarios IS 'Horários de funcionamento (JSONB: open_now + weekday_text)';
COMMENT ON COLUMN restaurantes.dining_options IS 'Opções: dine_in, delivery, takeout, curbside_pickup, reservable';
COMMENT ON COLUMN restaurantes.serves IS 'Serve: beer, wine, cocktails, vegetarian, breakfast, lunch, dinner';
COMMENT ON COLUMN restaurantes.atmosphere IS 'Ambiente: good_for_groups, outdoor_seating, live_music, allows_dogs';
COMMENT ON COLUMN restaurantes.payment_options IS 'Pagamento: credit, debit, cash, nfc';
COMMENT ON COLUMN restaurantes.parking IS 'Estacionamento: freeStreetParking, valetParking, etc.';
COMMENT ON COLUMN restaurantes.accessibility IS 'Acessibilidade: wheelchair, entrance, seating';

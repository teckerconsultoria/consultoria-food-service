-- Cria tabela de restaurantes coletados do Google Places
CREATE TABLE IF NOT EXISTS restaurantes (
    place_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    endereco TEXT,
    bairro TEXT,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    tipo TEXT,
    rating DOUBLE PRECISION,
    price_level INTEGER,
    tem_website BOOLEAN DEFAULT FALSE,
    permanently_closed BOOLEAN DEFAULT FALSE,
    data_coleta TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para busca rápida por bairro
CREATE INDEX IF NOT EXISTS idx_restaurantes_bairro ON restaurantes(bairro);

-- Índice para busca rápida por categoria/tipo
CREATE INDEX IF NOT EXISTS idx_restaurantes_tipo ON restaurantes(tipo);

-- Comentários para documentação
COMMENT ON TABLE restaurantes IS 'Restaurantes coletados do Google Places para o piloto de segmentação de tráfego pago.';
COMMENT ON COLUMN restaurantes.place_id IS 'ID único do Google Places.';
COMMENT ON COLUMN restaurantes.bairro IS 'Bairro normalizado via reverse geocoding.';

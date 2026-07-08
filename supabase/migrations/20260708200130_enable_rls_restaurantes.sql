-- Habilita Row Level Security na tabela restaurantes
ALTER TABLE restaurantes ENABLE ROW LEVEL SECURITY;

-- Policy: qualquer um pode ler (útil para dashboard público futuro)
CREATE POLICY "restaurantes_select_public"
ON restaurantes
FOR SELECT
USING (true);

-- Policy: apenas service_role pode inserir
-- (service_role bypassa RLS, mas policy explícita documenta a intenção)
CREATE POLICY "restaurantes_insert_authenticated"
ON restaurantes
FOR INSERT
WITH CHECK (true);

-- Policy: apenas service_role pode atualizar
CREATE POLICY "restaurantes_update_authenticated"
ON restaurantes
FOR UPDATE
USING (true);

-- Policy: apenas service_role pode deletar
CREATE POLICY "restaurantes_delete_authenticated"
ON restaurantes
FOR DELETE
USING (true);

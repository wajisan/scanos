-- database-postgre/init.sql
CREATE TABLE IF NOT EXISTS urls_table (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    frequency INT NOT NULL,
    last_checked_data JSONB
);

-- Insérer des données de test
INSERT INTO urls_table (url, frequency) VALUES
('https://example.com', 10),
('https://example2.com', 15);

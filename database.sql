-- Volitelný pomocný SQL soubor.
-- Aplikace databázi i tabulku vytváří automaticky při spuštění.
-- Tento soubor není nutné ručně spouštět.

CREATE DATABASE IF NOT EXISTS projekt2
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE projekt2;

CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav VARCHAR(50) NOT NULL DEFAULT 'Nezahájeno',
    datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

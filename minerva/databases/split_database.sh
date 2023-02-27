#!/bin/bash

# Conta le righe totali del file
total_lines=$(wc -l < minerva/databases/big/orderbook_2023-02-17_14:00.db)

# Calcola il numero di file da creare
num_files=$((($total_lines + 4999) / 5000))

# Crea la directory di output se non esiste già
mkdir -p output

# Dividi il file in pezzi da 5000 righe ciascuno
split -l 5000 minerva/databases/big/orderbook_2023-02-17_14:00.db minerva/databases/big/orderbook_2023-02-17_14:00_

# Rinomina i file di output con estensione .db
for file in minerva/databases/big/*
do
  mv "$file" "$file.db"
done
#!/bin/bash

# Cerca tutti i processi che corrispondono al pattern "python3 minerva/"
pids=$(pgrep -f "python3 minerva/")

# Se non ci sono processi, esci
if [ -z "$pids" ]; then
  echo "Nessun processo trovato"
  exit 0
fi

# Termina tutti i processi trovati
echo "Terminazione dei processi con pid: $pids"
kill $pids

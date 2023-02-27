# DOING

[ ] testa il codice di ricerca operativa GA
[ ] testa l observer del GA

[ ] testa il codice di trading demo


# TO DO

[ ] crea gli Integrali del Tempo ( filtrare i dati ): fai la sommatoria della queue per ogni tot volumi

[ ] Final Genetic Evolution
    nel campione finale fai in modo di poter modificare ogni parametro singolarmente e ribacktestarlo
    parti da piu sequenze di parametri con un algoritmo genetico che testa prima A-B-C , uno che fa B-C-A e C-A-B.
    ogni singolo altro parametro resta uguale durante la mutazione. Generi un GA con solo un campione con un unico parametro
    modificato alla volta e questa e' la popolazione iniziale.  

[ ] format data into dataframe and not string

[ ] sql to feather or parquet file format 
        df.to_csv() => df.to_feather('test.feather')

# DONE
[x] unit test di tutto per capire ed unire i pezzi per poter poi modificare il programma da testato
    testa i comportamenti dei vari moduli

[x] crea il modulo trader.py e testa un trade effettivo su Binance.com ed aggiungi l'unittest

[x] aggiungi parametri alle strategie


[x] 1 streamer_savior

[x] 2 streamer_mock

[x] 3 oracle subscriber zmq
   
[x] 4 problema di una struttura dati che si riempie ma non si svuota

[x] 4.01 provato con la queue ma non funziona
[x] 5 capisci le differenze di strutture dati quando plotti le colonne orizzontali con lo streaming dei dati oppure con il backtesting
[x] 6 reformat + pulizia di strutture dati -> meno possibili sia in backtesting che in live
[x] 7 testa il live
[x] 8 reformat la struttura del codice dell oracolo
[x] 9 reformat dello streamer
[x] 10 fix allo streamer del websocket con il socket precedente
[x] 11 fix del visualizer
[x] 12 fix logica informazioni visualizzate
[x] 13 reformat delle informazioni visualizza
[x] 14 fix del .db con tabella BTCUSDT ed un unico filde .db
[x] 15 revert dell'argparse con un file di configurazioni (ancora dentro l'oracolo)

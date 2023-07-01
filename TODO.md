# TESTS
103.81 USDT@21:51 15 Aprile => 103.0 @ 22:15 

# DOING # TO DO

[ ] blockchain orderbook binance 5 nodi con intervalli di timestamp
    streamer argparse il link tcp o icp
    5zmq -> 1zmq algo -> oracle
                      -> db

[ ] crea gli Integrali del Tempo ( filtrare i dati ): 
    fai la sommatoria della queue per ogni tot volumi e segnati l'orderbook storico
    

[ ] Final Genetic Evolution
    nel campione finale fai in modo di poter modificare 
    ogni parametro singolarmente e ribacktestarlo alla fine della GA con un altra GA
    parti da piu sequenze di parametri con un algoritmo genetico che testa prima A-B-C , uno che fa B-C-A e C-A-B.
    ogni singolo altro parametro resta uguale durante la mutazione. Generi un GA con solo un campione con un unico parametro
    modificato alla volta e questa e' la popolazione iniziale.  

[ ] observer GA con fitness media e massima aumenta di generazione in generazione

[ ] real fitness vs theoretical dentro trading_observer e toglilo da oracle
   check balance all'inizio e segnatelo come initial_capital da quello calcoli con timestamp la fitness
   per la fitness teoretica basta che la leggi e te la segni all'inizio
 
# DONE

[x] test bot che fa le operazioni

[x] checker balance assets 1time at the second

[x] websocket data

[x]test GA fa nuove generazioni fino al numero stabilito

[x]test cambiano parametri fra di loro durante le generazioni

[x] test ga + observer linode

[x]big ga + observer linode

[x] test trading module: esegui operazioni facs simili

[x]test best strategy oracle.py –strategy + streamer.py live
    
[x] format data into dataframe and not string

[x] sql to feather or parquet file format 
        df.to_csv() => df.to_feather('test.feather')

[x]debuggare la chiusura dei processi su ga. Poi fare un nuovo nodo su linode, testare ga con orderbook di backtesting a minuti, e poi mettere la stessa directory ma con gli orderbook orari dell ultima settimana. 


[X] testa il codice di trading demo


[x] pickle updates on oracle

[x] subprocess operation test

[x] .parquet slpit

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

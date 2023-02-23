1. PRENDI DATI
1. TROVA PICCHI ASK
1. TROVA PICCHI BID
1. PLOTTA ORDERBOOK
1. PLOTTA THRESHOLD
1. PLOTTA PREZZO
1. PLOTTA PICCHI
1. TROVA MINIMI 

    peaks, _ = find_peaks( -y, height = 0, THRESHOLD = THRESHOLD_BTCUSDT, prominence = 5) #, distance = 1
    i picchi sono effettivamente quelli che vedo? -> setta THRESHOLD
    distanza dal picco precendente -> setta distanza
    bin = x
    intensita = y



?AUTOMATIZZARE QUANTI PICCHI CI SONO
?AUTOMATIZZARE IL FIT DELLE GAUSSIANE


### SOLUZIONE 1
grid search con fit gaussiana random +x,-x

### SOLUZIONE 2
il limite e' quello dove trovi un minimo nel range di -x,+x 
i minimi del picco li prendo come i due minimi locali accanto al massimo

Use this formula to calculate your trading fees when using leverage:
Account Size x Leverage = Position size
Position Size x Transaction Fee = Total fee


## Finance research
Dai dati di klines e' possibile ricavare i seguenti dati

- taker_buy_base_asset_volume = maker_sell_base_asset_volume

- taker_sell_base_asset_volume = maker_buy_base_asset_volume

- total_volume = taker_buy_base_asset_volume + taker_sell_base_asset_volume = maker_buy_base_asset_volume + maker_sell_base_asset_volume



## Teoria dell Architettura di controllo del processo

È un tipo di architettura del flusso di dati in cui i dati non sono né sequenziali in batch né flussi pipeline. Il flusso di dati proviene da un insieme di variabili, che controlla l'esecuzione del processo. Scompone l'intero sistema in sottosistemi o moduli e li collega.
Tipi di sottosistemi

Un'architettura di controllo di processo dovrebbe avere un'unità di elaborazione per modificare le variabili di controllo di processo e un'unità di controllo per calcolare la quantità di modifiche.

Un'unità di controllo deve avere i seguenti elementi −

    Variabile controllata - La variabile controllata fornisce valori per il sistema sottostante e dovrebbe essere misurata dai sensori. Ad esempio, la velocità nel sistema di controllo automatico della velocità.

    Input Variable - Misura un input per il processo. Ad esempio, la temperatura dell'aria di ritorno nel sistema di controllo della temperatura

    Variabile manipolata - Il valore della variabile manipolata viene regolato o modificato dal controller.

    Definizione di processo - Include meccanismi per manipolare alcune variabili di processo.

    Sensore − Ottiene i valori delle variabili di processo pertinenti al controllo e può essere utilizzato come riferimento di feedback per ricalcolare le variabili manipolate.

    Set Point − È il valore desiderato per una variabile controllata.

    Algoritmo di controllo - Viene utilizzato per decidere come manipolare le variabili di processo.

## Demoni
### Start deamons with nohup

```nohup python3 teleryum.py > /path/to/custom.out &```

```nohup ./mn.sh > myscipt.sh &```

### get process id

```ps aux | grep teleryum.py```

```pgrep -a teleryum.py```


### kill processes

```kill -9 <PID>```

```kill -l```

```kill <PID>```


There are many fiddly things to take care of when becoming a well-behaved daemon process:
- prevent core dumps (many daemons run as root, and core dumps can contain sensitive information)
- behave correctly inside a chroot gaol
- set UID, GID, working directory, umask, and other process parameters appropriately for the use case
- relinquish elevated suid, sgid privileges
- close all open file descriptors, with exclusions depending on the use case
- behave correctly if started inside an already-detached context, such as init, inetd, etc.
- set up signal handlers for sensible daemon behaviour, but also with specific handlers determined by the use case
- redirect the standard streams stdin, stdout, stderr since a daemon process no longer has a controlling terminal
- handle a PID file as a cooperative advisory lock, which is a whole can of worms in itself with many contradictory but valid ways to behave
- allow proper cleanup when the process is terminated
- actually become a daemon process without leading to zombies

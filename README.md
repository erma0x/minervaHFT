# Leonardo
### High frequency automated trading system with volumes data driven system capital allocation.

- price discovery through limit orderd book imbalances
- limit order front running

<br>

![](docs/img/banner.png)

<br>

## **Installation**

1. `python3 -m venv venv` <br> install virtual enviroenment

2. `source venv/bin/activate` <br> activate virtual enviroenment

3. `python3 -m pip3 install --upgrade pip` <br> upgrade packet manager

4. `python3 -m pip3 install -r requirements.txt` <br> install project requirement libraries

4. `python3 -m pip3 install --upgrade python-binance` <br> install upgrades for python-binance library

5. `export binance_api="your api key"` <br> export binance.com api key

6. `export binance_secret="your api secret"` <br> export binance.com api secret

7. `export kucoin_api="your api key"` <br> export kucoin.com api key

8. `export kucoin_secret="your api secret"` <br> export kucoin.com api secret

## **How to run**

    ```
    
    python3 minerva.py --plot_data 1 --capital 10000 --limit_orderbook 500 --relative_threshold 15 --short_pressure 0.69 --long_pressure 0.31 --max_councurrent_trades 10 --peak_distance_divisor 50 --stop_loss_price_buffer 0.5 --percentage_per_trade 0.1 --ask_bid_window 50 --take_profit_price_buffer 1.0 --treshold_operative_volume_ab 0.00001 --market BTCUSDT
    
    ```

1. `python3 data_streamer.py` <br> STREAM: price, orderbook, klines

2. `python3 data_visualizer.py` <br> VISUALIZE: price, candlestick, orderbook, volume profile, open trades

3. `python3 white_dragon.py` <br> GET and DATA PROCESS: price, volume profile, orderbook -> POST(or not) trading_operation

4. `python3 risk_maneagement.py` <br> GET trading_operation -> risk maneagement -> POST trading_operation

5. `python3 live_trader.py` <br> GET trading_operation -> POST kucoin/api trade

<br>
________________________________

##  **Algorithm**
  
####  **SET ENTRIES, TAKE PROFITS AND STOP LOSSES OPERATION**

    HFT with directional move on void of orderbook+traded volumes an positioning
    on the within the nearby orderbook+traded volumes.

    1. vedi se ci sono operazioni aperte identiche o simili
        
    1. vedi se ci sono troppe operazioni aperte (troppo numero o troppo capitale investito) 

    1. calcolo se nell' immediato ci sono segnali puliti per applicare i vuoti volumetrici 
        volume profile del immediato e confrontarlo con l'order book, 
        se ci sono forti capitali fra i segnati calcolati meglio disdire

    1. calcolo del range in cui e' possibile aprire un operazione ENTRY ampiezza segnale volumetrico pulito

    1. se il prezzo e' nel range e l'order book sta per essere pienato da una unica direzione (LONG o SHORT)

    1. imposta ENTRY limite a prezzo svantaggioso nella direzione in cui sta andando

    1. imposta TP nel picco accanto rispetto al movimento secondo wychoff

    1. imposta SL nel picco accanto rispetto al movimento secondo wychoff 

### **RISK MANEAGEMENT**
    - 3% for trade with max allowed leverage 
    - 90% allowed parallel trading capital

<br>

### **DATASTREAMING** 
    
    Take data from binance.com
    - prendi volume profile ogni minuto e salvalo giornaliero
    - prendi il prezzo ogni minuto
    - x = prendi l'order book ogni minuto

<br>

### **EXCHANGES**
    
    TRADING               www.kucoin.com      
    TRADING               www.ftx.com         
    
    DATA STREAMING        www.binance.com

<br>


## **APIs**
### binance api 
#### exchangeInfo
- https://api.binance.com/api/v3/exchangeInfo
- https://api.binance.com/api/v3/exchangeInfo?symbol=BTCUSDT

#### server info
- https://api.binance.com/api/v3/time 
- https://api.binance.com/api/v3/ping

#### klines
- https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1
- https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=1

#### example klines 
- https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1
  
``` json
    [
      [
        1499040000000,      // Kline open time
        "0.01634790",       // Open price
        "0.80000000",       // High price
        "0.01575800",       // Low price
        "0.01577100",       // Close price
        "148976.11427815",  // Volume
        1499644799999,      // Kline Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "0"                 // Unused field, ignore.
      ]
    ]
```
### **FTX.com** APIs

<br>

________________________________

## Finance research
Dai dati di klines e' possibile ricavare i seguenti dati

- taker_buy_base_asset_volume = maker_sell_base_asset_volume

- taker_sell_base_asset_volume = maker_buy_base_asset_volume

- total_volume = taker_buy_base_asset_volume + taker_sell_base_asset_volume = maker_buy_base_asset_volume + maker_sell_base_asset_volume


<br>

________________________________

## Architettura di controllo del processo

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

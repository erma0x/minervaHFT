# MinervaHFT

<img src="./documents/space.gif" width="1600" />


## Description

High frequency Automated Trading System with crypto volumes data driven system capital allocation.
HFT with directional move on void of orderbook+traded volumes an positioningon the within the nearby orderbook+traded volumes. Price discovery through limit orderd book imbalances. Limit order front running.

## Development tools
- https://dev.binance.vision/
- https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
- https://www.binance.com/en
  
## How to run

###  Install
```bash
python3 setup.py install
```

### Unit-test project 
```bash
python3 -m unittest discover -v ./tests/
```
alternative
```
make test 
```

### Check evolution processes 
```bash
ps -aux | grep python3
```
alternative
```
htop
```
alternative
```
top
```

## Components
- streamer :         backtest/live, save in SQL .db
- oracle :           find LONG/SHORT, TP/SL/ENTRY, RISK-MANAGER, TRADER
- genetic_algorithm: evolve oracle strategies


### Trading API

https://api3.binance.com/api/v3/ping


```bash
export BINANCE_API_KEY='la_tua_api_key'
export BINANCE_API_SECRET='il_tuo_api_secret'
```
```python
import os

api_key = os.environ.get('BINANCE_API_KEY')
api_secret = os.environ.get('BINANCE_API_SECRET')
```


###  Trading execution
#### Japan Server (Linode.com)
```bash
python3 minerva/streamer.py                  # stream and save data
python3 minerva/oracle.py -s ./strategy_0.py # check signal and trading_operation generation
                                             # connect to binance.com for risk manager and trade execution
                                             # write fitness on file strategy.py

python3 minerva/observer_account.py          # connect to binance
                                             # check read real fitness (fitness strategy.py) vs theoretical fitness (what is printed out of oracle with PRINT)
```

###  Evolve: genetic algorithms
``` 
python3 observer_genetic_algorithm.py
python3 genetic_algorithm.py
```


## **How to run the Automated Trading System**
1. `python3 streamer.py` <br> STREAM: price, orderbook, klines
2. `python3 visualizer.py` <br> VISUALIZE: price, candlestick, orderbook, volume profile, open trades
3. `python3 oracle.py` <br> GET and DATA PROCESS: price, volume profile, orderbook -> POST(or not) trading_operation
4. `python3 oracle.py` <br> GET trading_operation -> risk maneagement -> POST trading_operation
5. `python3 oracle.py` <br> GET trading_operation -> POST kucoin/api trade

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

##  **Algorithm for Entries, Take Profits and Stop Losses**

1. see if there are any identical or similar open trades
1. see if there are too many open trades (too many or too much invested capital)
1. Calculate if there are immediate clean signals to apply volumetric voids
     volume profile of the immediate and compare it with the order book,
     if there are strong capitals among the calculated scores, it is better to cancel
1. calculation of the range in which it is possible to open an ENTRY operation clean volumetric signal amplitude
1. if the price is in the range and the order book is about to be filled from a single direction (LONG or SHORT)
1. Set ENTRY limit at disadvantageous price in the direction it is going
1. set TP in the next peak with respect to the movement according to wychoff
1. set SL in the next peak with respect to the movement according to wychoff

### **Algorithm for Risk Maneagement**
    - 3% for trade with max allowed leverage 
    - 90% allowed parallel trading capital

<br>

### **Streamer** 
    
    Take data from binance.com
    - prendi volume profile ogni minuto e salvalo giornaliero
    - prendi il prezzo ogni minuto
    - x = prendi l'order book ogni minuto
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


## example of command

```python3 minerva.py --plot_data 0 --capital 10000 --limit_orderbook 500 --relative_THRESHOLD 10 --short_pressure 0.75 --long_pressure 0.25 --max_concurrent_trades 5 --peak_distance_divisor 10 --stop_loss_price_buffer 0.2 --precentage_per_trade 0.18 --market BTCUSDT```


```python3 minerva.py -plt False -cap 5000 -lo 500 -rt 10 -sp 0.75 -lp 0.25 -maxt 5 -pkd 10 -pf 1 --market BTCUSDT```

## Workflow
1. GET DATA
2. FIND PEAKS ASK
3. FIND PEAK BIDs
4. PLOT ORDERBOOK
5. PLOT THRESHOLD
6. PRICE PLOT
7. PLOT PEAKS
9. FIND MINIMA

```python3
peaks, _ = find_peaks( -y, height = 0, THRESHOLD = THRESHOLD_BTCUSDT, prominence = 5) #, distance = 1```
```   

are the peaks actually what I see? -> set THRESHOLD
     distance from previous peak -> set distance

 bin = x
 intensity = y


 Use this formula to calculate your trading fees when using leverage:
 Account Size x Leverage = Position size
 Position Size x Transaction Fee = Total fee


## Finance research
Dai dati di klines e' possibile ricavare i seguenti dati

- taker_buy_base_asset_volume = maker_sell_base_asset_volume

- taker_sell_base_asset_volume = maker_buy_base_asset_volume

- total_volume = taker_buy_base_asset_volume + taker_sell_base_asset_volume = maker_buy_base_asset_volume + maker_sell_base_asset_volume



## Process Control Architecture Theory

It is a type of data flow architecture where the data is neither batch sequential nor pipelined flows. The data flow comes from a set of variables, which controls the execution of the process. It breaks down the whole system into subsystems or modules and connects them.
Types of subsystems

A process control architecture should have a processing unit to change the process control variables and a controller to calculate the amount of changes.

A control unit must have the following elements −

     Controlled Variable - The controlled variable provides values for the underlying system and should be measured by sensors. For example, the speed in cruise control.

     Input Variable - Measures an input to the process. For example, the return air temperature in the temperature control system

     Manipulated variable - The value of the manipulated variable is adjusted or changed by the controller.

     Process definition - Includes mechanisms for manipulating some process variables.

     Sensor − Obtains the values of the process variables relevant to the control and can be used as a feedback reference to recalculate the manipulated variables.

     Set Point − This is the desired value for a controlled variable.

     Control algorithm - It is used to decide how to manipulate process variables.

## Deamons
### Start deamons with nohup

```nohup python3 streamer.py > ./results.out 2>&1 &```

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










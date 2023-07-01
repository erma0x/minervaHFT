
## POSITIONING algorithm

    trova il primo picco sopra
    trova il secondo picco sotto (e fammeli vedere)
    metti TP nel picco sopra (LONG), entry nel microprice a market
    e SL nel picco sotto - SL_BELOW_PRICE (eg. 5.0 su BTCUSDT)
    segnati Entry TP e SL come TRADING_OPERATION
    calcola il Rendimento/Rischio  =>long (TP-ENTRY/ENTRY-SL) 
    se R/R > 0.8 allora COMUNICA la operazione a visualizer e trader
    ci sono picchi vicino al prezzo?
    

if asks_prices[peaks_asks[0]] - MID_PRICE  < 5.0 and MID_PRICE - bids_prices[peaks_bids[0]] < 5.0:        
- esiste un segnale per andare long o short?
- ci sono troppe operazioni aperte?

Se una delle due e' molto piu grande delle altre allora fai front running

A = prendo asks_prices dal prezzo piu basso e prendo i primi X1 in ordine CRESCENTE
B = prendo bids_prices dal prezzo piu basso e prendo i primi X1 in ordine DE-CRESCENTE

## ENTRY
       if A > THRESHOLD e B > THRESHOLD
    if A > THRESHOLD_VOLUME_BTCUSDT => short
    if B > THRESHOLD_VOLUME_BTCUSDT  and  a/(a+b)   =>   long


## POSITIONING
    prendo Ask e Bid con un filtro minimo di volumi THRESHOLD_BTCUSDT
    take the first volume peak in the ask and in the bid arrays

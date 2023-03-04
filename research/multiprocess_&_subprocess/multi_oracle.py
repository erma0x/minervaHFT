
import numpy as np
from minerva.oracle import *

def oracle(message, strategy):

    buffer_object = message.decode().split('|')

    MARKET = strategy['MARKET']
    LIMIT_ORDER_BOOK = strategy['LIMIT_ORDER_BOOK']
    RELATIVE_THRESHOLD_DIV = strategy['RELATIVE_THRESHOLD_DIV']
    THRESHOLD_SHORT = strategy['THRESHOLD_SHORT']
    THRESHOLD_LONG = strategy['THRESHOLD_LONG']
    MAX_SECONDS_TRADE_OPEN = strategy['MAX_SECONDS_TRADE_OPEN']
    PEAK_DISTANCE_DIVISOR = strategy['PEAK_DISTANCE_DIVISOR']
    SL_PRICE_BUFFER = strategy['SL_PRICE_BUFFER']
    TP_PRICE_BUFFER = strategy['TP_PRICE_BUFFER']
    PERCENTAGE_PER_TRADE = strategy['PERCENTAGE_PER_TRADE']
    K1 = strategy['K1']
    K2 = strategy['K2']
    K3 = strategy['K3']
    W_I = strategy['W_I']


    LOAD_DATA_SUCCESS = False

    try:    
        data_timestamp = buffer_object[0]
        # from string of list of lists to list of lists
        ask_array = from_string_to_list_of_lists(buffer_object[1])
        bid_array = from_string_to_list_of_lists(buffer_object[2])
        LOAD_DATA_SUCCESS = True
    except:
        LOAD_DATA_SUCCESS = False

    if LOAD_DATA_SUCCESS:
        # add list of lists to queue
        #my_buffer_ask.append(ask_array) 
        #my_buffer_bid.append(bid_array)
    
        asks_prices = np.hsplit(np.array(ask_array),2)[1].reshape(-1)
        asks_volumes =  np.hsplit(np.array(ask_array),2)[0].reshape(-1)
        bids_prices =  np.hsplit(np.array(bid_array),2)[1].reshape(-1)
        bids_volumes =  np.hsplit(np.array(bid_array),2)[0].reshape(-1)        

        max_ask_absolute_volume = max(asks_volumes)
        max_bid_absolute_volume = max(bids_volumes)
        min_ask_price = min(asks_prices)
        max_bid_price = max(bids_prices)

        MID_PRICE = (min_ask_price + max_bid_price) / 2


        #######################################################################
        ###################         SIGNAL GENERATOR        ###################
        #######################################################################
        # Se una delle due e' molto piu grande delle altre allora fai front running
        # A = prendo asks_prices dal prezzo piu basso e prendo i primi X1 in ordine CRESCENTE
        # B = prendo bids_prices dal prezzo piu basso e prendo i primi X1 in ordine DE-CRESCENTE
        # ENTRY algorithm
        # se A > THRESHOLD e B > THRESHOLD
        # if A > THRESHOLD_VOLUME_BTCUSDT => short
        # if B > THRESHOLD_VOLUME_BTCUSDT  and  a/(a+b)   =>   long


        A = sum(asks_volumes[:W_I]) * K1 +sum(asks_volumes[W_I:W_I*2]) * K2 + sum(asks_volumes[W_I*2:W_I*3] * K3 )

        B = sum(bids_volumes[:W_I]) * K1 +sum(asks_volumes[W_I:W_I*2]) * K2 + sum(asks_volumes[W_I*2:W_I*3] * K3 )

        OPERATION_PARAMETER = round(  A / ( A + B ) ,3 )

        OPERATION_SIDE = ""

        if OPERATION_PARAMETER > THRESHOLD_SHORT and ALLOW_SHORT_OPERATIONS==True:
            OPERATION_SIDE = "SHORT" 

        elif OPERATION_PARAMETER < THRESHOLD_LONG and ALLOW_LONG_OPERATIONS==True:
            OPERATION_SIDE = "LONG" 
        
        else:
            OPERATION_SIDE = "WAIT"


        #######################################################################
        ###################           POSITIONING           ###################
        #######################################################################
        # prendo Ask e Bid con un filtro minimo di volumi THRESHOLD_BTCUSDT

        # take the first volume peak in the ask and in the bid arrays
        x_all = np.where(asks_prices == min_ask_price)[0] # find the index of this in the list
        y_all = np.where(bids_prices == max_bid_price)[0]

        #if x_all.any():
        #    x = deepcopy(np.where(asks_prices == min_ask_price)[0][0]) # find the index of this in the list
        
        #if y_all.any():
        #    y = deepcopy(np.where(bids_prices == max_bid_price)[0][0])

        BEST_ASK_OFFER_PRICE = asks_prices[x_all] # lowest ask
        BEST_BID_OFFER_PRICE = bids_prices[y_all] # highest bid

        #MICRO_PRICE = (BEST_ASK_OFFER_VOLUME*max_bid_price + BEST_BID_OFFER_VOLUME*min_ask_price) / BEST_ASK_OFFER_VOLUME+BEST_BID_OFFER_VOLUME
        #THRESHOLD_BTCUSDT = 0.2
        THRESHOLD_BTCUSDT = max(max_ask_absolute_volume, max_bid_absolute_volume) / RELATIVE_THRESHOLD_DIV
        
        # number of channels / int
        PEAK_DISTANCE = int(round(LIMIT_ORDER_BOOK / PEAK_DISTANCE_DIVISOR))

        peaks_asks, _1 = find_peaks(
            asks_volumes, height=0, threshold= THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)
        peaks_bids, _2 = find_peaks(
            bids_volumes, height=0,  threshold=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)

        
        ENTRY,STOP_LOSS,TAKE_PROFIT,REWARD_RISK_RATEO  = 0,0,0,0
        # long or short
        REWARD_RISK_RATEO = 0
        if peaks_bids.any():
            #if MID_PRICE - bids_prices[peaks_bids[0]].size  < 20 :
                if OPERATION_SIDE=="LONG":
                    TAKE_PROFIT = get_max_peak_price(peaks_asks,asks_prices) - TP_PRICE_BUFFER
                    STOP_LOSS = get_max_peak_price(peaks_bids,bids_prices) - SL_PRICE_BUFFER
                    ENTRY = BEST_ASK_OFFER_PRICE
                    REWARD_RISK_RATEO = (TAKE_PROFIT-ENTRY)/(ENTRY-STOP_LOSS)
        
    
        if peaks_asks.any():
            #if asks_prices[peaks_asks[0]] - MID_PRICE  < 5.0:
                if OPERATION_SIDE=="SHORT":
                    TAKE_PROFIT = get_max_peak_price(peaks_bids,bids_prices) + TP_PRICE_BUFFER 
                    STOP_LOSS = get_max_peak_price(peaks_asks,asks_prices) + SL_PRICE_BUFFER
                    ENTRY = BEST_BID_OFFER_PRICE
                    REWARD_RISK_RATEO = (ENTRY-TAKE_PROFIT)/(STOP_LOSS-ENTRY)
            
        TRADING_OPERATION = {"side": OPERATION_SIDE,
                            "symbol": MARKET,  
                            "take_profits": TAKE_PROFIT,
                            "entry_prices": ENTRY,  
                            "stop_losses": STOP_LOSS,
                            "reward_risk_rateo":REWARD_RISK_RATEO,
                            "start_time":datetime.now()}
        return TRADING_OPERATION




        #######################################################################
        ###################         RISK MANAGER            ###################
        #######################################################################
        
# Connected to Binance

def risk_manager():
    LONG_OPERATIONS,SHORT_OPERATIONS = 0, 0
    for k,v in TRADE_ORDERBOOK.items():
        if v['side']=='LONG':
            LONG_OPERATIONS+=1
        if v['side']=='SHORT':
            SHORT_OPERATIONS+=1

    AVAILABLE_CAPITAL = (SHORT_OPERATIONS + LONG_OPERATIONS) <= MAX_CONCURRENT_OPEN_TRADES

    if REWARD_RISK_RATEO > 0.2 and AVAILABLE_CAPITAL:

        POSITION_SIZE = EQUITY * PERCENTAGE_PER_TRADE * LEVERAGE
        N_TOKEN_CONTRACT = POSITION_SIZE / MID_PRICE 
        TRADING_OPERATION = {"side": OPERATION_SIDE,
                            "symbol": MARKET,  
                            "take_profits": [TAKE_PROFIT],
                            "entry_prices": [ENTRY],  
                            "stop_losses": [STOP_LOSS],
                            "leverage": str(LEVERAGE),
                            "n_token":N_TOKEN_CONTRACT,
                            "usd_position":POSITION_SIZE,
                            "reward_risk_rateo":REWARD_RISK_RATEO,
                            "start_time":datetime.now(),
                            "running_time":0}
                                
        TRADE_ID += 1
        TRADE_ORDERBOOK[TRADE_ID] = TRADING_OPERATION # RUN TRADE 

    #######################################################################
    ###################         MONITOR POSITIONS       ###################
    #######################################################################
    
    TIME_COUNTER += 1
    SECONDS_COUNTER = TIME_COUNTER * REQUEST_TIME_INTERVAL
    MINUTES_COUNTER = SECONDS_COUNTER/60
    HOURS_COUNTER = MINUTES_COUNTER/60
    DAYS_COUNTER = round(HOURS_COUNTER/24,5)

    UNREALIZED_PNL = 0
    if TRADE_ORDERBOOK:
        CLOSED_TRADE_ID = []
        for op in TRADE_ORDERBOOK.items():
            
            # EXTRACT DATA
            ID_TRADE_ = op[0]
            TRADING_OPERATION_ = op[1]
            CLOSE_TRADE = False

            # no more than 50%LONG 50% SHORT
            OPERATION_SIDE_ = op[1]['side']
            LONG_OPERATIONS,SHORT_OPERATIONS=0,0
            if OPERATION_SIDE_ == "LONG":
                LONG_OPERATIONS+=1
            if OPERATION_SIDE_ == "SHORT":
                SHORT_OPERATIONS+=1

            # GET DATA FROM OPERATION
            REWARD_RISK_RATEO = op[1]["reward_risk_rateo"]
            LEVERAGE = int(op[1]['leverage'])
            POSITION_SIZE = op[1]['usd_position']
            N_TOKEN_CONTRACT = op[1]['n_token']
            START_TIME = op[1]["start_time"]

            # CALCULATE THE POSITION GAIN
            if OPERATION_SIDE_ == "LONG":
                GAIN = (BEST_BID_OFFER_PRICE - op[1]['entry_prices'][0]) * N_TOKEN_CONTRACT  
            if OPERATION_SIDE_ == "SHORT":
                GAIN = (op[1]['entry_prices'][0] - BEST_ASK_OFFER_PRICE ) * N_TOKEN_CONTRACT 

            # CALCULATE THE FEES
            GAIN = GAIN - GAIN * TAKER_FEES

            UNREALIZED_PNL += GAIN

            # CLOSE THE POSITION IF TOO MUCH TIME HAS BEEN PASSED
            if datetime.now() > START_TIME + timedelta(seconds = MAX_SECONDS_TRADE_OPEN ):
                CLOSE_TRADE = True
                
            # TAKE PROFIT
            if OPERATION_SIDE_ == "LONG":
                if MID_PRICE >= TRADING_OPERATION_['take_profits'][0]:
                    CLOSE_TRADE=True

                if MID_PRICE <= TRADING_OPERATION_['stop_losses'][0]:
                    CLOSE_TRADE=True
                    
            # STOP LOSS
            if OPERATION_SIDE_ == "SHORT":
                if MID_PRICE <= TRADING_OPERATION_['take_profits'][0]:
                    CLOSE_TRADE=True

                if MID_PRICE >= TRADING_OPERATION_['stop_losses'][0]:
                    CLOSE_TRADE=True
            
            # CLOSE THE TRADE
            if CLOSE_TRADE:
                if OPERATION_SIDE_ == "SHORT":
                    GAIN = (op[1]['entry_prices'][0] - MID_PRICE) * N_TOKEN_CONTRACT
                
                if OPERATION_SIDE_ == "LONG":
                    GAIN = (MID_PRICE - op[1]['entry_prices'][0]) * N_TOKEN_CONTRACT

                GAIN = GAIN - GAIN*TAKER_FEES
                EQUITY += GAIN

                GAIN_PERCENTAGE_24H = ((EQUITY-INITIAL_CAPITAL)/INITIAL_CAPITAL * 100 ) / DAYS_COUNTER
                                        
                if type(GAIN_PERCENTAGE_24H) != float :
                    GAIN_PERCENTAGE_24H = float(GAIN_PERCENTAGE_24H[0])

                store_pickle(new_data = GAIN_PERCENTAGE_24H, filename= STRATEGY_PATH.replace('.py','.pickle'))
                #update_performance( performance = GAIN_PERCENTAGE_24H , performance_name = "fitness" , path = STRATEGY_PATH )

                CLOSED_TRADE_ID.append( ID_TRADE_ )

        # DELETE ALL THE CLOSED TRADE FROM THE TRADE ORDERBOOK
        for id_ in CLOSED_TRADE_ID:
            TRADE_ORDERBOOK = del_trade_orderbook(TRADE_ORDERBOOK, id_)

    # APPLY RUNNING TIME UPDATE TO EACH TRADE
    for op in TRADE_ORDERBOOK.items():
        ID_TRADE_ = op[0]
        TRADING_OPERATION_ = op[1]
        START_TIME = TRADING_OPERATION_['start_time']
        TRADING_OPERATION_['running_time'] =  datetime.now() - START_TIME                     
        TRADE_ORDERBOOK[ID_TRADE_] = TRADING_OPERATION_ 

    return TRADE_ORDERBOOK


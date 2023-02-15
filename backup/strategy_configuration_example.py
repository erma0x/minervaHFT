#######################################################################
###################   STRATEGY PARAMETERS           ###################
#######################################################################
MARKET = 'BTCUSDT'
LIMIT_ORDER_BOOK =  500
RELATIVE_THRESHOLD_DIV = 10 # int (2,100) "relative operative trading threshold refered to : max_local_volume/relative_threshold "
THESHOLD_SHORT = 0.63
THESHOLD_LONG = 0.37
MAX_CONCURRENT_OPEN_TRADES = 6
MAX_SECONDS_TRADE_OPEN = 360
PEAK_DISTANCE_DIVISOR = 50 #"peak_distance = limit_orderbook/peak_distance_divisor"
SL_PRICE_BUFFER = 0.5 #"add absolute price buffer for the stop loss, is the distance in price from the sl peak"
TP_PRICE_BUFFER = 0.5 #"add absolute price buffer for the take profit, is the distance in price from the tp peak"
MARKET = "BTCUSDT" # BTCUSDT 
PERCENTAGE_PER_TRADE = 0.01 # 0.01 = 1%
GAIN_PERCENTAGE_24H = 0.2
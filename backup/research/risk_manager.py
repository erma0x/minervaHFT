from configuration_backtest import *

def risk_manager(EQUITY,REWARD_RISK_RATEO):
    """
    get the trading operation from the oracle(kaf) and confirm
    """
    if REWARD_RISK_RATEO > 3.0:

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
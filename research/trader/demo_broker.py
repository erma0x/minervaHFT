#!/usr/bin/env python3

from dataclasses import dataclass
import math
import datetime

@dataclass
class DemoBroker:
    """
    Simulate a demo account
    """
    unrialized_pnl: float # 
    realized_pnl: float # real value
    trading_book: dict
    ticker: str
    TAKER_FEES: float
    long_operations: int
    short_operations: int
    max_concurrent_operations: int
    equity_array: list
    initial_capital: float
    max_open_operation_seconds: int
    MID_PRICE: float

    def __str__(self):
        print(f'equity          {self.equity} $')
        print(f'unrealized P&L  {self.unrialized_pnl}')
        print(f'realized P&L    {self.realized_pnl}')
        print(f'number of LONG open trades:   { self.long_operations}')
        print(f'number of SHORT open trades:  {math.floor(self.max_concurrent_operations/2)}')      
        
    def delete_operation_from_trading_book(self,trade_id:int):
        for trade_id_ , _ in self.trading_book.items():
            if (trade_id == trade_id_ ):
                del self.trading_book[trade_id]
        
    def update_tradebook_informations(self):
            
        UNREALIZED_PNL = 0
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

            REWARD_RISK_RATEO = op[1]["reward_risk_rateo"]
            LEVERAGE = int(op[1]['leverage'])
            POSITION_SIZE = op[1]['usd_position']
            N_TOKEN_CONTRACT = op[1]['n_token']
            START_TIME = op[1]["start_time"]

            if OPERATION_SIDE_ == "LONG":
                GAIN = (self.MID_PRICE - op[1]['entry_prices'][0]) * N_TOKEN_CONTRACT  
            if OPERATION_SIDE_ == "SHORT":
                GAIN = (op[1]['entry_prices'][0] - self.MID_PRICE ) * N_TOKEN_CONTRACT 

            GAIN = GAIN - GAIN * self.TAKER_FEES
            UNREALIZED_PNL += GAIN


            # calcolare se le fees sono GAIN - GAIN * TAKER_FEES
            # too much time open
            if datetime.now() > START_TIME + datetime.timedelta(seconds = self.max_open_operation_seconds ):
                CLOSE_TRADE = True
                
            # TAKE PROFIT
            if OPERATION_SIDE_ == "LONG":
                if self.MID_PRICE >= TRADING_OPERATION_['take_profits'][0]:
                    CLOSE_TRADE=True

                if self.MID_PRICE <= TRADING_OPERATION_['stop_losses'][0]:
                    CLOSE_TRADE=True
                    
            # STOP LOSS
            if OPERATION_SIDE_ == "SHORT":
                if self.MID_PRICE <= TRADING_OPERATION_['take_profits'][0]:
                    CLOSE_TRADE=True

                if self.MID_PRICE >= TRADING_OPERATION_['stop_losses'][0]:
                    CLOSE_TRADE=True
            
            if CLOSE_TRADE:
                if OPERATION_SIDE_ == "SHORT":
                    GAIN = (op[1]['entry_prices'][0] - self.MID_PRICE) * N_TOKEN_CONTRACT
                
                if OPERATION_SIDE_ == "LONG":
                    GAIN = (self.MID_PRICE - op[1]['entry_prices'][0]) * N_TOKEN_CONTRACT

                GAIN = GAIN - GAIN*self.TAKER_FEES
                EQUITY += GAIN
                CLOSED_TRADE_ID.append(ID_TRADE_)

            # delete order from filled book
            for id_operations in CLOSED_TRADE_ID:
                TRADE_ORDERBOOK = self.delete_operation_from_trading_book(id_operations)

            # apply running time trading datetime
            for op in TRADE_ORDERBOOK.items():
                ID_TRADE_ = op[0]
                TRADING_OPERATION_ = op[1]
                START_TIME = TRADING_OPERATION_['start_time']
                TRADING_OPERATION_['running_time'] =  datetime.now() - START_TIME                     
                TRADE_ORDERBOOK[ID_TRADE_] = TRADING_OPERATION_ 
                

            self.realized_pnl = self.equity - self.initial_capital
            self.equity_array.append(EQUITY)
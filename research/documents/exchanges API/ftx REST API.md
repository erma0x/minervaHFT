
place_order()

[input]
    market: str,
    side: str,
    price: float,
    size: float, 
    type: str = 'limit',
    reduce_only: bool = False,
    ioc: bool = False,
    post_only: bool = False,
    client_id: str = None,
    reject_after_ts: float = None
    
[output dict]
    'market': market,
    'side': side,
    'price': price,
    'size': size,
    'type': type,
    'reduceOnly': reduce_only,
    'ioc': ioc,
    'postOnly': post_only,
    'clientId': client_id,
    'rejectAfterTs': reject_after_ts



place_conditional_order()

[input]
    market: str,
    side: str,
    size: float,
    type: str = 'stop',
    limit_price: float = None,
    reduce_only: bool = False, 
    cancel: bool = True,
    trigger_price: float = None,
    trail_value: float = None

[output dict]
    'market': market,
    'side': side,
    'triggerPrice': trigger_price,
    'size': size,
    'reduceOnly': reduce_only,
    'type': 'stop',
    'cancelLimitOnTrigger': cancel,
    'orderPrice': limit_price
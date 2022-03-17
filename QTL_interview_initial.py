import json
import ccxt


class crypto_info:
    
    # Initializes crypto object to be interacted with
    def __init__(self, exchange_id : str) -> None:
        self.exchange   = getattr(ccxt, exchange_id)
        self.market     = None
        self.ticker     = None
        self.ohlc       = None


    def exchange_ticker (self):
        self.ticker     = json.dumps(self.exchange().fetch_ticker('KDA/USDT'), indent=2)



binance = crypto_info("binance")
print(binance.ticker) # Should be None

binance.exchange_ticker()
print(binance.ticker) # Should be full ticker
        
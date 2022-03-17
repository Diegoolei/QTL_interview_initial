import json
import ccxt


class crypto_info:
    
    # Initializes crypto object to be interacted with
    def __init__(self, exchange_id : str) -> None:
        self.exchange   = getattr(ccxt, exchange_id)
        self.market     = None
        self.ticker     = None
        self.ohlc       = None


    def exchange_ticker (self, crypto_a: str, crypto_b: str):
        if (crypto_a + "/" + crypto_b) in self.market:
            self.ticker     = json.dumps(self.exchange().fetch_ticker(crypto_a + "/" + crypto_b), indent=2)


    # Lists all available exchanges in ccxt
    def list_exchanges():
        for exchange in ccxt.exchanges: 
            print(exchange)


    # Available Currency trades in current exchange AND ITS INFO
    def update_exchange_market (self):
        self.market     = self.exchange().load_markets()


    # # Open-high-low-close values
    # def update_exchange_ohlc (self, crypto_a: str, crypto_b: str):
    #     if (crypto_a + "/" + crypto_b) in self.market:
    #         self.ohlc       = json.dumps(self.exchange().fetch_ohlcv(crypto_a + "/" + crypto_b), indent=2) 


binance = crypto_info("binance")

binance.update_exchange_market()

binance.exchange_ticker("ETH", "BTC")
print(binance.ticker) # Should be full ticker

# binance.update_exchange_ohlc("ETH", "BTC")
# print(binance.ohlc)
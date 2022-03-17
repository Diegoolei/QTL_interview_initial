import json
import ccxt


class exchange_info:
    
    # Initializes market object to be interacted with
    def __init__(self, exchange_id : str) -> None:
        self.exchange   = getattr(ccxt, exchange_id)
        self.market     = self.exchange().load_markets()
        self.crypto_a   = None
        self.crypto_b   = None

    def crypto_check(self):
        return (self.crypto_a and self.crypto_b)


    # Lists all available exchanges in ccxt
    def list_exchanges(self):
        for exchange in ccxt.exchanges: 
            print(exchange)

    def update_exchange(self, exchange_id : str) -> None:
        self.exchange   = getattr(ccxt, exchange_id)
        self.market     = self.exchange().load_markets()
        self.crypto_a_b   = None
        self.crypto_b_a   = None


    # Available Currency trades in current exchange AND ITS INFO
    def update_exchange_market (self):
        self.market = self.exchange().load_markets()



class crypto_info:
    def __init__(self, exchange: exchange_info, crypto_a : str, crypto_b : str) -> None:
        self.market = exchange.market
        self.crypto_a: str = crypto_a   #Crypto shorted names
        self.crypto_b: str = crypto_b   #
        self.valid_market  = False      #Valid only if market extists in exchange
        self.ticker     = None

    def crypto_ticker (self) -> None:
        if (self.ticker_a + "/" + self.ticker_b) in self.market:
            self.ticker = json.dumps(self.exchange().fetch_ticker(
                                        self.crypto_a + "/" + self.crypto_b), indent=4
                                        )
        else:
            self.ticker = None


binance = exchange_info("binance")

binance.update_exchange_market()

binance.exchange_ticker()
print(binance.ticker) # Should be full ticker

import json

import ccxt


class exchange_info:

    # Initializes market object to be interacted with
    def __init__(self, exchange_id: str) -> None:
        self.exchange = getattr(ccxt, exchange_id)
        self.market = self.exchange().load_markets()

    def crypto_check(self):
        return (self.crypto_a and self.crypto_b)

    # Lists all available exchanges in ccxt

    def list_exchanges(self):
        for exchange in ccxt.exchanges:
            print(exchange)

    def update_exchange(self, exchange_id: str) -> None:
        self.exchange = getattr(ccxt, exchange_id)
        self.market = self.exchange().load_markets()

    # Available Currency trades in current exchange AND ITS INFO

    def update_exchange_market(self):
        self.market = self.exchange().load_markets()


class crypto_info:
    def __init__(self, exchange_info: exchange_info, crypto_a: str, crypto_b: str) -> None:
        self.exchange_info: exchange_info = exchange_info
        self.crypto_a: str = crypto_a  # Crypto shorted names
        self.crypto_b: str = crypto_b   #
        self.valid_market = False  # Valid only if market extists in exchange
        self.ticker = None

    def get_crypto_ticker(self) -> None:
        if (self.crypto_a + "/" + self.crypto_b) in self.exchange_info.market:
            self.ticker = json.dumps(self.exchange_info.exchange().fetch_ticker(
                self.crypto_a + "/" + self.crypto_b), indent=4
            )
        else:
            self.ticker = None

    def get_crypto_ask_bid(self) -> str:
        return self.ticker["ask"]


binance = exchange_info("binance")

ETH_BTC = crypto_info(binance, "ETH", "BTC")

ETH_BTC.get_crypto_ticker()

print(ETH_BTC.get_crypto_ask_bid())  # Should be full ticker

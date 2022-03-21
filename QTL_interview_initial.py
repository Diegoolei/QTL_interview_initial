from datetime import datetime
import ccxt
from time import sleep

import pprint
pp = pprint.PrettyPrinter(indent=0)


def list_exchanges() -> None:
    """Lists all available exchanges in ccxt."""
    for exchange in ccxt.exchanges:
        print(exchange)


class exchange_info:

    def __init__(self, exchange_id: str) -> None:
        """Initializes exchange object to be interacted with"""
        self.exchange = getattr(ccxt, exchange_id)
        self.market = self.exchange().load_markets()

    def __str__(self) -> str:
        """Instance Description"""
        return f"Current exchange: {self.exchange()}"

    def update_exchange(self, exchange_id: str) -> None:
        """Updates instance exchange"""
        self.exchange = getattr(ccxt, exchange_id)
        self.market = self.exchange().load_markets()

    def update_exchange_market(self) -> None:
        """Updates instance market"""
        # Available Currency trades in current exchange AND ITS INFO
        self.market = self.exchange().load_markets()

    def print_markets(self) -> None:
        """Lists reverse sorted list of all available markets in current exchange"""
        sorted_market = sorted(self.market.keys(), reverse=True)
        for market in sorted_market:
            print(market)


class market_info:
    def __init__(self, exchange_info: exchange_info, crypto_a: str, crypto_b: str) -> None:
        """Initializes market object to be interacted with"""
        self.exchange_info = exchange_info
        self.crypto_a: str = crypto_a.upper()  # Crypto symbol in capital letters
        self.crypto_b: str = crypto_b.upper()  #
        # True only if market extists in exchange
        self.__valid_market = self.check_valid_market()
        self.last_orderbook = None
        if not self.__valid_market:
            print(f"{self.crypto_a}/{self.crypto_b} is not a valid market")

    def __str__(self) -> str:
        """Crypto market Symbols"""
        if self.__valid_market:
            return f"{self.crypto_a}/{self.crypto_b}"
        else:
            return("Please define a valid market before trying to get crypto symbols")

    def check_valid_market(self) -> bool:
        """True only if market extists in exchange"""
        return (self.crypto_a.upper() + "/" + self.crypto_b.upper()) in self.exchange_info.market

    def update_market_orderbook(self) -> None:
        """Updates instance orderbook if market is valid"""
        if self.__valid_market:
            self.last_orderbook = self.exchange_info.exchange().fetch_order_book(
                self.crypto_a + "/" + self.crypto_b
            )
        else:
            print("Please define a valid market before trying to update the ORDERBOOK")

    def get_orderbook_info(self, info: str) -> str:
        """Returns "info" parameter of the orderbook if market is valid and the orderbook is not None"""
        if self.__valid_market and self.last_orderbook[info] and len(self.last_orderbook[info]) > 0:
            return self.last_orderbook.get(info, info + "is not defined in the ORDERBOOK, please specify a valid one before trying to get orderbook info")
        else:
            return "Please define a valid market before trying to get ORDERBOOK info"


binance = exchange_info("binance")
btc_usdt = market_info(binance, "btc", "usdt")
eth_usdt = market_info(binance, "eth", "usdt")

t_delay = 2  # seconds

while True:
    btc_usdt.update_market_orderbook()
    # bids structure: 'bids': [ [ price, amount ], ... , []]
    btc_bid = btc_usdt.get_orderbook_info("bids")[0][0]
    # ask structure: 'asks': [ [ price, amount ], ... , []]
    btc_ask = btc_usdt.get_orderbook_info("asks")[0][0]

    eth_usdt.update_market_orderbook()
    eth_bid = eth_usdt.get_orderbook_info("bids")[0][0]
    eth_ask = eth_usdt.get_orderbook_info("asks")[0][0]

    btc_eth_ratio = float(btc_bid)/float(eth_ask)
    eth_btc_ratio = float(eth_bid)/float(btc_ask)

    print("")
    pp.pprint(btc_usdt.__str__() + ", " + eth_usdt.__str__())
    print("")

    print("Date/time:", datetime.now())

    print(binance)

    print("BTC/ETH ratio:", btc_eth_ratio)
    print("ETH/BTC ratio:", eth_btc_ratio)
    print("--------------------------------")

    sleep(t_delay)  # rate limit

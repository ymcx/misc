import sys
from yfinance import Ticker


def get_price(ticker: str) -> str:
    price = Ticker(ticker).fast_info.last_price
    return f"{price:.2f}"


def get_output(tickers: list[str]) -> str:
    prices = [get_price(ticker) for ticker in tickers]
    n = max(len(price) for price in prices)
    return "\n".join(f"{price:>{n}} {ticker}" for price, ticker in zip(prices, tickers))


def main() -> None:
    tickers = sys.argv[1:]
    output = get_output(tickers)
    print(output)


if __name__ == "__main__":
    main()

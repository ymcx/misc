def _starts_with_dollar(string: str) -> bool:
    return string.startswith("$")


def _is_uppercase(string: str) -> bool:
    return string.isupper()


def _contains_no_numbers(string: str) -> bool:
    return string.isalpha()


def tickers(string: str) -> list[str]:
    tickers = string.split()
    tickers = [i for i in tickers if _starts_with_dollar(i) or _is_uppercase(i)]
    tickers = [i for i in tickers if _contains_no_numbers(i)]

    return tickers

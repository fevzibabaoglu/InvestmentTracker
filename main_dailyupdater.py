import sys

from portfolio import FundPortfolio


def main(portfolioName: str):
    portfolio = FundPortfolio(portfolioName)
    portfolio.loadFromJson()
    portfolio.dailyChangeUpdate()
    portfolio.saveToJson()


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        raise Exception("Not enough arguments: Portfolio name must be given.")

    main(args[0])

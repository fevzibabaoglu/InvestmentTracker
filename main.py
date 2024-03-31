from portfolio import FundPortfolio


def main():
    portfolio = FundPortfolio('yapikredi')

    # portfolio.addFund('ykt')
    # portfolio.addFund('yas')
    # portfolio.addFund('yay')
    # portfolio.addFund('ybe')
    # portfolio.loadFundsFromWeb()
    # portfolio.saveToJson()

    portfolio.loadFromJson()
    portfolio.dailyChangeUpdate()
    portfolio.saveToJson()

    # print(portfolio)
    # print(portfolio.getTotalShares())
    # print(portfolio.getTotalProfit())
    # print(portfolio.getTotalBoughtSharePrice())


        
if __name__ == "__main__":
    main()

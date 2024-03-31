import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode
from typing import Union


URL = 'https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod='
PERCENTAGE_MOD = 10


class Fund:
    def __init__(self, code: str) -> None:
        self.code = code.upper()
        self.label = ''
        self.price = 0.0
        self.date = ''
        self.changes: list[FundChange] = []

    def __call__(self) -> dict[str, Union[str, float, list[dict[str, Union[int, float]]]]]:
        return {
            'code': self.code,
            'label': self.label,
            'price': round(self.price, 6),
            'profit': round(self.getTotalProfit(), 6),
            'profitPercentage': round(self.getProfitPercentage() * 100, 6),
            'date': self.date,
            'changes': [change() for change in self.changes],
        }
    
    def __str__(self) -> str:
        return json.dumps(self(), indent=2, sort_keys=False, ensure_ascii=False)

    @staticmethod
    def getWebData(code: str) -> dict[str, Union[str, float]]:
        url = f"{URL}{code.upper()}"   
        response = requests.get(url=url)

        if response.status_code != 200:
            raise Exception(f"Request error (code:{response.status_code}) while requesting from {url}")

        soup = BeautifulSoup(response.content, 'html.parser')

        content_label = soup.find(attrs={'id': 'MainContent_FormViewMainIndicators_LabelFund'})
        content_topList = soup.find(attrs={'class': 'top-list'})
        content_priceIndicators = soup.find(attrs={'class': 'price-indicators'})

        li_topList = {li.contents[0]: li.span.string for li in content_topList.find_all('li')}
        li_priceIndicators = {li.contents[0]: li.span.string for li in content_priceIndicators.find_all('li')}

        data = {
            'label': unidecode(content_label.string),
            'price': float(li_topList['Son Fiyat (TL)'].replace(',', '.')),
            'oneMonthProfitPercentage': float(li_priceIndicators['Son 1 Ay Getirisi'].replace(',', '.').strip('%')),
            'threeMonthsProfitPercentage': float(li_priceIndicators['Son 3 Ay Getirisi'].replace(',', '.').strip('%')),
            'sixMonthsProfitPercentage': float(li_priceIndicators['Son 6 Ay Getirisi'].replace(',', '.').strip('%')),
            'oneYearProfitPercentage': float(li_priceIndicators['Son 1 Yıl Getirisi'].replace(',', '.').strip('%')),
        }
        return data

    def updateShares(self, shareChange: int) -> None:
        self.dailyChangeUpdate()
        changeToday = self.changes[-1]
        changeToday.shareChange += shareChange 

    def getTotalShares(self) -> int:
        return sum(change.shareChange for change in self.changes)

    def getTotalProfit(self) -> float:
        return sum(self.getProfitList())
    
    def getProfitList(self) -> list[float]:
        profits = []
        share = 0

        for change in self.changes:
            profits.append(share * change.priceChange)
            share += change.shareChange

        return profits
    
    def getProfitPercentage(self) -> float:
        totalBoughtSharePrice = self.getTotalBoughtSharePrice()

        if totalBoughtSharePrice == 0:
            return 0.0

        return self.getTotalProfit() / totalBoughtSharePrice * 100
    
    def getTotalBoughtSharePrice(self) -> float:
        price = self.price
        totalPrice = 0

        for change in self.changes:
            price += change.priceChange
            totalPrice += change.shareChange * price

        return totalPrice
    
    def getTotalValue(self) -> float:
        valueList = self.getValueList()

        if len(valueList) == 0:
            return 0.0

        return valueList[-1]

    def getValueList(self) -> list[float]:
        values = []
        price = self.price
        share = 0

        for change in self.changes:
            price += change.priceChange
            share += change.shareChange
            values.append(share * price)

        return values

    def dailyChangeUpdate(self) -> None:
        dateStart = datetime.strptime(self.date.split("_")[0], "%Y-%m-%d")
        dayDifference = (datetime.now() - dateStart).days

        if len(self.changes) != 0 and dayDifference == self.changes[-1].daySinceStart:
            return

        webData = Fund.getWebData(self.code)
        lastPrice = self.price + sum(change.priceChange for change in self.changes)
        priceDifference = webData['price'] - lastPrice
        priceDifferencePercentage = priceDifference / lastPrice * 100

        dailyChange = FundChange()
        dailyChange.daySinceStart = dayDifference
        dailyChange.priceChange = priceDifference
        dailyChange.profitPercentageSinceLastChange = priceDifferencePercentage

        if dayDifference % PERCENTAGE_MOD == 0:
            dailyChange.oneMonthProfitPercentage = webData['oneMonthProfitPercentage']
            dailyChange.threeMonthsProfitPercentage = webData['threeMonthsProfitPercentage']
            dailyChange.sixMonthsProfitPercentage = webData['sixMonthsProfitPercentage']
            dailyChange.oneYearProfitPercentage = webData['oneYearProfitPercentage']
        
        self.changes.append(dailyChange)

    def loadFromWeb(self) -> None:
        webData = Fund.getWebData(self.code)
        self.label = webData['label']
        self.price = webData['price']
        self.date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.dailyChangeUpdate()
    
    def loadFromJsonData(self, jsonLoadData) -> None:
        if self.code != jsonLoadData['code']:
            raise Exception(f"Codes does not match")
        
        self.label = jsonLoadData['label']
        self.price = jsonLoadData['price']
        self.date = jsonLoadData['date']
        
        for changeJson in jsonLoadData['changes']:
            change = FundChange()
            change.loadFromJsonData(changeJson)
            self.changes.append(change)
    

class FundChange:
    def __init__(self) -> None:
        self.daySinceStart = 0
        self.priceChange = 0.0
        self.shareChange = 0
        self.profitPercentageSinceLastChange = 0.0
        self.oneMonthProfitPercentage = 0.0
        self.threeMonthsProfitPercentage = 0.0
        self.sixMonthsProfitPercentage = 0.0
        self.oneYearProfitPercentage = 0.0

    def __call__(self) -> dict[str, Union[int, float]]:
        fundChangeJson = {
            'daySinceStart': self.daySinceStart,
            'priceChange': round(self.priceChange, 6),
            'shareChange': self.shareChange,
            'profitPercentageSinceLastChange': round(self.profitPercentageSinceLastChange, 6),
        }

        if self.daySinceStart % PERCENTAGE_MOD == 0:
            fundChangeJson.update({
                'oneMonthProfitPercentage': round(self.oneMonthProfitPercentage, 6),
                'threeMonthsProfitPercentage': round(self.threeMonthsProfitPercentage, 6),
                'sixMonthsProfitPercentage': round(self.sixMonthsProfitPercentage, 6),
                'oneYearProfitPercentage': round(self.oneYearProfitPercentage, 6),
            })

        return fundChangeJson

    def __str__(self) -> str:
        return json.dumps(self(), indent=2, sort_keys=False, ensure_ascii=False)
    
    def loadFromJsonData(self, jsonLoadData) -> None:
        self.daySinceStart = jsonLoadData['daySinceStart']
        self.priceChange = jsonLoadData['priceChange']
        self.shareChange = jsonLoadData['shareChange']
        self.profitPercentageSinceLastChange = jsonLoadData['profitPercentageSinceLastChange']

        if self.daySinceStart % PERCENTAGE_MOD == 0:
            self.oneMonthProfitPercentage = jsonLoadData['oneMonthProfitPercentage']
            self.threeMonthsProfitPercentage = jsonLoadData['threeMonthsProfitPercentage']
            self.sixMonthsProfitPercentage = jsonLoadData['sixMonthsProfitPercentage']
            self.oneYearProfitPercentage = jsonLoadData['oneYearProfitPercentage']

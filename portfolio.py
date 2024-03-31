import json
import os
from typing import Union

from fund import Fund


JSON_FOLDER_PATH = 'json'


class FundPortfolio:
    def __init__(self, name: str) -> None:
        self.name = name
        self.funds: dict[str, Fund] = {}

    def __call__(self) -> dict[str, Union[str, float, dict[str, Fund]]]:
        return {
            'name': self.name,
            'profit': round(self.getTotalProfit(), 6),
            'profitPercentage': round(self.getTotalProfitPercentage(), 6),
            'funds': {code: fund() for code, fund in self.funds.items()},
        }
    
    def __str__(self) -> str:
        return json.dumps(self(), indent=2, sort_keys=False, ensure_ascii=False)

    def addFund(self, code: str) -> None:
        self.funds.update({code.lower(): Fund(code)})

    def getTotalShares(self) -> int:
        return sum(fund.getTotalShares() for fund in self.funds.values())

    def getTotalProfit(self) -> float:
        return sum(fund.getProfit() for fund in self.funds.values())
        
    def getTotalProfitPercentage(self) -> float:
        totalBoughtSharePrice = self.getTotalBoughtSharePrice()

        if totalBoughtSharePrice == 0:
            return 0.0

        return self.getTotalProfit() / totalBoughtSharePrice * 100
    
    def getTotalBoughtSharePrice(self) -> float:
        return sum(fund.getTotalBoughtSharePrice() for fund in self.funds.values())

    def dailyChangeUpdate(self) -> None:
        for fund in self.funds.values():
            fund.dailyChangeUpdate()

    def loadFundsFromWeb(self) -> None:
        for fund in self.funds.values():
            fund.loadFromWeb()

    def loadFromJson(self) -> None:
        filename = f"{JSON_FOLDER_PATH}/portfolio_{self.name}.json"

        if not os.path.exists(filename):
            raise Exception(f"Error while loading portfolio '{self.name}' from json: '{filename}' file does not exist.")
        
        with open(filename, 'r') as jsonFile:
            loadedData = json.load(jsonFile)

            self.name = loadedData['name']

            for code, fund in loadedData['funds'].items():
                self.addFund(code)
                self.funds[code].loadFromJsonData(fund)

    def saveToJson(self) -> None:
        filename = f"{JSON_FOLDER_PATH}/portfolio_{self.name}.json"

        if not os.path.exists(JSON_FOLDER_PATH):
            os.makedirs(JSON_FOLDER_PATH)

        with open(filename, 'w') as jsonFile:
            json.dump(self(), jsonFile, indent=4)

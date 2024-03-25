import json
import requests
from bs4 import BeautifulSoup
from typing import Any, Union


URL = 'https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod='


class Fund:
    def __init__(self, code: str) -> None:
        self.code = code.upper()
        self.label = ''
        self.price = 0.0
        self.oneDayProfitPercentage = 0.0
        self.oneMonthProfitPercentage = 0.0
        self.threeMonthsProfitPercentage = 0.0
        self.sixMonthsProfitPercentage = 0.0
        self.oneYearProfitPercentage = 0.0

        self.getFundInfo()

    def __call__(self) -> dict[str, Union[str, float]]:
        return {
            'code': self.code,
            'label': self.label,
            'price': self.price,
            'oneDayProfitPercentage': self.oneDayProfitPercentage,
            'oneMonthProfitPercentage': self.oneMonthProfitPercentage,
            'threeMonthsProfitPercentage': self.threeMonthsProfitPercentage,
            'sixMonthsProfitPercentage': self.sixMonthsProfitPercentage,
            'oneYearProfitPercentage': self.oneYearProfitPercentage,
        }
    
    def __str__(self) -> str:
        return json.dumps(self.__call__(), indent=2, sort_keys=False, ensure_ascii=False)

    def getFundInfo(self) -> None:
        url = f"{URL}{self.code}"
        response = requests.get(url=url)

        if response.status_code != 200:
            raise Exception(f"Request error (code:{response.status_code}) while requesting from {url}")

        soup = BeautifulSoup(response.content, 'html.parser')

        content_label = soup.find(attrs={'id': 'MainContent_FormViewMainIndicators_LabelFund'})
        content_topList = soup.find(attrs={'class': 'top-list'})
        content_priceIndicators = soup.find(attrs={'class': 'price-indicators'})

        li_topList = {li.contents[0]: li.span.string for li in content_topList.find_all('li')}
        li_priceIndicators = {li.contents[0]: li.span.string for li in content_priceIndicators.find_all('li')}

        self.label = content_label.string
        self.price = float(li_topList['Son Fiyat (TL)'].replace(',', '.'))
        self.oneDayProfitPercentage = float(li_topList['Günlük Getiri (%)'].replace(',', '.').strip('%'))
        self.oneMonthProfitPercentage = float(li_priceIndicators['Son 1 Ay Getirisi'].replace(',', '.').strip('%'))
        self.threeMonthsProfitPercentage = float(li_priceIndicators['Son 3 Ay Getirisi'].replace(',', '.').strip('%'))
        self.sixMonthsProfitPercentage = float(li_priceIndicators['Son 6 Ay Getirisi'].replace(',', '.').strip('%'))
        self.oneYearProfitPercentage = float(li_priceIndicators['Son 1 Yıl Getirisi'].replace(',', '.').strip('%'))

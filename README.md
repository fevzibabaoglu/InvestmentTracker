---
# InvestmentTracker

A basic fund tracking program that can be used in Turkey.

---

The program retrieves data for the specified fund codes from the web and stores it in JSON format. 
Additionally, you can utilize the 'main_dailyupdater.py' script in conjunction with a task scheduler to automatically update the data on a daily basis.

---

The data is taken from [TEFAS](https://www.tefas.gov.tr).

---

Example JSON file:

```json
{
    "name": "testPortfolio",
    "profit": 123.456789,
    "profitPercentage": 1.234567,
    "funds": {
        "testFund1": {
            "code": "TESTFUND1",
            "label": "TEST FUND 1",
            "price": 0.123456,
            "profit": 123.456789,
            "profitPercentage": 1.234567,
            "date": "2024-03-31_17-06-40",
            "changes": [
                {
                    "daySinceStart": 0,
                    "priceChange": 0.0,
                    "shareChange": 12345,
                    "profitPercentageSinceLastChange": 0.0,
                    "oneMonthProfitPercentage": 12.345678,
                    "threeMonthsProfitPercentage": 23.456789,
                    "sixMonthsProfitPercentage": 34.567890,
                    "oneYearProfitPercentage": 45.678901
                },
                {
                    "daySinceStart": 1,
                    "priceChange": 0.012345,
                    "shareChange": 123,
                    "profitPercentageSinceLastChange": 1.234567
                }
            ]
        },
        "testFund2": {
            "code": "TESTFUND2",
            "label": "TEST FUND 2",
            "price": 0.123456,
            "profit": 123.456789,
            "profitPercentage": 1.234567,
            "date": "2024-03-31_17-06-40",
            "changes": [
                {
                    "daySinceStart": 0,
                    "priceChange": 0.0,
                    "shareChange": 12345,
                    "profitPercentageSinceLastChange": 0.0,
                    "oneMonthProfitPercentage": 12.345678,
                    "threeMonthsProfitPercentage": 23.456789,
                    "sixMonthsProfitPercentage": 34.567890,
                    "oneYearProfitPercentage": 45.678901
                },
                {
                    "daySinceStart": 1,
                    "priceChange": 0.012345,
                    "shareChange": 123,
                    "profitPercentageSinceLastChange": 1.234567
                }
            ]
        }
    }
}
```

---

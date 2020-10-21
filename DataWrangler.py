from datetime import date
import requests
import os
import json

# pulls minutely data from up to the last 30 days on a given list of stocks from
# the IEX API and writes it to a folder containing a .json file for each stock
# example call:
# stockList = ["aapl", "tsla", "z"]
# DataWrangler(stockList, 5, "YOUR API KEY")
class DataWrangler:
    # constructor
    # @param stocks - a list of stock tickers to get data from (tickers must be lowercase)
    # @param days   - how many trailing days you want data for (can be between 1 and 30)
    # @param token  - IEX api token
    def __init__(self, stocks, days, token):
        self.stocks = stocks
        self.days = days
        self.baseURL = "https://cloud.iexapis.com/stable"
        self.queryParameter = "?token=" + token
        self.responses = []
        os.mkdir(os.getcwd() + "/Stocks")
        for stock in stocks:
            self.pull(stock)

    # pulls the individual data from IEX
    # @param stock - stock to get data on
    def pull(self, stock):
        today = int(date.today().strftime("%Y%m%d").replace('-', ''))
        weekday = date.today().weekday() - 1
        dates = []
        i = 0
        j = 0
        while i < self.days:
            if (weekday < 5):
                dates.append(today-j-1)
            else:
                i = i - 1
            weekday = weekday - 1
            i = i + 1
            j = j + 1
            if (weekday < 0):
                weekday = 6
        with open(os.getcwd() + "/Stocks/" + stock + ".json", 'w') as f:
            data = ""
            for day in dates:
                data = data + requests.get(self.baseURL + "/stock/" + stock + "/chart/date/" + str(day) + self.queryParameter).text[1:-1] + ","
            file = json.loads("["+data[:-1]+"]")
            json.dump(file, f)

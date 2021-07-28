# this is the "app/robo_advisor.py" file
import csv
import json
import os
from dotenv import load_dotenv
import requests
from pandas import DataFrame
import plotly.express as px
from pprint import pprint
from datetime import datetime

load_dotenv

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# ask for user input 
symbol = str.strip(input("Please choose a stock ticker to search (i.e. MSFT):"))  #TODO: accept user input

# Validate a user input

# INFO INPUTS
#
api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 



stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
response = requests.get(stock_url)
parsed_response = json.loads(response.text)

records = []
for date, daily_data in parsed_response["Time Series (Daily)"].items():
    record = {
        "date": date,
        "open": float(daily_data["1. open"]),
        "high": float(daily_data["2. high"]),
        "low": float(daily_data["3. low"]),
        "close": float(daily_data["4. close"]),
        "volume": int(daily_data["5. volume"]),
    }
    records.append(record)

df = DataFrame(records)
# last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# 
# tsd = parsed_response["Time Series (Daily)"]
# 
# dates = list(tsd.keys()) #TODO: assumes first day is on top, sort to ensure latest is first
# 
# latest_day = dates[0]
# 
# lastest_close = tsd[latest_day]["4. close"]
# 
# high_prices = []
# low_prices = []
# 
# for date in dates:
#     high_price = tsd[date]["2. high"]
#     high_prices.append(float(high_price))    
#     low_price = tsd[date]["3. low"]
#     low_prices.append(float(low_price))
# 
# recent_high = max(high_prices)
# recent_low = min(low_prices)

#
# INFO INPUTS
#

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["6. volume"]
        })

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
# code for datetime = https://www.geeksforgeeks.org/get-current-date-using-python/

print(f"REQUEST AT: {datetime.now()}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(lastest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


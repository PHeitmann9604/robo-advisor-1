# this is the "app/robo_advisor.py" file
import csv
import json
import os

import requests

from pprint import pprint
from datetime import datetime
from getpass import getpass

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
#
# INFO INPUTS
#

stock_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo"
response = requests.get(stock_url)
parsed_response = json.loads(response.text)
pprint(parsed_response)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) #TODO: assumes first day is on top, sort to ensure latest is first

latest_day = dates[0]

lastest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))    
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#
# INFO INPUTS
#

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader()
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
# code for datetikme = https://www.geeksforgeeks.org/get-current-date-using-python/

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


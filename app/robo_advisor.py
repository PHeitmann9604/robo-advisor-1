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
symbol = str.strip(input("Please choose a stock ticker to search (e.g. MSFT):"))
# symbol1, symbol2 = str.strip(input("Please choose a stock ticker to search (i.e. MSFT):")).split()
if symbol.isnumeric() or len(symbol) > 5:
    print("INVALID INPUT")
        exit()
else:
    print(f"Looking up data for: {symbol}")
# Validate a user input


api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 

stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
response = requests.get(stock_url)
parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

records = []
for date, daily_data in tsd.items():
     record = {
         "date": date,
         "open": to_usd(float(daily_data["1. open"])),
         "high": to_usd(float(daily_data["2. high"])),
         "low": to_usd(float(daily_data["3. low"])),
         "close": to_usd(float(daily_data["4. close"])),
         "volume": int(daily_data["6. volume"]),
     }
     records.append(record)
 
df = DataFrame(records)
 
 


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
# EXPORT TO CSV

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
df.to_csv(csv_file_path)


# csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
# 
# csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
# with open(csv_file_path, "w") as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
#     writer.writeheader()
#     for date in dates:
#         daily_prices = tsd[date]
#         writer.writerow({
#             "timestamp": date,
#             "open": daily_prices["1. open"],
#             "high": daily_prices["2. high"],
#             "low": daily_prices["3. low"],
#             "close": daily_prices["4. close"],
#             "volume": daily_prices["6. volume"]
#         })
# 
print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
# code for datetime = https://www.geeksforgeeks.org/get-current-date-using-python/

print(f"REQUEST AT: {datetime.now()}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: ", records[0]["close"])
print("RECENT HIGH: ", df["high"].max())
print("RECENT LOW: ", df["low"].min())
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

# CHART PRICES OVER TIME

fig = px.line(df, y="close", x="date", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
fig.update_yaxes(autorange="reversed")
fig.show()
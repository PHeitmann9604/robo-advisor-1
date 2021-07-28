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

# Validate a user input


print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")

api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
try:
    stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
    response = requests.get(stock_url)
    parsed_response = json.loads(response.text)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    tsd = parsed_response["Time Series (Daily)"]
except:
    print("INVALID ticker. Please run the program again with a valid ticker symbol")
    exit()
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
 
 #
# INFO INPUTS
#
# EXPORT TO CSV

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
df.to_csv(csv_file_path)

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
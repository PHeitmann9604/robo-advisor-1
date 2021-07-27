# this is the "app/robo_advisor.py" file

from pprint import pprint
import requests
import json
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
lastest_close = parsed_response["Time Series (Daily)"]["2021-07-26"]["4. close"]
recent_high = parsed_response["Time Series (Daily)"]["2021-07-26"]["2. high"]
recent_low = parsed_response["Time Series (Daily)"]["2021-07-26"]["3. low"] 
#
# INFO INPUTS
#

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(lastest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
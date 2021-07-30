# this is the "app/robo_advisor.py" file
import csv
import json
import os
from dotenv import load_dotenv
import requests
from pandas import DataFrame
import plotly.express as px
from pprint import pprint
import datetime
import statistics

load_dotenv

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

data_choice = str.strip(input("Please choose between stocks or crypto:"))
if data_choice == "stocks" or data_choice == "crypto":
    print(f"REQUESTING {data_choice} DATA...")
else:
    print("INVALID CHOICE. Please selected either stocks or crypto data")
    data_choice = str.strip(input("Please choose between stocks or crypto:"))
# ask for user input 
if data_choice == "stocks":
    symbol = str.strip(input("Please choose a stock ticker to search (e.g. MSFT):"))
    # symbol1, symbol2 = str.strip(input("Please choose a stock ticker to search (i.e. MSFT):")).split()

    # Validate a user input
    if symbol.isnumeric() or len(symbol) > 5:
        print("INVALID INPUT")
        exit()
    else:
        print("-------------------------")
        print(f"SELECTED SYMBOL: {symbol}")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
    # try except source: https://www.w3schools.com/python/python_try_except.asp
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
             "open": float(daily_data["1. open"]),
             "high": float(daily_data["2. high"]),
             "low": float(daily_data["3. low"]),
             "close": float(daily_data["5. adjusted close"]),
             "volume": int(daily_data["6. volume"]),
         }
         records.append(record)
    
    df = DataFrame(records)
    
    #
    # INFO INPUTS
    #
    # EXPORT TO CSV

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol}_prices.csv")
    df.to_csv(csv_file_path)

    # code for datetime = https://www.geeksforgeeks.org/get-current-date-using-python/
    now = datetime.datetime.now().strftime("%H:%M%p on %B %d, %Y")
    print(type(date))
    print(f"REQUEST AT: {now}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print("LATEST CLOSE: ", to_usd(records[0]["close"]))
    print("RECENT HIGH: ", to_usd(df["high"].max()))
    print("RECENT LOW: ", to_usd(df["low"].min()))
    print("-------------------------")
    buy_test = df["low"].min() * 1.10
    if float(records[0]["close"]) < float(buy_test): 
        print("RECOMMENDATION: BUY")
    else: 
         print("RECOMMENDATION: SELL")
    print("RECOMMENDATION REASON:The most recent closing price of", to_usd(float(records[0]["close"])), "is compared to the 10 percent above the recent low", to_usd(float(buy_test)))
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}...")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    # CHART PRICES OVER TIME
    sorted_close = sorted("close")
    fig = px.line(df, y="close", x="date", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
    fig.show()
else:
    symbol = str.strip(input("Please choose a crypto currency to search (e.g.BTC):"))
    # symbol1, symbol2 = str.strip(input("Please choose a stock ticker to search (i.e. MSFT):")).split()

    # Validate a user input
    if symbol.isnumeric() or len(symbol) > 5:
        print("INVALID INPUT")
        exit()
    else:
        print("-------------------------")
        print(f"SELECTED SYMBOL: {symbol}")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
    # try except source: https://www.w3schools.com/python/python_try_except.asp
    try:
        crypto_url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={api_key}"
        response = requests.get(crypto_url)
        parsed_response = json.loads(response.text)

        last_refreshed = parsed_response["Meta Data"]["6. Last Refreshed"]

        tsd = parsed_response["Time Series (Digital Currency Daily)"]
    except:
        print("INVALID crypto currency. Please run the program again with a valid crypto currency")
        exit()
    records = []
    for date, daily_data in tsd.items():
         record = {
             "date": date,
             "open": float(daily_data["1b. open (USD)"]),
             "high": float(daily_data["2b. high (USD)"]),
             "low": float(daily_data["3b. low (USD)"]),
             "close": float(daily_data["4b. close (USD)"]),
             "volume": daily_data["5. volume"],
         }
         records.append(record)
    
    df = DataFrame(records)
    
    #
    # INFO INPUTS
    #
    # EXPORT TO CSV

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol}_prices.csv")
    df.to_csv(csv_file_path)

    # code for datetime = https://www.geeksforgeeks.org/get-current-date-using-python/

    now = datetime.datetime.now().strftime("%H:%M%p on %B %d, %Y")
    print(f"REQUEST AT: {now}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print("LATEST CLOSE: ", to_usd(records[0]["close"]))
    print("RECENT HIGH: ", to_usd(df["high"].max()))
    print("RECENT LOW: ", to_usd(df["low"].min()))
    print("-------------------------")
    buy_test = df["low"].min() * 1.10
    if float(records[0]["close"]) < float(buy_test):  
        print("RECOMMENDATION: BUY")
    else: 
         print("RECOMMENDATION: SELL")
    print("RECOMMENDATION REASON:The most recent closing price of", to_usd(float(records[0]["close"])), "is compared to the ten day average price of", to_usd(float(buy_test)))
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}...")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    # CHART PRICES OVER TIME

    fig = px.line(df, y="close", x="date", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
    fig.show()
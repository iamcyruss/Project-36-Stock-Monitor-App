import os
import requests
import datetime
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
TICKER_DATA_API = os.environ.get("TICKER_DATA_API")
TICKER_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_DATA_API = os.environ.get("NEWS_DATA_API")
SMS_ACCOUNT_SID = os.environ.get("SMS_ACCOUNT_SID")
SMS_AUTH_TOKEN = os.environ.get("SMS_AUTH_TOKEN")
FROM_ = +19474652240
TICKER_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": TICKER_DATA_API,
}
current_date = datetime.now()
print(current_date.today())
today = str(current_date.today()).split()
yesterday = str(current_date - timedelta(1)).split()
print(today)
print(yesterday)

ticker_response = requests.get(TICKER_ENDPOINT, params=TICKER_PARAMS)
ticker_response.raise_for_status()
ticker_data = ticker_response.json()["Time Series (Daily)"]
print(ticker_data)
print(ticker_data[today[0]])
print(ticker_data[yesterday[0]])

print(TICKER_PARAMS)
print(f"ACCOUNT: {SMS_ACCOUNT_SID} and AUTH: {SMS_AUTH_TOKEN}")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


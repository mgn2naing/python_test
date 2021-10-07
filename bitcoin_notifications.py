import requests
import time
from datetime import datetime
import json

from requests.api import post
BITCOIN_PRICE_THRESHOLD = 10000
BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start':'1',
    'limit':'1',
    'convert':'USD'
}
head_data = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY':'33e2166a-2c67-4ebb-a01a-b8d4245a1248'
}
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/d1RpBX3HjoUgDllivCPzZg'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL, params=parameters, headers=head_data)
    response_dict = response.json()
    return float((response_dict["data"][0]['quote']['USD']['price']))

def post_ifttt_webhook(event, value):
    data = {'Value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)
        
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            bitcoin_history = []
        
        time.sleep(5 * 60)

if __name__ == '__main__':
    main()

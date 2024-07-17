# price_fetcher/fetch_prices.py
import os
import time
import requests
import psycopg2
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL')

def fetch_and_store_price():
    try:
        response = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
        data = response.json()
        price = data['data']['amount']
        timestamp = datetime.utcnow()

        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prices (timestamp, price) VALUES (%s, %s)",
            (timestamp, price)
        )
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error fetching or storing price: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_store_price()
        time.sleep(60)  # Fetch every minute


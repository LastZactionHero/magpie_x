# TODO:
# - Save to DB
# - Run every 10 seconds

import logging
import os
import sys
from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient
from dotenv import load_dotenv

load_dotenv()

coinbase_client = None
logger = logging.getLogger(__name__)

print(os.getenv("COINBASE_API_PRIVATE_KEY").replace("\\n", "\n"))


try:
    coinbase_client = CoinbaseAdvancedTradeAPIClient.from_cloud_api_keys(
        os.getenv("COINBASE_API_KEYNAME"),
        os.getenv("COINBASE_API_PRIVATE_KEY").replace("\\n", "\n"),
    )
except Exception as e:
    logger.error(f"Failed to initialize the Coinbase Advanced Trade API Client: {e}")
    sys.exit(1)

products = coinbase_client.list_products()
product_ids = list(map(lambda p: p.product_id, products.products))

# Filter product list to strings that end with "-USDC", like "BTC-USDC"
product_ids = list(filter(lambda p: p.endswith("-USDC"), product_ids))

best_bids_asks = coinbase_client.get_best_bid_ask(product_ids)


def pricebook_to_dict(pricebook):
    return {
        "bid": pricebook.bids[0].price,
        "ask": pricebook.asks[0].price,
        "product_id": pricebook.product_id,
    }


pricebook_dict = list(map(lambda p: pricebook_to_dict(p), best_bids_asks.pricebooks))
print(pricebook_dict)

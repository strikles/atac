import logging
import requests

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%d/%m/%y %H:%M:%S"
)

user_id = "791808808420643"
app_id = "504405717243097"
app_secret = "6b4708d5b8424f4724791cf3bdbf8a8b"
user_short_token = "EAAHKwRuZAVNkBALXOlhx05bZCBhZCTfgWRmUodJlh9vY2ZB41n4S9lSEBf3JjIE9q1O59AFAvZCU9aiGTy30QFBZAxjQkJjgBTVT1QRTZCRX6ZBn5edonAD6FQCigcD4yb0vn02YIdYZB21SSVeia702qNaS2Wc1G08dqhMJHgRiqKgcCWgiyuh98"

url = "https://graph.facebook.com/oauth/access_token"

payload = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": user_short_token,
}

try:
    response = requests.get(
        url,
        params=payload,
        timeout=5,
    )

except requests.exceptions.Timeout as e:
    logging.error("TimeoutError", e)

else:

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        logging.error("HTTPError", e)

    else:
        response_json = response.json()
        logging.info(response_json)
        user_long_token = response_json["access_token"]

"""
print(response_json)
{'access_token': 'EAAPxxxx', 'token_type': 'bearer', 'expires_in': 5183614}
"""
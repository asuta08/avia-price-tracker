import requests
from config import TOKEN, URL

def get_cheapest(origin, destination, date, price):

    params = {
        "origin": origin,
        "destination": destination,
        "departure_at": date,
        "limit": 40,
        "one_way": 'true',
        "token": TOKEN
    }

    try:
        response = requests.get(URL,params=params)
        data = response.json()
        if data.get("success") and data.get("data"):
            cheap = sorted([x for x in data["data"] if x["price"]<int(price)], key = lambda x: x["price"])
            return cheap[:3]
        return None
    except Exception as error:
        print(f'ERROR: {error}')
        return None

#print(get_cheapest(IATA_origin, IATA_dest, '2026-04')["price"])




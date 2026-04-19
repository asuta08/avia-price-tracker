import requests
from config import TOKEN, URL

def get_cheapest(origin, destination, date):

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
            cheapest = min(data["data"], key= lambda x: x["price"])
            return cheapest
        return None
    except Exception as error:
        print(f'ERROR: {error}')
        return None

#print(get_cheapest(IATA_origin, IATA_dest, '2026-04')["price"])




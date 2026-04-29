import requests
import smtplib
from config import TOKEN, URL
import json
from email.message import EmailMessage

DATA_FILE = 'data.json'

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
            cheap = sorted([x for x in data["data"] if x["price"]<price], key = lambda x: x["price"])
            print(cheap[:3])
            return cheap[:3]
        return None
    except Exception as error:
        print(f'ERROR: {error}')
        return None

def send_letter():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

        cheapest = get_cheapest(data["origin"], data["destination"], data["date"], data["price"])
        dep_time = cheapest[0]["departure_at"].split('T')

        message = f"""Привет, вот самый дешевый билет:
        Цена: {cheapest[0]["price"]}
        Дата вылета: {dep_time[0]} {dep_time[1][:5]}
        Аэропорт вылета: {cheapest[0]["origin_airport"]}
        Авиакомпания: {cheapest[0]["airline"]}
        """
        msg = EmailMessage()
        msg["Subject"] = "Билет стал дешевле!"
        msg["From"] = "notificationbot1050@mail.ru"
        msg["To"] = data["email"]
        msg.set_content(message)

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login('notificationbot1050@mail.ru','6tq07s1mtF2FBuGfaGdT')
        server.send_message(msg)
        server.quit()
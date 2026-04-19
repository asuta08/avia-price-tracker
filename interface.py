from tkinter import *
from tkinter import ttk
import re
from main import get_cheapest
import json

DATA_FILE = 'data.json'
IATA_origin = ''
IATA_dest = ''
DATE = ''
EMAIL = ''

def get_data():
    global IATA_origin, IATA_dest, DATE, EMAIL
    IATA_origin = entry_origin.get().upper()
    IATA_dest = entry_dest.get().upper()
    if len(IATA_dest) == 3 and len(IATA_origin) == 3:
        print(IATA_origin)
        print(IATA_dest)
        try:
            cheapest = get_cheapest(IATA_origin, IATA_dest, '2026-05')
            label.config(text=f'Самый дешевый билет: {cheapest["price"]}')
        except Exception as err:
            print(f"ERROR: {err}")
        entry_origin.delete(0, END)
        entry_dest.delete(0, END)
    DATE = entry_date.get()
    EMAIL = entry_email.get()
    write_to_json()

def check_iata(code):
    if code == '': return True
    code = str(code).upper().strip()
    return bool(re.match(r'^[A-Z]{1,3}$', code))

def write_to_json():
    global IATA_origin, IATA_dest, DATE, EMAIL
    data = {
        "email": EMAIL,
        "origin": IATA_origin,
        "destination": IATA_dest,
        "date": DATE
    }
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

root = Tk()
root.title("Трекер")
root.geometry("600x500+450+100")

check = (root.register(check_iata),"%P")

label_origin = ttk.Label(text="Город вылета")
label_origin.place(relx=.3,rely=.2,anchor=N)
label_dest = ttk.Label(text="Город прилета")
label_dest.place(relx=.7,rely=.2,anchor=N)

label_date = ttk.Label(text="Дата вылета")
label_date.place(relx=.3,rely=.4,anchor=N)
label_email = ttk.Label(text="Ваша почта")
label_email.place(relx=.7,rely=.4,anchor=N)

entry_origin = ttk.Entry(validate="key",validatecommand=check)
entry_origin.place(relx=.3,rely=.25,anchor=N)
entry_dest = ttk.Entry(validate="key",validatecommand=check)
entry_dest.place(relx=.7,rely=.25,anchor=N)

entry_date = ttk.Entry()
entry_date.place(relx=.3,rely=.45,anchor=N)
entry_email = ttk.Entry()
entry_email.place(relx=.7,rely=.45,anchor=N)

btn = ttk.Button(text="Enter",command=get_data)
btn.place(relx=.5,rely=.7,anchor=N)

label = ttk.Label()
label.place(relx=.5,rely=.8,anchor=N)

root.mainloop()
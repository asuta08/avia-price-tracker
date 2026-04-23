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
PRICE = ''

def get_data():
    global IATA_origin, IATA_dest, DATE, EMAIL, PRICE
    IATA_origin = entry_origin.get().upper()
    IATA_dest = entry_dest.get().upper()
    if len(IATA_dest) == 3 and len(IATA_origin) == 3:
        entry_origin.delete(0, END)
        entry_dest.delete(0, END)
    DATE = entry_date.get()
    EMAIL = entry_email.get()
    PRICE = entry_price.get()
    entry_date.delete(0,END)
    entry_email.delete(0,END)
    entry_price.delete(0,END)
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
        "date": DATE,
        "price": PRICE
    }
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def show_cheapest():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            cheapest = get_cheapest(data["origin"], data["destination"], data["date"], data["price"])
            label1.config(text=f'Самый дешевый билет по цене не более {data["price"]}: {cheapest[0]["price"]}')
            if len(cheapest)==2:
                label2.config(text=f'Дешевый билет по цене не более {data["price"]}: {cheapest[1]["price"]}')
            elif len(cheapest)==3:
                label2.config(text=f'Дешевый билет по цене не более {data["price"]}: {cheapest[1]["price"]}')
                label3.config(text=f'Дешевый билет по цене не более {data["price"]}: {cheapest[2]["price"]}')
    except Exception as err:
        print(f'ERROR: {err}')

root = Tk()
root.title("Трекер")
root.geometry("600x500+450+100")

check = (root.register(check_iata),"%P")

label_origin = ttk.Label(text="Город вылета")
label_origin.place(relx=.3,rely=.15,anchor=N)
label_dest = ttk.Label(text="Город прилета")
label_dest.place(relx=.7,rely=.15,anchor=N)

label_date = ttk.Label(text="Дата вылета")
label_date.place(relx=.3,rely=.3,anchor=N)
label_email = ttk.Label(text="Ваша почта")
label_email.place(relx=.7,rely=.3,anchor=N)

label_price = ttk.Label(text="Желаемая цена")
label_price.place(relx=.5,rely=.45,anchor=N)

entry_origin = ttk.Entry(validate="key",validatecommand=check)
entry_origin.place(relx=.3,rely=.2,anchor=N)
entry_dest = ttk.Entry(validate="key",validatecommand=check)
entry_dest.place(relx=.7,rely=.2,anchor=N)

entry_date = ttk.Entry()
entry_date.place(relx=.3,rely=.35,anchor=N)
entry_email = ttk.Entry()
entry_email.place(relx=.7,rely=.35,anchor=N)

entry_price = ttk.Entry()
entry_price.place(relx=.5,rely=.5,anchor=N)

button_save = ttk.Button(text="Save",command=get_data)
button_save.place(relx=.4,rely=.6,anchor=N)

button_find = ttk.Button(text="Find",command=show_cheapest)
button_find.place(relx=.6,rely=.6,anchor=N)

label1 = ttk.Label()
label1.place(relx=.5,rely=.8,anchor=N)
label2 = ttk.Label()
label2.place(relx=.5,rely=.85,anchor=N)
label3 = ttk.Label()
label3.place(relx=.5,rely=.9,anchor=N)

root.mainloop()
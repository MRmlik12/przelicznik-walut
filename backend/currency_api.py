import sqlite3
import requests

addr = "https://api.exchangeratesapi.io/latest"

def get_short_name(currency_name, currency_name2):
    short = []
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("SELECT `short` FROM `currency` WHERE long='{}'".format(currency_name))
    short.append(cursor.fetchone()[0])
    cursor.execute("SELECT `short` FROM `currency` WHERE long='{}'".format(currency_name2))
    short.append(cursor.fetchone()[0])
    db.close()
    return short

def get_currency_details(currency_short):
    params = {
        "base":currency_short
    }
    response = requests.get(addr, params=params)
    return response.json()

def calculate(currency_name, currency_name2, value):
    shorts = get_short_name(currency_name, currency_name2)
    response = get_currency_details(shorts[0])
    response = response.get('rates')
    calculations = float(value) * response[shorts[1]]
    return round(calculations, 2)
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from backend.currency_api import calculate
import os

app = Flask(__name__, template_folder='website', static_folder='website')
values = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html', result="0.00", names=read_currency_names())
    elif request.method == "POST":
        get_values()
        if values[0] == "" or values[1] == "" or values[2] == "":
            values.clear()
            return redirect("/blad")
        else:
            return redirect("/wynik")

def get_values():
    values.append(request.form["currency1"])
    values.append(request.form["currency2"])
    values.append(request.form["input"])

@app.route('/wynik', methods=['GET', 'POST'])
def wynik():
    if request.method == "GET":
        result = calculate(currency_name=values[0], currency_name2=values[1], value=values[2])
        info_message = [values[0], values[1]]
        values.clear()
        return render_template("index.html", result=result, names=read_currency_names(), message="wynik",
            waluta1=info_message[0], waluta2=info_message[1])
    elif request.method == "POST":
        get_values()
        if values[0] == "" or values[1] == "" or values[2] == "":
            values.clear()
            return redirect("/blad")
        else:
            return redirect("/wynik")

@app.route("/blad")
def blad():
    if request.method == "GET":
        return render_template("index.html", result="0.00", names=read_currency_names(), message="blad500")
    elif request.method == "POST":
        get_values()
        if values[0] == "" or values[1] == "" or values[2] == "":
            values.clear()
            return redirect("/blad")
        else:
            return redirect("/wynik")

@app.errorhandler(405)
def error_405():
    return redirect("/blad")

@app.errorhandler(500)
def error(e):
    return redirect("/blad")

@app.errorhandler(404)
def error_404(e):
    return "<h1>Strona nie została znaleziona</h1>"

def read_currency_names():
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("SELECT `long` FROM `currency`")
    names = cursor.fetchall()
    curr = [""]
    for name in names:
        curr.append(name[0])
    cursor.close()
    db.close()
    return curr

def run():
    app.run(debug=False, host="https://przelicznik-walut.herokuapp.com/", port=os.environ["PORT"])
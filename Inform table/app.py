from flask import Flask, render_template, request, redirect, url_for
import requests
import time
import sys
import copy





my_app = Flask(__name__)
ip_adresses = {84 : "145.93.36.167"}

@my_app.route('/')
def home():
    return render_template("start.html")

@my_app.route('/inform-table', methods = ['POST'])
def inform_table():
    global ip_adresses
    table_number = request.form['table number']
    ip_adress = f"http://{ip_adresses[int(table_number)]}:5000/order-ready"
    response = requests.post(ip_adress, json = {"Ok" : "Ok"})
    return redirect("/")

#@my_app.route('/go-to-cashier-menu')
#def go_to_cashier_website():
#    return redirect("/cashier-menu")

#@my_app.route('/cashier-menu')
#def cashier_menu():
#    return render_template("cashier menu.html")



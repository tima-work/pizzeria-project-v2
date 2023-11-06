from flask import Flask, render_template, request, redirect, url_for
import requests
import time
import sys
import copy
import random





my_app = Flask(__name__)
order_list = [ ]
products_dict = {"Pepperoni/Peperoni" : 500, "Hawaї" : 500, "Seafood pizza/Pizza di pesce" : 500, "Four cheese pizza/quattro formaggi" : 500, "Veggie pizza/pizza vegeterian" : 500, "Cola" : 500, "Sprite" : 500, "Pepsi" : 500, "Heineken" : 500, "Corona" : 500}
all_orders = {}
ip_adresses = {84 : "145.93.36.167"}

def get_price():
    global order_list
    global products_dict
    if len(order_list) == 0:
        return 0
    else:
        price_list = [products_dict[i] for i in order_list]
        return sum(price_list)
    
def add_order():
    global all_orders
    global order_list
    order_number = random.randint(1, 999)
    while order_number in all_orders:
        order_number = random.randint(1, 999)
    all_orders[order_number] = order_list
    return order_number


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

@my_app.route('/go-to-cashier-menu', methods=['POST', 'GET'])
def go_to_cashier_website():
    return redirect('/main-menu')

@my_app.route('/main-menu')
def main_menu():
    return render_template("main menu.html", products_dict = products_dict)

@my_app.route('/go-to-payment-method', methods=['POST'])
def go_to_payment_method():
    global order_list
    global products_dict
    for a in products_dict:
        for b in range(int(request.form[a])):
            order_list.append(a)
    print(request.form['Hawaї'])
    return redirect('/payment-method')

@my_app.route('/payment-method')
def payment_method():
    total_price = get_price()
    return render_template('payment method.html', total_price = get_price())

@my_app.route('/place-order', methods=['POST', 'GET'])
def place_order():
    return redirect('/order-number')

@my_app.route('/order-number')
def order_number():
    global all_orders
    order_number = add_order()
    print(str(all_orders))
    return render_template('place order.html', order_number = order_number)

@my_app.route('/back_home', methods=['POST', 'GET'])
def back_home():
    return redirect('/')



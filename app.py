from flask import Flask, render_template, request, redirect, url_for
import requests
import time
import sys
import copy
import random





app = Flask(__name__)
app.static_folder = 'static'
order_list = [ ]
eating_place = ""
products_dict = {"Pepperoni/Peperoni" : 7, "Hawaiian" : 7, "Seafood pizza/Pizza di Pesce" : 8.5, "Four cheese pizza/Quattro Formaggi" : 8, "Veggie pizza/Pizza Vegetariana" : 6.5, "Cola" : 3, "Sprite" : 3, "Pepsi" : 3, "Heineken" : 5, "Corona" : 5}
pizzas = ("Pepperoni/Peperoni", "Hawaiian", "Seafood pizza/Pizza di Pesce", "Four cheese pizza/Quattro Formaggi", "Veggie pizza/Pizza Vegetariana")
screen = ""
number_of_order = -1
all_orders = { }
order_ending_time = { }
ip_adresses = {84 : "145.93.160.96"}
smart_oven_ip = "145.93.98.2"


def get_prices():
    global order_list
    global products_dict
    if len(order_list) == 0:
        return 0, [ ]
    else:
        price_list = [products_dict[i] for i in order_list]
        return sum(price_list), price_list
    
def calculate_time(order_number):
    time_required = 0
    for a in all_orders:
        for b in range(len(all_orders[a])):
            if all_orders[a][b] in pizzas:
                time_required += 5
            if all_orders[a][b] == all_orders[order_number][len(all_orders[order_number]) - 1]:
                return time_required

@app.route('/')
def init():
    return redirect('/home/')

@app.route('/home/')
def home():
    global screen
    global order_list
    global number_of_order
    order_list = [ ]
    number_of_order = ""
    screen = '/home/'
    return render_template("clientWebsiteHomePage.html")

@app.route('/home/choose-take-away', methods = ['POST', 'GET'])
def choose_take_away():
    global eating_place
    eating_place = "take away"
    return redirect("/home/pizza-menu")

@app.route('/home/choose-delivery', methods = ['POST', 'GET'])
def choose_delivery():
    global eating_place
    eating_place = "delivery"
    return redirect("/home/pizza-menu")

@app.route('/home/pizza-menu')
def pizza_menu():
    global order_list
    global screen
    screen = '/home/pizza-menu'
    price, price_list = get_prices()
    return render_template("pizza.html", order_list = order_list, price = price, price_list = price_list)

@app.route('/home/drinks-menu')
def drinks_menu():
    global order_list
    global screen
    screen = '/home/drinks-menu'
    price, price_list = get_prices()
    if eating_place == "delivery":
        button_name = "Delivery"
    else:
        button_name = "Payment"
    return render_template("drinks.html", order_list = order_list, price = price, price_list = price_list, button_name = button_name)

@app.route('/home/add-product', methods=['POST'])
def add_product():
    global order_list
    global screen
    product = request.form['product name']
    order_list.append(product)
    return redirect(screen)

@app.route('/home/remove-product', methods=['POST'])
def remove_product():
    global order_list
    global screen
    product = request.form['product name']
    order_list.remove(product)
    return redirect(screen)

@app.route('/home/go-home', methods=['POST', 'GET'])
def go_home():
    global order_list
    order_list.clear()
    return redirect("/")

@app.route('/home/go-back', methods=['POST', 'GET'])
def go_back():
    global order_list
    global screen
    if screen == "/home/pizza-menu":
        order_list.clear()
        return redirect("/")
    elif screen == "/home/drinks-menu":
        return redirect("/home/pizza-menu")
    elif screen == "/home/delivery":
        return redirect("/home/drinks-menu")
    elif screen == "/home/payment" and eating_place == "delivery":
        return redirect("/home/delivery")
    else:
        return redirect("/home/drinks-menu")

@app.route('/home/go-to-payment', methods=['POST', 'GET'])
def go_to_payment():
    global order_list
    if len(order_list) == 0:
        return redirect(screen)
    elif eating_place == "delivery":
        return redirect("/home/delivery")
    else:
        return redirect("/home/payment")

@app.route('/home/payment', methods=['POST', 'GET'])
def payment():
    global order_list
    global screen
    price, price_list = get_prices()
    screen = "/home/payment"
    return render_template("paymentPage.html", order_list = order_list, price = price, price_list = price_list)

@app.route('/home/delivery', methods=['POST', 'GET'])
def delivery():
    global order_list
    global screen
    price, price_list = get_prices()
    screen = "/home/delivery"
    return render_template("deliveryPage.html", order_list = order_list, price = price, price_list = price_list)
        
@app.route('/home/go-to-drinks', methods=['POST', 'GET'])
def go_to_drinks():
    return redirect('/home/drinks-menu')

@app.route('/home/go-to-order-number', methods=['POST', 'GET'])
def go_to_order_number():
    return redirect('/home/order-number')

@app.route('/home/order-number')
def order_number():
    global number_of_order
    global all_orders
    global order_list
    global eating_place
    global order_ending_time
    number_of_order = random.randint(1, 999)
    while number_of_order in all_orders:
        number_of_order = random.randint(1, 999)
    all_orders[number_of_order] = order_list
    order_ending_time[number_of_order] = time.time() + calculate_time(number_of_order) * 60
    order_list = [ ]
    eating_place = ""
    return render_template('orderNumber.html', order_number = number_of_order)

@app.route('/home/add-something-more', methods=['POST'])
def add_something_more():
    return redirect("/home/pizza-menu")

@app.route('/home/go-to-order-screen', methods=['POST', 'GET'])
def go_to_order_screen():
    return redirect("/order-screen")

@app.route('/order-screen')
def order_screen():
    time_list = [ ]
    for i in all_orders:
        if order_ending_time[i] > time.time():
            time_list.append(int((order_ending_time[i] - time.time()) // 60))
        else:
            time_list.append("Ready")
    return render_template("orderlist_template.html", all_orders = all_orders, time_list = time_list)

@app.route('/chef-website')
def chef_website():
    global all_orders
    return render_template("chef website.html", all_orders = all_orders)

@app.route('/cashier/')
def cashier():
    global order_list
    global number_of_order
    order_list = [ ]
    number_of_order = ""
    return render_template("cashier start.html")

@app.route('/cashier/go-to-cashier-menu')
def go_to_cashier_menu():
    return redirect("/cashier/cashier-menu")

@app.route('/cashier/cashier-menu')
def cashier_menu():
    return render_template("menuCashier.html")

@app.route('/cashier/go-to-cashier-payment', methods=['POST'])
def go_to_cashier_payment():
    global order_list
    for b in products_dict:
        try:
            for a in range(int(request.form[b])):
                order_list.append(b)
        except:
            pass
    if len(order_list) == 0:
        return redirect("/cashier/cashier-menu")
    else:
        return redirect('/cashier/cashier-payment')

@app.route('/cashier/cashier-payment')
def cashier_payment():
    price, price_list = get_prices()
    return render_template('PaymentCashierSite.html', price = price)

@app.route('/cashier/go-to-order-number-cashier', methods=['POST', 'GET'])
def go_to_order_number_cashier():
    global number_of_order
    global all_orders
    global order_list
    global order_ending_time
    number_of_order = random.randint(1, 999)
    while number_of_order in all_orders:
        number_of_order = random.randint(1, 999)
    all_orders[number_of_order] = order_list
    order_ending_time[number_of_order] = time.time() + calculate_time(number_of_order) * 60
    order_list = [ ]
    return redirect('/cashier/order-number-cashier')

@app.route('/cashier/order-number-cashier')
def order_number_cashier():
    return render_template("NumberOfOrderCashier.html", order_number = number_of_order)

@app.route('/cashier/return-home')
def return_home_cashier():
    return redirect("/cashier/")

@app.route('/cashier/order-was-collected', methods=['POST'])
def order_was_collected():
    global all_orders
    try:
        order_number = int(request.form["order number"])
    except:
        return redirect("/cashier/")
    if order_number in all_orders:
        all_orders.pop(order_number)
        for i in range(100):
            print("Success")
    return redirect("/cashier/")

@app.route('/cashier/inform-table', methods=['POST'])
def inform_table():
    global ip_adresses
    try:
        table_number = int(request.form['table number'])
    except:
        return redirect("/cashier/")
    ip_adress = f"http://{ip_adresses[table_number]}:5000/order-ready"
    response = requests.post(ip_adress, json = {"Ok" : "Ok"})
    return redirect("/cashier/")

@app.route('/smart-oven/')
def smart_oven():
    return render_template("start.html")

@app.route('/smart-oven/temperature')
def temperature():
    return render_template("set temperature.html")

@app.route('/smart-oven/set-temperature', methods=['POST', 'GET'])
def set_temperature():
    global expected_temperature
    global temperature_start_time
    expected_temperature = int(copy.copy(request.form["amountRange"]))
    temperature_start_time = time.time() + expected_temperature * 0.1
    response = requests.post(f"http://{smart_oven_ip}:5000/get-data", json = {'mode' : 'temperature', 'expected temperature' : expected_temperature})
    return redirect("/show-temperature")

@app.route('/smart-oven/show-temperature', methods=['POST', 'GET'])
def show_temperature():
    global expected_temperature
    global temperature_start_time
    if round((time.time() - temperature_start_time) / 0.1, 0) >= expected_temperature:
        response = requests.post(f"http://{smart_oven_ip}:5000/get-data", json = {'mode' : 'sleep'})
        return redirect('/set-timer')
    else:
        return render_template("smart oven.html", expected_temperature = expected_temperature, current_temperature = round((time.time() - temperature_start_time) / 0.1, 0))

@app.route('/smart-oven/set-timer', methods=['POST', 'GET'])
def set_timer():
    return render_template("set timer.html")

@app.route('/smart-oven/get-time', methods=['POST', 'GET'])
def get_time():
    global timer_end
    global order_number
    global pizza
    timer_end = time.time() + int(request.form['minutes']) * 60 + int(request.form['seconds'])
    order_number = request.form['order number']
    pizza = request.form['pizza']
    response = requests.post(f"http://{smart_oven_ip}:5000/get-data", json = {'mode' : 'timer', 'timer end' : timer_end})
    return redirect('/show-timer')

@app.route('/smart-oven/show-timer', methods=['POST', 'GET'])
def show_timer():
    global order_number
    global pizza
    global timer_end
    if int(timer_end - time.time()) // 60 < 0:
        response = requests.post(f"http://{smart_oven_ip}:5000/get-data", json = {'mode' : 'sleep'})
        return redirect('/pizza-done')
    else:
        return render_template("show timer.html", minutes = str(int(timer_end - time.time()) // 60), seconds = str(int(round((timer_end - time.time()) % 60, 0))), order_number = order_number, pizza = pizza)


@app.route('/smart-oven/pizza-done', methods=['POST', 'GET'])
def pizza_done():
    response = requests.post(f"http://{smart_oven_ip}:5000/get-data", json = {'mode' : 'done'})
    return render_template("pizza done.html")

if __name__ == "__main__":
    app.run()
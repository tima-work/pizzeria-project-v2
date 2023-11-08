import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from flask import Flask, render_template, redirect
import threading
import os
from flask import Flask, url_for
import csv
from flask import Flask, render_template, request
import random

# Set the current working directory to script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

app = Flask(__name__,)
app.static_folder = 'static'

@app.route('/')
def homepage():
    return redirect('/casier')

@app.route('/casier')
def hello_Temperature():
    return render_template('menuCashier.html')

def add_order():
    global all_orders
    global order_list
    
    while order_number in all_orders:
        order_number = random.randint(1, 999)
    all_orders[order_number] = order_list
    return order_number

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        pizza1 = request.form['quantity1']
        pizza2 = request.form['quantity2']
        pizza3 = request.form['quantity3']
        pizza4 = request.form['quantity4']
        pizza5 = request.form['quantity5']
        drinks1 = request.form['quantity6']
        drinks2 = request.form['quantity7']
        drinks3 = request.form['quantity8']
        drinks4 = request.form['quantity9']
        drinks5 = request.form['quantity10']
        
        order_number = random.randint(1, 999)  # Generate a new order number
        
        with open('data.csv', 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([order_number, pizza1, pizza2, pizza3, pizza4, pizza5, drinks1, drinks2, drinks3, drinks4, drinks5])

        return '''
        <h1>Data stored successfully!</h1>
        <form action="/casier" method="get">
            <button type="submit">Go Back</button>
        </form>
        '''

@app.route('/empty')
def empty_csv():
    with open('data.csv', 'w') as file:
        file.truncate(0)

    return '''
    <h1>CSV file emptied successfully!</h1>
    <h2>Wait 10 seconds!</h2>
    <form action="/casier" method="get">
        <button type="submit">Go to caasier</button>
    </form>
    <form action="/" method="get">
        <button type="submit">Go to home</button>
    </form>
    '''

def write_data_to_csv():
    global order_number, pizza1, pizza2, pizza3, pizza4, pizza5, drinks1, drinks2, drinks3, drinks4, drinks5
    data_file_path = 'data.csv'

    while True:
        if not os.path.exists(data_file_path):
            with open(data_file_path, 'w', newline='') as file:
                file.write("order_number, pizza1, pizza2, pizza3, pizza4, pizza5, drinks1, drinks2, drinks3, drinks4, drinks5\n")
        with open(data_file_path, 'a', newline='') as file:
            file.write(f"{order_number}{pizza1}, {pizza2}, {pizza3}, {pizza4}, {pizza5}, {drinks1}, {drinks2}, {drinks3}, {drinks4}, {drinks5}\n")
        time.sleep(10)


@app.route('/data')
def display_data():
    with open('data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        data_list = list(csv_reader)

    return render_template('data.html', data_list=data_list)

if __name__ == "__main__":
    app.run(debug=False)

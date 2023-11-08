import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from flask import Flask, render_template, redirect
import threading
import os
from flask import Flask, url_for
import csv
from flask import Flask, render_template, request

# Set the current working directory to script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


app = Flask(__name__,)
app.static_folder = 'static'






@app.route('/')
def homepage():
    #link=url_for('home')
    return redirect('/casier')


@app.route('/casier')
def hello_Temperature():
    #link = url_for('casier') 
    return render_template('menuCashier.html')


#



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        pizza1 = request.form['quantity1']
        pizza2 = request.form['quantity2']
        pizza3 = request.form['quantity3']
        pizza4 = request.form['quantity4']
        pizza5 = request.form['quantity5']
        # drinks
        drinks1 = request.form['quantity6']
        drinks2 = request.form['quantity7']
        drinks3 = request.form['quantity8']
        drinks4 = request.form['quantity9']
        drinks5 = request.form['quantity10']

        with open('data.csv', 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([pizza1, pizza2, pizza3, pizza4, pizza5, drinks1, drinks2, drinks3, drinks4, drinks5])
            

        return '''
        <h1>Data stored successfully!</h1>
        <form action="/casier" method="get">
            <button type="submit">Go Back</button>
        </form>
        '''

 

#@app.route('/orders')
#def display_orders():
#    with open('data.csv', 'r') as file:
#        csv_reader = csv.reader(file)
#        data_list = list(csv_reader)
#
#    # Calculate the average for each column
#    averages = []
#    for i in range(len(data_list[0])):
#        column_values = [float(row[i]) for row in data_list[1:] if row[i] != '']  # Exclude empty values
#        column_average = sum(column_values) / len(column_values)
#        averages.append(column_average)
#
#    num_columns = len(data_list[0])  # Calculate the number of columns
#
#    return render_template('data.html', data=data_list, averages=averages, num_columns=num_columns)
#


@app.route('/empty')
def empty_csv():
    with open('data.csv', 'w') as file:
        file.truncate(0)

    #return 'CSV file emptied successfully!'
    return '''
    <h1>CSV file emptied successfully!</h1>
    <h2>Wait 10 seconds!</h2>
    <form action="/form" method="get">
        <button type="submit">Go to form</button>
    </form>
    <form action="/data" method="get">
        <button type="submit">Go to data</button>
    </form>


    '''


#
# write to csv
 
def write_data_to_csv():
    global pizza1, pizza2, pizza3, pizza4, pizza5, drinks1, drinks2, drinks3, drinks4, drinks5
    data_file_path = 'data.csv'  # Relative path to the file

    while True:
        if not os.path.exists(data_file_path):
            with open(data_file_path, 'w', newline='') as file:
                file.write("temperature, humidity, value\n")
        with open(data_file_path, 'a', newline='') as file:
            file.write(f"{pizza1}, {pizza2}, {pizza3}, {pizza4}, {pizza5}, {drinks1}, {drinks2}, {drinks3}, {drinks4}, {drinks5}\n")
        time.sleep(10)


# --------------
# main program
# --------------

if __name__ == "__main__":
    app.run(debug=False)
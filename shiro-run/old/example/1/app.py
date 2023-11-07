import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from flask import Flask, render_template
import threading
import os
from flask import Flask, url_for
import csv
from flask import Flask, render_template, request

# Set the current working directory to script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


DHTPIN = 12  # digital pin => air
LDRPIN = 2  # analog pin A2

app = Flask(__name__)

PIN9 = 9  # left yellow button
REDLEDPIN5 = 5  # green led

humidity = 0
temperature = 0
value = 0


def Measure(data):
    global humidity, temperature
    if (data[1] == 0):
        humidity = data[4]
        temperature = data[5]


def setup():
    global board
    board = CustomTelemetrix()
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, dht_type=11, callback=Measure)
    board.set_pin_mode_analog_input(LDRPIN, callback=LDRChanged, differential=10)
    board.set_pin_mode_digital_input_pullup(PIN9)


def loop():
    global humidity, temperature, value
    time.sleep(0.01)

    data2 = board.digital_read(PIN9)
    if data2:
        level2 = data2[0]
        print(level2)

        if level2 == 0:
            board.digital_write(REDLEDPIN5, 1)
        else:
            board.digital_write(REDLEDPIN5, 0)

    print(humidity, temperature, value)
    if value == 0:
        board.displayShow(temperature)
    elif value == 1:
        board.displayShow(humidity)
    elif value == 2:
        board.displayShow(board.get_brightness())
    elif value == 3:
        board.displayShow(temperature)


def LDRChanged(data):
    global value
    value = data[2]


@app.route('/')
def hello_world():
    link=url_for('hello_Temperature')
    legend_image = url_for('static', filename='hello_world.jpg')
    return render_template('index.html', input_EPIC_data="OFF", link=link, legend_image=legend_image)


@app.route('/Temperature')
def hello_Temperature():
    link = url_for('hello_Humidity') 
    legend_image = url_for('static', filename='hello_Temperature.jpg')
    return render_template('index.html', input_EPIC_name="Temperature", input_EPIC_data=temperature, link=link, legend_image=legend_image)


@app.route('/Humidity')
def hello_Humidity():
    link=url_for('hello_Brightness')
    legend_image = url_for('static', filename='hello_Humidity.jpg')
    return render_template('index.html', input_EPIC_name="Humidity", input_EPIC_data=humidity, link=link, legend_image=legend_image)


@app.route('/Brightness')
def hello_Brightness():
    link=url_for('hello_world')
    legend_image = url_for('static', filename='hello_Brightness.jpg')
    return render_template('index.html', input_EPIC_name="Brightness", input_EPIC_data=value, link=link, legend_image=legend_image)




#
#

@app.route('/form')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        column1_data = request.form['column1']
        column2_data = request.form['column2']
        column3_data = request.form['column3']
        # Add more columns as needed

        with open('data.csv', 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([column1_data, column2_data, column3_data])
            # Add more columns as needed

        return '''
        <h1>Data stored successfully!</h1>
        <form action="/form" method="get">
            <button type="submit">Go Back</button>
        </form>
        '''



@app.route('/data')
def display_data():
    with open('data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        data_list = list(csv_reader)

    # Calculate the average for each column
    averages = []
    for i in range(len(data_list[0])):
        column_values = [float(row[i]) for row in data_list[1:] if row[i] != '']  # Exclude empty values
        column_average = sum(column_values) / len(column_values)
        averages.append(column_average)

    num_columns = len(data_list[0])  # Calculate the number of columns

    return render_template('data.html', data=data_list, averages=averages, num_columns=num_columns)


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
    global humidity, temperature, value
    data_file_path = 'data.csv'  # Relative path to the file

    while True:
        if not os.path.exists(data_file_path):
            with open(data_file_path, 'w', newline='') as file:
                file.write("temperature, humidity, value\n")
        with open(data_file_path, 'a', newline='') as file:
            file.write(f"{temperature}, {humidity}, {value}\n")
        time.sleep(10)


def main():
    setup()
    main_thread = threading.Thread(target=app.run)
    data_thread = threading.Thread(target=write_data_to_csv)
    main_thread.start()
    data_thread.start()

    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print('shutdown')
            board.shutdown()
            os._exit(0)


if __name__ == '__main__':
    main()

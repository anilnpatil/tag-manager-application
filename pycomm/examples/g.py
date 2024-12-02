from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

# Create a ClxDriver instance
c = ClxDriver()
is_connected = False  # Flag to track connection status

@app.route('/insertDataToPlc', methods=['POST'])
@cross_origin()
def insert_data_to_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            c.open('192.168.12.5')  # Open connection to the PLC (only once)
            print("Connection to PLC established.")
            is_connected = True

        c.forward_open()  # Initialize the session

        # Get the JSON data from the request
        data_list = request.json

        # Iterate through the data and process it
        for item in data_list:
            for key, value in item.items():
                # Convert value to string regardless of its type
                str_value = str(value)
                
                print("Writing to PLC: Key:", type(key), "Value:", type(str_value))
                
                # Write string value to PLC
                key = key.encode('utf-8')
                str_value = str_value.encode('utf-8')
                try:
                    c.write_string(key, str_value)
                    print("Read String Value is", c.read_string(key))
                    print("Data written to PLC successfully for key:", key.decode('utf-8'))
                except Exception as e:
                    print("Error writing string:", key.decode('utf-8'), ":", e)
                sleep(1)

        return jsonify({"message": "Data written to PLC successfully.", "error": None}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while writing data to PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            c.close()
            is_connected = False
            print("Connection to PLC closed.")

@app.route('/closeConnection', methods=['GET'])
def close_connection():
    global is_connected
    if is_connected:
        c.close()
        is_connected = False
        print("Connection to PLC closed.")
    return jsonify({"message": "Connection to PLC closed successfully.", "error": None}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8083)

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
            if not c.open('192.168.12.5'):  # Open connection to the PLC
                raise Exception("Unable to open connection to PLC.")
            if not c.register_session():  # Register the session
                raise Exception("Unable to register session with PLC.")
            if not c.forward_open():  # Initialize the session
                raise Exception("Unable to forward open with PLC.")
            print("Connection to PLC established.")
            is_connected = True

        # Get the JSON data from the request
        data_list = request.json

        # Collect all the write operations
        write_operations = []
        for item in data_list:
            for key, value in item.items():
                # Convert value to string regardless of its type
                str_value = str(value)
                key = key.encode('utf-8')
                str_value = str_value.encode('utf-8')
                write_operations.append((key, str_value))

        # Perform all write operations
        for key, str_value in write_operations:
            try:
                c.write_string(key, str_value)
                print("Data written to PLC successfully for key: {key.decode('utf-8')}")
            except Exception as e:
                print("Error writing string: {key.decode('utf-8')}: {e}")

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

@app.route('/readDataFromPlc', methods=['POST'])
@cross_origin()
def read_data_from_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            if not c.open('192.168.12.5'):  # Open connection to the PLC
                raise Exception("Unable to open connection to PLC.")
            if not c.register_session():  # Register the session
                raise Exception("Unable to register session with PLC.")
            if not c.forward_open():  # Initialize the session
                raise Exception("Unable to forward open with PLC.")
            print("Connection to PLC established.")
            is_connected = True

        # Get the tag name from the request
        tag_name = request.json.get('tag_name')
        if not tag_name:
            raise Exception("Tag name is required.")

        try:
            tag_name = tag_name.encode('utf-8')
            read_value = c.read_string(tag_name)
            print("Read from PLC: Tag: {tag_name.decode('utf-8')}, Value: {read_value}")
            return jsonify({"data": {tag_name.decode('utf-8'): read_value}, "error": None}), 200
        except Exception as e:
            print("Error reading string: {tag_name.decode('utf-8')}: {e}")
            return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            c.close()
            is_connected = False
            print("Connection to PLC closed.")

if __name__ == '__main__':
    app.run(debug=True, port=8083)

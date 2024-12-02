from pylogix import PLC
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)

# IP Address of the Robot Controller
robot_ip = '192.168.1.10'

# List of tags to read
tags_to_read = [f't{i}' for i in range(1, 100)]  # Customize tags as per FANUC configuration

def batch_write(robot_ip, batch):
    try:
        with PLC() as plc:
            plc.IPAddress = robot_ip
            for key, value in batch:
                plc.Write(key, str(value))
                print(f"Data written to Robot Controller successfully for key: {key}")
    except Exception as e:
        print(f"Error during batch write: {e}")

def read_tag(robot_ip, tag):
    try:
        with PLC() as plc:
            plc.IPAddress = robot_ip
            value = plc.Read(tag).Value
            print(f"Data read from Robot Controller for tag {tag}: {value}")
            return tag, value
    except Exception as e:
        print(f"Error reading tag {tag}: {e}")
        return tag, None

def batch_read(robot_ip, tags, max_workers=50):
    try:
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(read_tag, robot_ip, tag) for tag in tags]
            for future in as_completed(futures):
                tag, value = future.result()
                if value is not None:
                    results[tag] = value
        return results
    except Exception as e:
        print(f"Error during batch read: {e}")
        return None

@app.route('/insertDataToRobot', methods=['POST'])
@cross_origin()
def insert_data_to_robot():
    try:
        data_list = request.json
        write_operations = [(key, value) for item in data_list for key, value in item.items()]
        start_time = time.time()

        batch_size = 10
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(0, len(write_operations), batch_size):
                batch = write_operations[i:i + batch_size]
                futures.append(executor.submit(batch_write, robot_ip, batch))
            
            for future in as_completed(futures):
                future.result()

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to write to Robot Controller: {time_taken:.4f} seconds")

        return jsonify({"message": "Data written to Robot Controller successfully.", "error": None}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred while writing data to Robot Controller.", "error": str(e)}), 500

@app.route('/readDataFromRobot', methods=['GET'])
@cross_origin()
def read_data_from_robot():
    try:
        start_time = time.time()
        results = batch_read(robot_ip, tags_to_read, max_workers=50)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to read from Robot Controller: {time_taken:.4f} seconds")

        if results is None:
            raise Exception("Error occurred during reading from Robot Controller.")

        return jsonify({"message": "Data read from Robot Controller successfully.", "data": results, "error": None}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred while reading data from Robot Controller.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8083)

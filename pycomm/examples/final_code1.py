# from pylogix import PLC
# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# import time
# from concurrent.futures import ThreadPoolExecutor, as_completed

# app = Flask(__name__)
# CORS(app)

# # List of tags to read (sampled)
# tags_to_read = [f't{i}' for i in range(1, 1000)]  # Assuming t1, t2, ..., t1000

# def batch_write(plc_ip, batch):
#     try:
#         with PLC() as plc:
#             plc.IPAddress = plc_ip
#             for key, value in batch:
#                 plc.Write(key, str(value))
#                 print(f"Data written to PLC successfully for key: {key}")
#     except Exception as e:
#         print(f"Error during batch write: {e}")

# def read_tag(plc_ip, tag):
#     try:
#         with PLC() as plc:
#             plc.IPAddress = plc_ip
#             value = plc.Read(tag).Value
#             print(f"Data read from PLC for tag {tag}: {value}")
#             return tag, value
#     except Exception as e:
#         print(f"Error reading tag {tag}: {e}")
#         return tag, None

# def batch_read(plc_ip, tags, max_workers=50):
#     try:
#         results = {}
#         with ThreadPoolExecutor(max_workers=max_workers) as executor:
#             futures = [executor.submit(read_tag, plc_ip, tag) for tag in tags]
#             for future in as_completed(futures):
#                 tag, value = future.result()
#                 if value is not None:
#                     results[tag] = value
#         return results
#     except Exception as e:
#         print(f"Error during batch read: {e}")
#         return None

# @app.route('/insertDataToPlc', methods=['POST'])
# @cross_origin()
# def insert_data_to_plc():
#     try:
#         # Extract the PLC IP address from query parameters
#         plc_ip = request.args.get('ip')
#         if not plc_ip:
#             raise ValueError("IP address parameter 'ip' is missing.")
        
#         # Get the JSON data from the request
#         data_list = request.json
#         if not isinstance(data_list, list):
#             raise ValueError("Payload must be a list of tag-value dictionaries.")
        
#         # Prepare write operations
#         write_operations = []
#         for item in data_list:
#             tag = item.get('tag')
#             value = item.get('value')
#             if not tag or value is None:
#                 raise ValueError("Each item in payload must have 'tag' and 'value'.")
#             write_operations.append((tag, value))
        
#         # Measure time before writing starts
#         start_time = time.time()
        
#         # Perform write operations using multithreading
#         batch_size = 10
#         with ThreadPoolExecutor(max_workers=20) as executor:
#             futures = []
#             for i in range(0, len(write_operations), batch_size):
#                 batch = write_operations[i:i + batch_size]
#                 futures.append(executor.submit(batch_write, plc_ip, batch))
            
#             for future in as_completed(futures):
#                 future.result()
        
#         # Measure time after all write operations complete
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f"Time taken to write to PLC: {time_taken:.4f} seconds")
        
#         if time_taken > 3:
#             # Log a custom message instead of raising an exception
#             print("Custom Log: Writing to PLC took longer than 3 seconds.")
        
#         return jsonify({"message": "Data written to PLC successfully.", "error": None}), 200
    
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "Error occurred while writing data to PLC.", "error": str(e)}), 500



# @app.route('/readDataTagsFromPlc', methods=['GET'])
# @cross_origin()
# def read_data_tags_from_plc():
#     try:
#         ip_address = request.args.get('ip')  # Get IP address from query parameter
#         if not ip_address:
#             raise ValueError("IP address parameter 'ip' is missing.")

#         with PLC() as plc:
#             plc.IPAddress = ip_address

#             # Read all available tags from the PLC
#             tags_response = plc.GetTagList()
#             if tags_response is None or tags_response.Value is None:
#                 raise Exception("Failed to get tag list from PLC.")

#             # Extract tag names from the response
#             tag_names = [tag.TagName for tag in tags_response.Value]

#         return jsonify({"tags": tag_names}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "Error occurred while reading data from PLC please check the Ip address.", "error": str(e)}), 500

# @app.route('/readDataFromPlcByTags', methods=['GET'])
# @cross_origin()
# def read_data_from_plc():
#     try:
#         ip_address = request.args.get('ip')  # Get IP address from query parameter
#         if not ip_address:
#             raise ValueError("IP address parameter 'ip' is missing.")

#         # Measure time before reading starts
#         start_time = time.time()

#         # Perform read operations with the provided IP
#         results = batch_read(ip_address, tags_to_read, max_workers=50)

#         # Measure time after all read operations complete
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f"Time taken to read from PLC: {time_taken:.4f} seconds")

#         if results is None:
#             raise Exception("Error occurred during reading from PLC.")

#         return jsonify({"message": "Data read from PLC successfully.", "data": results, "error": None}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500
    

# @app.route('/getTagValues', methods=['POST'])
# @cross_origin()
# def get_tag_values():
#     try:
#         ip_address = request.args.get('ip')  # Get IP address from query parameter
#         payload = request.json  # Read JSON payload
#         tags_to_read = payload.get('tags', [])  # Extract the tags from payload

#         if not ip_address:
#             raise ValueError("IP address parameter 'ip' is missing.")
#         if not tags_to_read:
#             raise ValueError("No tags provided in the payload.")

#         # Measure time before reading starts
#         start_time = time.time()

#         # Perform read operations with the provided IP and tags
#         results = batch_read(ip_address, tags_to_read, max_workers=50)

#         # Convert results to JSON-serializable format
#         serialized_results = {}
#         for tag, value in results.items():
#             if isinstance(value, bytes):
#                 # Decode bytes to string (adjust encoding if necessary)
#                 serialized_results[tag] = value.decode('utf-8', errors='ignore')
#             else:
#                 serialized_results[tag] = value

#         # Measure time after all read operations complete
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f"Time taken to read from PLC: {time_taken:.4f} seconds")

#         if results is None:
#             raise Exception("Error occurred during reading from PLC.")

#         return jsonify({"message": "Data read from PLC successfully.", "data": serialized_results, "error": None}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True, port=8083)


from pylogix import PLC
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)

# List of tags to read (sampled)
tags_to_read = [f't{i}' for i in range(1, 1000)]  # Assuming t1, t2, ..., t1000

def is_plc_connected(ip):
    """Utility function to check if PLC is connected."""
    try:
        with PLC() as plc:
            plc.IPAddress = ip
            response = plc.GetTagList()  # Attempt to get tag list to verify connection
            return response is not None and response.Value is not None
    except Exception as e:
        print(f"PLC connection check failed for IP {ip}: {e}")
        return False

def batch_write(plc_ip, batch):
    try:
        with PLC() as plc:
            plc.IPAddress = plc_ip
            for key, value in batch:
                plc.Write(key, str(value))
                print(f"Data written to PLC successfully for key: {key}")
    except Exception as e:
        print(f"Error during batch write: {e}")

def read_tag(plc_ip, tag):
    try:
        with PLC() as plc:
            plc.IPAddress = plc_ip
            value = plc.Read(tag).Value
            print(f"Data read from PLC for tag {tag}: {value}")
            return tag, value
    except Exception as e:
        print(f"Error reading tag {tag}: {e}")
        return tag, None

def batch_read(plc_ip, tags, max_workers=50):
    try:
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(read_tag, plc_ip, tag) for tag in tags]
            for future in as_completed(futures):
                tag, value = future.result()
                if value is not None:
                    results[tag] = value
        return results
    except Exception as e:
        print(f"Error during batch read: {e}")
        return None

@app.before_request
def check_plc_connection():
    """Middleware to validate PLC connection before route execution."""
    if request.endpoint in ['insert_data_to_plc', 'read_data_tags_from_plc', 'read_data_from_plc', 'get_tag_values']:
        ip_address = request.args.get('ip')
        if not ip_address:
            return jsonify({"message": "IP address parameter 'ip' is missing.", "error": "No IP provided"}), 400
        if not is_plc_connected(ip_address):
            return jsonify({"message": f"PLC with IP {ip_address} is not connected or not active.", "error": "PLC not connected"}), 400

@app.route('/insertDataToPlc', methods=['POST'])
@cross_origin()
def insert_data_to_plc():
    try:
        # Extract the PLC IP address from query parameters
        plc_ip = request.args.get('ip')
        data_list = request.json
        if not isinstance(data_list, list):
            raise ValueError("Payload must be a list of tag-value dictionaries.")

        write_operations = [(item['tag'], item['value']) for item in data_list if 'tag' in item and 'value' in item]

        start_time = time.time()
        batch_size = 10
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(batch_write, plc_ip, write_operations[i:i + batch_size]) for i in range(0, len(write_operations), batch_size)]
            for future in as_completed(futures):
                future.result()
        
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to write to PLC: {time_taken:.4f} seconds")

        if time_taken > 3:
            print("Custom Log: Writing to PLC took longer than 3 seconds.")
        
        return jsonify({"message": "Data written to PLC successfully.", "error": None}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred while writing data to PLC.", "error": str(e)}), 500

@app.route('/readDataTagsFromPlc', methods=['GET'])
@cross_origin()
def read_data_tags_from_plc():
    try:
        ip_address = request.args.get('ip')
        with PLC() as plc:
            plc.IPAddress = ip_address
            tags_response = plc.GetTagList()
            if tags_response is None or tags_response.Value is None:
                raise Exception("Failed to get tag list from PLC.")
            tag_names = [tag.TagName for tag in tags_response.Value]
        return jsonify({"tags": tag_names}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500

@app.route('/readDataFromPlcByTags', methods=['GET'])
@cross_origin()
def read_data_from_plc():
    try:
        ip_address = request.args.get('ip')
        start_time = time.time()
        results = batch_read(ip_address, tags_to_read, max_workers=50)
        end_time = time.time()
        print(f"Time taken to read from PLC: {end_time - start_time:.4f} seconds")
        return jsonify({"message": "Data read from PLC successfully.", "data": results, "error": None}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500

@app.route('/getTagValues', methods=['POST'])
@cross_origin()
def get_tag_values():
    try:
        ip_address = request.args.get('ip')
        tags_to_read = request.json.get('tags', [])
        if not tags_to_read:
            raise ValueError("No tags provided in the payload.")
        start_time = time.time()
        results = batch_read(ip_address, tags_to_read, max_workers=50)
        end_time = time.time()
        print(f"Time taken to read from PLC: {end_time - start_time:.4f} seconds")
        return jsonify({"message": "Data read from PLC successfully.", "data": results, "error": None}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8083)

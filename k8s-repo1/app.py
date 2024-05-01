import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

directory_path = "/Ahar_PV_dir/"


def store_data_in_file(filename, data):
    try:

        with open(os.path.join(directory_path, filename), "w+") as file:
            file.write(data)
        return True

    except Exception as e:
        return False


@app.route("/store-file", methods=["POST"])
def store_file():

    if request.is_json:

        request_data = request.get_json()
        file_name = request_data.get("file")
        data = request_data.get("data")

        if file_name is not None:

            if store_data_in_file(file_name, data):
                response = {"file": file_name, "message": "Success."}
                return jsonify(response), 200

            else:
                response = {
                    "file": file_name,
                    "error": "Error while storing the file to the storage."
                }

                return jsonify(response), 500

        else:
            response = {"file": None, "error": "Invalid JSON input."}
            return jsonify(response), 400

    else:

        response = {"file": None, "error": "Invalid JSON input."}
        return jsonify(response), 400

#calling the method in second container
@app.route("/get-temperature", methods=["POST"])
def get_temp():

    if request.is_json:

        request_data = request.get_json()

        response = requests.post(
            "http://app2-deployment-service:6001/get-temperature", json=request_data
        )

    return response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)

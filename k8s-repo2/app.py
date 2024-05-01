import os
from flask import Flask, request, jsonify

app = Flask(__name__)

DIRECTORY = "/Ahar_PV_dir/"


def get_file_headers(file_path):

    with open(file_path, "r") as f:

        headers_line = f.readline().strip()
        headers = [header.strip() for header in headers_line.split(",")]

        return headers


@app.route("/get-temperature", methods=["POST"])
def get_temperature():

    data = request.json
    file = data.get("file")
    name = data.get("name")

    if not file or not name:
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

    try:
        with open(os.path.join(DIRECTORY, file), "r") as f:
            lines = f.readlines()

        # headers = [header.strip() for header in lines[0].split(",")]
        headers = lines[0].strip().split(",")
        temp = 0
        temp_index = headers.index("temperature")

        if temp_index == -1:

            raise ValueError("Invalid JSON input.")

        for line in lines[1:]:

            values = line.strip().split(",")

            if values[0] == name:

                temp = int(values[temp_index].strip())

        return jsonify({
            "file": file,
            "temperature": temp
        }), 200

    except ValueError as e:

        if "temperature" not in headers:
            return jsonify({
                "file": file,
                "error": "Input file not in CSV format."
            }), 400

        else:
            return jsonify({
                "file": file,
                "error": str(e)
            }), 400

    except FileNotFoundError:

        return jsonify({
            "file": file,
            "error": "File not found."
        }), 404

    except Exception as e:

        return jsonify({
            "file": file,
            "error": "Input file not in CSV format."
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, debug=True)

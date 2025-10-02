import json
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)


@app.route('/canteens', methods=['GET'])
def get_canteens():
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM CANTEEN")
    canteens = c.fetchall()
    conn.close()

    canteens_list = []
    for canteen in canteens:
        canteen_dict = {
            'ID': canteen[0],
            'Name': canteen[1],
            'Location': canteen[2],
            'time_open': canteen[3],
            'time_closed': canteen[4]
        }
        canteens_list.append(canteen_dict)

    return jsonify(canteens_list)


@app.route('/canteens/<time_open>-<time_closed>', methods=['GET'])
def get_canteens_by_time(time_open, time_closed):
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM CANTEEN")
    canteens = c.fetchall()
    conn.close()

    format_time_open_input = datetime.strptime(time_open, '%H:%M')
    format_time_closed_input = datetime.strptime(time_closed, '%H:%M')
    time_filtered_canteens = []
    for canteen in canteens:
        format_time_open = datetime.strptime(canteen[3], '%H:%M')
        format_time_closed = datetime.strptime(canteen[4], '%H:%M')
        if format_time_open <= format_time_open_input and format_time_closed >= format_time_closed_input:
            canteen_dict = {
                'ID': canteen[0],
                'Name': canteen[1],
                'Location': canteen[2],
                'time_open': canteen[3],
                'time_closed': canteen[4]
            }
            time_filtered_canteens.append(canteen_dict)

    return jsonify(time_filtered_canteens)


@app.route('/canteens', methods=['POST'])
def add_canteen():
    data = request.get_json()
    name = data.get("Name")
    location = data.get("Location")
    time_open = data.get("time_open")
    time_closed = data.get("time_closed")

    if not name or not location or not time_open or not time_closed:
        return jsonify({'Message': 'Missing required data!'}), 400

    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("INSERT INTO CANTEEN (Name, Location, time_open, time_closed) VALUES (?, ?, ?, ?)",
              (name, location, time_open, time_closed))
    conn.commit()
    conn.close()

    return jsonify({'Message': 'Canteen added successfully!'}), 200


@app.route('/canteens/<canteen_id>', methods=['PUT'])
def update_canteen(canteen_id):
    data = request.get_json()
    name = data.get("Name")
    location = data.get("Location")
    time_open = data.get("time_open")
    time_closed = data.get("time_closed")

    if not canteen_id.isdigit():
        return jsonify({'Message': 'Invalid canteen ID format!'}), 400

    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM CANTEEN WHERE ID = ?", (canteen_id,))
    canteen = c.fetchall()

    if not canteen:
        return jsonify({'Message': 'Canteen with this ID does not exist!'}), 400

    c.execute("UPDATE CANTEEN SET Name = ?, Location = ?, time_open = ?, time_closed = ? WHERE ID = ?",
              (name, location, time_open, time_closed, canteen_id))

    conn.commit()
    conn.close()

    return jsonify({'Message': 'Canteen updated successfully!'}), 200


@app.route('/canteens/<canteen_id>', methods=['DELETE'])
def delete_canteen(canteen_id):

    if not canteen_id.isdigit():
        return jsonify({'Message': 'Invalid canteen ID format!'}), 400

    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM CANTEEN WHERE ID = ?", (canteen_id,))
    canteen = c.fetchall()

    if not canteen:
        return jsonify({'Message': 'Canteen with this ID does not exist!'}), 400

    c.execute('DELETE FROM CANTEEN WHERE ID = ?', (canteen_id,))
    conn.commit()
    conn.close()

    return jsonify({'Message': 'Canteen deleted successfully!'}), 200


if __name__ == '__main__':
    app.run(debug=True)

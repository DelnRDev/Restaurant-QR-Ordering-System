from flask import Flask, jsonify, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "telemetry.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Telemetry server is running."


@app.route("/temperature", methods=["POST"])
def receive_temperature():

    data = request.get_json()

    temperature = data["temperature"]
    created_at = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO temperature_readings
        (temperature, created_at)
        VALUES (?, ?)
        """,
        (temperature, created_at)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "saved",
        "temperature": temperature,
        "created_at": created_at
    })


@app.route("/temperature", methods=["GET"])
def get_temperatures():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, temperature, created_at
        FROM temperature_readings
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    readings = []

    for row in rows:
        readings.append({
            "id": row[0],
            "temperature": row[1],
            "created_at": row[2]
        })

    return jsonify(readings)


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT temperature, created_at
        FROM temperature_readings
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    html = """
    <html>
    <head>
        <title>Temperature Dashboard</title>
    </head>
    <body>

        <h1>Temperature Dashboard</h1>

        <table border="1" cellpadding="5">
            <tr>
                <th>Temperature (°C)</th>
                <th>Timestamp</th>
            </tr>

            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
            </tr>
            {% endfor %}

        </table>

    </body>
    </html>
    """

    return render_template_string(html, rows=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
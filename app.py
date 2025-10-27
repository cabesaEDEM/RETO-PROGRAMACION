import os, time, psycopg
from flask import Flask, jsonify

app = Flask(__name__)
url = os.getenv("DATABASE_URL")

def get_connection():
    for i in range(30):
        try:
            return psycopg.connect(url)
        except Exception as e:
            print(f"[DB] Esperando BD… intento {i+1}/30: {e}")
            time.sleep(1.0)
    raise RuntimeError("No se pudo conectar a la BD")

@app.route("/")
def home():
    return {"message": "API Rick & Morty lista"}

@app.route("/species")
def get_species():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT species, COUNT(*) FROM characters GROUP BY species;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = [{"species": s, "count": c} for s, c in rows]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
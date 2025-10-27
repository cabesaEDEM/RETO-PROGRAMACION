
# Reto: Rick & Morty + Base de Datos + Visualización

## 🎯 Objetivo del reto
Aprender a **conectar Python con una base de datos PostgreSQL** y **guardar información obtenida desde una API real**.

En este caso usaremos la **API pública de Rick & Morty**, cargaremos los personajes en una tabla `characters` y haremos un pequeño `SELECT` para comprobar que todo funciona.

> Este reto es  para practicar, explorar y reforzar lo aprendido.  
> Puedes hacerlo completo o hasta donde quieras.  
> Hay además **dos extras opcionales** para quienes quieran ir un paso más allá (IA o Data).

---

## 🪜 Paso a paso (reto base)

### 1️. Conexión con la base de datos
Usa `psycopg` (la librería oficial de PostgreSQL en Python) y la variable de entorno `DATABASE_URL` para conectarte.  
Haz que el script espere unos segundos si la base de datos aún no está lista.

```python
import os, psycopg
url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")
```

---

### 2️. Crear la tabla `characters`
Recrea la tabla (CREATE) con los siguientes campos:

```sql
id INTEGER PRIMARY KEY,
name TEXT,
status TEXT,
species TEXT,
type TEXT,
gender TEXT,
origin_name TEXT,
location_name TEXT,
image TEXT,
url TEXT,
created TIMESTAMPTZ
```

---

### 3️. Consumir la API de Rick & Morty
Haz una petición GET a:

```
https://rickandmortyapi.com/api/character
```

Descarga una (usando simplemente la url base) o varias páginas (según la variable `RM_PAGES`) y guarda los datos en la tabla.

Cada registro debe incluir:

- `id`
- `name`
- `status`
- `species`
- `type`
- `gender`
- `origin.name`
- `location.name`
- `image`
- `url`
- `created`

Inserta los datos con **INSERT normales** usando `cur.executemany()`.

---

### 4️. Comprobación con `fetchall()`
Haz un `SELECT` simple, por ejemplo:

```python
cur.execute("SELECT id, name, species FROM characters LIMIT 10;")
print(cur.fetchall())
```

Así podrás ver en consola los primeros personajes guardados en la base de datos.

---

### 5️. Cierra la conexión
Recuerda siempre cerrar correctamente el cursor y la conexión:

```python
connection.commit()
cur.close()
connection.close()
```
### 6. Sube tu reto a GitHub
Un miembro del equipo debe crear un repositorio en GitHub y añadir al resto de miembros del equipo de colaboradores. En este repositorio deberéis subir el trabajo. Diapositivas de ayuda para subir el trabajo [Diapositivas Git](https://marinadeempresas-my.sharepoint.com/:p:/g/personal/scpinilla_edem_es/EXLF_hosFdBGrxomRBcIXw4BrVLHWcDV-gOCGiuBJ0wdrw?e=Mi6d4S)  

---

## 💡 Extras opcionales
Estos extras **no son obligatorios**, pero son una buena forma de explorar herramientas que **verás más adelante en el máster**.

---

### ⭐ Extra 1 (para los de IA): Visualización con Matplotlib
👉 **Matplotlib** es una librería de Python para crear gráficos y visualizaciones.  
La usarás más adelante en el máster cuando veamos **ciencia de datos, análisis e IA**.

Para este reto, puedes probar a representar los datos que acabas de guardar:

```python
import matplotlib.pyplot as plt

cur.execute("SELECT species, COUNT(*) FROM characters GROUP BY species;")
rows = cur.fetchall()

species = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.bar(species, counts)
plt.title("Número de personajes por especie")
plt.xlabel("Especie")
plt.ylabel("Cantidad")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("grafico.png")

print("[OK] Gráfico guardado como grafico.png")
```

📊 Esto generará una imagen `grafico.png` con un gráfico de barras como el siguiente:

- **Eje X:** especies (Human, Alien, Robot, etc.)  
- **Eje Y:** cuántos personajes hay de cada una.

---

### ⭐ Extra 2 (para los de Data): API con Flask
👉 **Flask** es un *micro framework web* en Python que permite crear endpoints (rutas) y devolver datos en formato JSON.  
Lo verás más adelante en el máster cuando abordemos la parte de **backend y APIs**.

Puedes crear un archivo aparte llamado `app.py` con algo así:

```python
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
```

Luego podrás abrir [http://localhost:5000/species](http://localhost:5000/species)  
y ver un JSON como:

```json
[
  {"species": "Human", "count": 388},
  {"species": "Alien", "count": 50},
  {"species": "Robot", "count": 10}
]
```

---

## 🧩 Resumen rápido

| Nivel | Objetivo | Herramienta | Resultado |
|:------|:----------|:-------------|:------------|
| Base | Conexión, INSERT, SELECT | `psycopg` | Datos guardados en Postgres |
| Extra IA | Visualización | `matplotlib` | `grafico.png` con el recuento por especie |
| Extra Data | Endpoint web | `flask` | `GET /species` devuelve los datos en JSON |

---

## Equipos
### [Extensión VSC para trabajar en equipos](https://visualstudio.microsoft.com/es/services/live-share/)
GRUPO 1
Daniel – Adrián – Raúl

GRUPO 2
Jorge Albalat – Ignacio – Fátima

GRUPO 3
Gemma – Sergi – Jose

GRUPO 4
Carlos Beltrán – David – Juan Luis

GRUPO 5
Iñaki – Jorge Greus – Iván

GRUPO 6
Pau – Enrique – Javier López

GRUPO 7
Marina Azul – Alejandro – Antonio

GRUPO 8
Jorge Martínez – Félix – Silvia – Javier Gracia

GRUPO 9
Javier Plaza – Paola – Florencia - Celia

GRUPO 10
Salvador – Carlos Sevillano – Marta

## ENCUESTA Y VALORACIÓN

### Encuesta sobre el reto

[Encuesta sobre el Reto](https://docs.google.com/forms/d/e/1FAIpQLSfH0WB0oS04QVy2H-jzFKLGolYpjuXSNOncgYELvyDhbU9Jfg/viewform?usp=publish-editor)  

### QR Valoración Python

<img src="./qrpython.png" alt="QR Python" width="600">

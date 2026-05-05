from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# ======================
# AUTO-GENERAR BASE DE DATOS (IMPORTANTE PARA RENDER)
# ======================
if not os.path.exists("betanalytics.db"):
    import analisis
    analisis.ejecutar()

# ======================
# PAGINA PRINCIPAL
# ======================
@app.route("/", methods=["GET", "POST"])
def inicio():

    conexion = sqlite3.connect("betanalytics.db")
    conexion.row_factory = sqlite3.Row  # 👈 permite usar nombres de columnas
    cursor = conexion.cursor()

    buscar = ""

    if request.method == "POST":
        buscar = request.form["buscar"]

        cursor.execute("""
        SELECT * FROM jugadores
        WHERE Jugador LIKE ?
        ORDER BY Prob_Gol DESC
        """, ('%' + buscar + '%',))

    else:
        cursor.execute("""
        SELECT * FROM jugadores
        ORDER BY Prob_Gol DESC
        """)

    jugadores = cursor.fetchall()
    conexion.close()

    return render_template(
        "index.html",
        jugadores=jugadores,
        buscar=buscar
    )

# ======================
# PAGINA EQUIPOS
# ======================
@app.route("/equipos")
def equipos():

    conexion = sqlite3.connect("betanalytics.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM equipos
    ORDER BY Prob_Ganar DESC
    """)

    equipos = cursor.fetchall()
    conexion.close()

    return render_template(
        "equipos.html",
        equipos=equipos
    )

# ======================
# PAGINA GRAFICAS
# ======================
@app.route("/graficas")
def graficas():
    return render_template("graficas.html")

# ======================
# MAIN (IMPORTANTE PARA RENDER)
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
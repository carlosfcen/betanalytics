from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ======================
# CONEXION DB
# ======================

def get_db_connection():
    conn = sqlite3.connect("betanalytics.db")
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre
    return conn

# ======================
# PAGINA PRINCIPAL
# ======================

@app.route("/", methods=["GET", "POST"])
def inicio():

    conn = get_db_connection()

    buscar = ""

    if request.method == "POST":
        buscar = request.form["buscar"]

        jugadores = conn.execute("""
            SELECT * FROM jugadores
            WHERE Jugador LIKE ?
            ORDER BY Prob_Gol DESC
        """, ('%' + buscar + '%',)).fetchall()

    else:
        jugadores = conn.execute("""
            SELECT * FROM jugadores
            ORDER BY Prob_Gol DESC
        """).fetchall()

    # 🔥 TOP 5 RECOMENDADOS
    top_goleadores = conn.execute("""
        SELECT * FROM jugadores
        ORDER BY Prob_Gol DESC
        LIMIT 5
    """).fetchall()

    top_asistencias = conn.execute("""
        SELECT * FROM jugadores
        ORDER BY Prob_Asistencia DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        jugadores=jugadores,
        buscar=buscar,
        top_goleadores=top_goleadores,
        top_asistencias=top_asistencias
    )

# ======================
# PAGINA EQUIPOS
# ======================

@app.route("/equipos")
def equipos():

    conn = get_db_connection()

    equipos = conn.execute("""
        SELECT * FROM equipos
        ORDER BY Prob_Ganar DESC
    """).fetchall()

    conn.close()

    return render_template(
        "equipos.html",
        equipos=equipos
    )

# ======================
# GRAFICAS
# ======================

@app.route("/graficas")
def graficas():
    return render_template("graficas.html")

# ======================
# RUN
# ======================

if __name__ == "__main__":
    app.run(debug=True)
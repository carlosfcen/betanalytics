import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. CARGA Y LIMPIEZA
# =========================

def cargar_datos():
    df = pd.read_csv("jugadores.csv")
    return df

def limpiar_datos(df):
    df = df.drop_duplicates()
    df = df.dropna()
    return df

# =========================
# 2. FEATURE ENGINEERING (SEGURO)
# =========================

def calcular_metricas(df):

    # evitar division por cero
    df["Partidos"] = df["Partidos"].replace(0, 1)

    # asegurar columnas existentes
    if "Goles" not in df.columns:
        df["Goles"] = 0

    if "Asistencias" not in df.columns:
        df["Asistencias"] = 0

    df["Prom_Goles"] = df["Goles"] / df["Partidos"]

    df["Prob_Gol"] = (1 - np.exp(-df["Prom_Goles"])) * 100
    df["Prom_Asistencias"] = df["Asistencias"] / df["Partidos"]

    df["Prob_Asistencia"] = (1 - np.exp(-df["Prom_Asistencias"])) * 100

    df["Prob_Gol"] = df["Prob_Gol"].fillna(0).round(0).astype(int)
    df["Prob_Asistencia"] = df["Prob_Asistencia"].fillna(0).round(0).astype(int)

    return df

# =========================
# 3. ANALISIS EQUIPOS
# =========================

def analizar_equipos(df):

    equipos = df.groupby("Equipo").agg({
        "Goles": "sum",
        "Asistencias": "sum",
        "Partidos": "sum"
    }).reset_index()

    equipos["Partidos"] = equipos["Partidos"].replace(0, 1)

    equipos["Prom_Equipo"] = (
        (equipos["Goles"] + equipos["Asistencias"]) /
        equipos["Partidos"]
    )

    equipos["Prob_Ganar"] = (1 - np.exp(-equipos["Prom_Equipo"])) * 100
    equipos["Prob_Empatar"] = equipos["Prob_Ganar"] * 0.25
    equipos["Prob_Perder"] = 100 - (
        equipos["Prob_Ganar"] + equipos["Prob_Empatar"]
    )

    equipos["Prob_Ganar"] = equipos["Prob_Ganar"].round(0).astype(int)
    equipos["Prob_Empatar"] = equipos["Prob_Empatar"].round(0).astype(int)
    equipos["Prob_Perder"] = equipos["Prob_Perder"].round(0).astype(int)

    return equipos

# =========================
# 4. GRAFICAS
# =========================

def generar_graficas(df, equipos):

    plt.figure()
    plt.scatter(df["Partidos"], df["Goles"])
    plt.title("Relación partidos vs goles")
    plt.savefig("static/grafica_goles.png")
    plt.close()

    plt.figure()
    plt.hist(df["Goles"], bins=10)
    plt.title("Distribución de goles")
    plt.savefig("static/hist_goles.png")
    plt.close()

    top = equipos.sort_values("Prob_Ganar", ascending=False).head(10)

    plt.figure(figsize=(10,5))
    plt.bar(top["Equipo"], top["Prob_Ganar"])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/grafica_equipos.png")
    plt.close()

# =========================
# 5. GUARDAR DB (CRÍTICO)
# =========================

def guardar_db(df, equipos):

    conn = sqlite3.connect("betanalytics.db")

    # fuerza tipos consistentes
    df.to_sql("jugadores", conn, if_exists="replace", index=False)
    equipos.to_sql("equipos", conn, if_exists="replace", index=False)

    conn.close()

# =========================
# MAIN
# =========================

def ejecutar():
    df = cargar_datos()
    df = limpiar_datos(df)
    df = calcular_metricas(df)
    equipos = analizar_equipos(df)

    generar_graficas(df, equipos)
    guardar_db(df, equipos)

    print("Proyecto listo correctamente")

if __name__ == "__main__":
    ejecutar()
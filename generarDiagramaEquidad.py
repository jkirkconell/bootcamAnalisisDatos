import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


sns.set(style="whitegrid")


DATA_PATH = os.path.join("data", "sports.csv")


df = pd.read_csv(DATA_PATH)

# Filtrar filas con participación registrada
df_gendered = df[(df["sum_partic_men"] > 0) | (df["sum_partic_women"] > 0)].copy()

# Calcular totales y proporciones por género
df_gendered["partic_total"] = df_gendered["sum_partic_men"] + df_gendered["sum_partic_women"]
df_gendered["rev_total"] = df_gendered["rev_men"].fillna(0) + df_gendered["rev_women"].fillna(0)
df_gendered["exp_total"] = df_gendered["exp_men"].fillna(0) + df_gendered["exp_women"].fillna(0)

df_gendered["partic_women_pct"] = (df_gendered["sum_partic_women"] / df_gendered["partic_total"])
df_gendered["rev_women_pct"] = df_gendered["rev_women"].fillna(0) / df_gendered["rev_total"]
df_gendered["exp_women_pct"] = df_gendered["exp_women"].fillna(0) / df_gendered["exp_total"]

# Agrupar por año y calcular promedios
summary_by_year = df_gendered.groupby("year")[
    ["partic_women_pct", "rev_women_pct", "exp_women_pct"]
].mean().reset_index()

# Visualización
plt.figure(figsize=(10, 6))
plt.plot(summary_by_year["year"], summary_by_year["partic_women_pct"], label="% Participación Femenina")
plt.plot(summary_by_year["year"], summary_by_year["rev_women_pct"], label="% Ingresos para Mujeres")
plt.plot(summary_by_year["year"], summary_by_year["exp_women_pct"], label="% Gastos para Mujeres")

plt.title("¿Hay equidad de género en la inversión deportiva universitaria?")
plt.ylabel("Proporción")
plt.xlabel("Año")
plt.legend()
plt.tight_layout()


os.makedirs("outputs", exist_ok=True)
plt.savefig(os.path.join("outputs", "equidad_genero.png"))

plt.show()

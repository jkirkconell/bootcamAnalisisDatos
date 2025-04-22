import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


df = pd.read_csv("data/sports.csv")


df_gendered = df[
    (df["sum_partic_men"] > 0) & (df["sum_partic_women"] > 0) &
    (df["exp_men"] > 0) & (df["exp_women"] > 0)
].copy()

# Calcular gasto por atleta
df_gendered["gasto_por_hombre"] = df_gendered["exp_men"] / df_gendered["sum_partic_men"]
df_gendered["gasto_por_mujer"] = df_gendered["exp_women"] / df_gendered["sum_partic_women"]
df_gendered["brecha_absoluta"] = df_gendered["gasto_por_hombre"] - df_gendered["gasto_por_mujer"]
df_gendered["razon_equidad"] = df_gendered["gasto_por_mujer"] / df_gendered["gasto_por_hombre"]

# Agrupación por institución
institucion_brecha = df_gendered.groupby("institution_name")[[
    "gasto_por_hombre", "gasto_por_mujer", "brecha_absoluta", "razon_equidad"
]].mean().reset_index()

# Mostrar top 5 instituciones con mayor brecha a favor de hombres
print("Top 5 instituciones con mayor brecha a favor de hombres:")
print(institucion_brecha.sort_values(by="brecha_absoluta", ascending=False).head())

# Mostrar top 5 instituciones con mayor equidad (razón cercana a 1)
print("\nTop 5 instituciones más equitativas en gasto:")
print(institucion_brecha.loc[(institucion_brecha["razon_equidad"] < 2)].sort_values(
    by="razon_equidad", ascending=False).head())

# Filtrar último año disponible
ultimo_anio = df_gendered["year"].max()
df_ultimo = df_gendered[df_gendered["year"] == ultimo_anio]

# Histograma de la razón de equidad por institución
plt.figure(figsize=(10, 6))
sns.histplot(df_ultimo["razon_equidad"], bins=40, kde=True, color="skyblue")
plt.axvline(1, color="red", linestyle="--", label="Equidad perfecta")
plt.title(f"Distribución de equidad en gasto por atleta - {ultimo_anio}")
plt.xlabel("Razón de Equidad (mujer/hombre)")
plt.ylabel("Cantidad de instituciones")
plt.legend()
plt.tight_layout()


os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/histograma_equidad_instituciones.png")
plt.show()

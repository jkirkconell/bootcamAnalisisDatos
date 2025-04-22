import pandas as pd
import os


data_path = os.path.join("data", "sports.csv")


df = pd.read_csv(data_path)


df_copy = df.copy()


df_gendered = df_copy[
    (df_copy["sum_partic_men"] > 0) | (df_copy["sum_partic_women"] > 0)
].copy()


df_gendered["partic_total"] = df_gendered["sum_partic_men"] + df_gendered["sum_partic_women"]
df_gendered["rev_total"] = df_gendered["rev_men"].fillna(0) + df_gendered["rev_women"].fillna(0)
df_gendered["exp_total"] = df_gendered["exp_men"].fillna(0) + df_gendered["exp_women"].fillna(0)


df_gendered["partic_men_pct"] = df_gendered["sum_partic_men"] / df_gendered["partic_total"]
df_gendered["partic_women_pct"] = df_gendered["sum_partic_women"] / df_gendered["partic_total"]
df_gendered["rev_men_pct"] = df_gendered["rev_men"].fillna(0) / df_gendered["rev_total"]
df_gendered["rev_women_pct"] = df_gendered["rev_women"].fillna(0) / df_gendered["rev_total"]
df_gendered["exp_men_pct"] = df_gendered["exp_men"].fillna(0) / df_gendered["exp_total"]
df_gendered["exp_women_pct"] = df_gendered["exp_women"].fillna(0) / df_gendered["exp_total"]


summary_by_year = df_gendered.groupby("year")[
    ["partic_women_pct", "rev_women_pct", "exp_women_pct"]
].mean().reset_index()


print("Resumen anual de participación e inversión femenina:")
print(summary_by_year.head())
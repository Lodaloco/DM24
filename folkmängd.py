import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


file_path = "folkmängd.csv" 
df_population = pd.read_csv(file_path, encoding="latin1")

# Filtrera data för åren 2000-2023
df_population = df_population[df_population["år"].between(2000, 2023)]

# Ta bort länskoder från "region"-kolumnen så att den matchar olycksdata, irrelevant
df_population["region"] = df_population["region"].str.split(" ", n=1).str[1]  # Tar bort länskoden

# Byt namn på kolumner för att matcha olycksdata
df_population.rename(columns={"region": "County", "år": "Year", "Folkmängd": "Population"}, inplace=True)

# Ladda in olycksdata
accident_file = "bearbetad_data.xlsx"
df_accidents = pd.read_excel(accident_file, sheet_name="Rådata")

# Filtrera bort rader där "County" innehåller "Okänt" (som vi gjorde i den tidigare versionen av koden)
df_accidents = df_accidents[~df_accidents['County'].str.contains("Okänt", na=False)]

# Ta bort data för 2024 då vi saknar fullständig data, för att allt ska mätas konsekvent
df_accidents = df_accidents[df_accidents["Year"] <= 2023]

# Aggreggera olycksdata till årsnivå
df_accidents = df_accidents.groupby(["County", "Year"]).agg({"Quantity": "sum"}).reset_index()

# Slå ihop olycksdata med befolkningsdata
merged_df = df_accidents.merge(df_population, on=["County", "Year"], how="left")

# Beräkna olyckor per 1000 invånare
merged_df["Accidents_per_1000"] = (merged_df["Quantity"] / merged_df["Population"]) * 1000

# Skapa statistik per år och län
yearly_stats = merged_df.groupby(["County", "Year"]).agg(
    skadade_per_1000=("Accidents_per_1000", "sum")
).reset_index()

# Förutsäga olyckor per 1000 invånare fram till 2028 med linjär regression
future_years = np.array(range(2024, 2029)).reshape(-1, 1)

predictions = []

if not yearly_stats.empty:
    for year in future_years.flatten():
        for county in yearly_stats["County"].unique():
            subset = yearly_stats[yearly_stats["County"] == county]
            if subset.shape[0] > 1:  # Kontrollera att det finns tillräckligt med data för att träna modellen
                X = subset["Year"].values.reshape(-1, 1)
                y = subset["skadade_per_1000"].values
                
                model = LinearRegression()
                model.fit(X, y)
                future_pred = model.predict([[year]])[0]
                
                predictions.append([county, year, future_pred])

# Skapa en DataFrame för prognosen om vi har några värden
if predictions:
    predictions_df = pd.DataFrame(predictions, columns=["County", "Year", "Predicted_skadade_per_1000"])
else:
    predictions_df = pd.DataFrame(columns=["County", "Year", "Predicted_skadade_per_1000"])

# Beräkna förändringen från 2024 till 2028 per län
df_pivot = predictions_df.pivot(index="County", columns="Year", values="Predicted_skadade_per_1000")
df_pivot["Change"] = df_pivot[2028] - df_pivot[2024]

# Hämta de fem län med störst förändring
top_5_counties = df_pivot["Change"].nlargest(5)
top_5_counties_list = top_5_counties.index.tolist()

# Filtrera data för dessa län
df_top5 = predictions_df[predictions_df["County"].isin(top_5_counties_list)]

# Skapa linjediagram
plt.figure(figsize=(10, 6))

# Plotta varje läns utveckling över åren
for county in top_5_counties_list:
    county_data = df_top5[df_top5["County"] == county]
    plt.plot(county_data["Year"], county_data["Predicted_skadade_per_1000"], marker="o", linestyle="-", label=county)

# Anpassa diagrammet
plt.legend()
plt.title("Prognos: Skadade per 1000 invånare per län (2024-2028)")
plt.xlabel("År")
plt.ylabel("Predicerade skadade per 1000 invånare")
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()

# Spara den sammanfogade datan och prognosen till en ny Excel-fil
output_file = "kombinerad_data.xlsx"
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    merged_df.to_excel(writer, sheet_name="Kombinerad Data", index=False)
    yearly_stats.to_excel(writer, sheet_name="Årlig Statistik", index=False)
    if not predictions_df.empty:
        predictions_df.to_excel(writer, sheet_name="Prognos 2024-2028", index=False)

# Linjediagram för skadade per 1000 invånare per län
plt.figure(figsize=(12, 6))
for county in yearly_stats["County"].unique(): #yearly_stats["County"].unique():
    subset = yearly_stats[yearly_stats["County"] == county]
    plt.plot(subset["Year"], subset["skadade_per_1000"], label=county)
plt.legend()
plt.title("Linjediagram: Skadade per 1000 invånare per län (2000-2023)")
plt.xlabel("År")
plt.ylabel("Skadade per 1000 invånare")
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()

# Horisontellt stapeldiagram för ett specifikt år (2023)
year_2023 = yearly_stats[yearly_stats["Year"] == 2023]
year_2023 = year_2023.sort_values(by="skadade_per_1000", ascending=False)
plt.figure(figsize=(12, 6))
plt.barh(year_2023["County"], year_2023["skadade_per_1000"], color="skyblue")
plt.title("Skadade per 1000 invånare per län (2023)")
plt.xlabel("Skadade per 1000 invånare")
plt.ylabel("Län")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# Linjediagram för prognos 2024-2028 (Maskininlärning)
plt.figure(figsize=(12, 6))
for county in predictions_df["County"].unique():
    subset = predictions_df[predictions_df["County"] == county]
    plt.plot(subset["Year"], subset["Predicted_skadade_per_1000"], linestyle="--", marker="o", label=county)
plt.legend()
plt.title("Prognos: Skadade per 1000 invånare per län (2024-2028)")
plt.xlabel("År")
plt.ylabel("Predicerade skadade per 1000 invånare")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()



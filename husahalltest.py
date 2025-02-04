import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Läs in Excel-filen
file_path = "bearbetad_data.xlsx"
xls = pd.ExcelFile(file_path)


df = pd.read_excel(xls, sheet_name="Rådata")

#Filtrera bort rader där "County" innehåller "Okänt"
df = df[~df['County'].str.contains("Okänt", na=False)]

# Ta bort kolumnen "Severity" om den finns
df = df.drop(columns=["Severity"], errors="ignore")

# 🔹 Klustring av län baserat på olycksnivå
county_accidents = df.groupby("County")["Quantity"].sum().reset_index()

# Standardisera datan
scaler = StandardScaler()
county_accidents["Quantity_Scaled"] = scaler.fit_transform(county_accidents[["Quantity"]])

# KMeans-klustring (3 kluster)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
county_accidents["Cluster"] = kmeans.fit_predict(county_accidents[["Quantity_Scaled"]])

# 🔹 Sortera klustrens nivåer
cluster_means = county_accidents.groupby("Cluster")["Quantity"].mean().sort_values()
sorted_clusters = {cluster_means.index[0]: "Lågrisk",
                   cluster_means.index[1]: "Mellannivå",
                   cluster_means.index[2]: "Högrisk"}

county_accidents["Cluster_Label"] = county_accidents["Cluster"].map(sorted_clusters)

# 🔹 Statistik per kluster
cluster_stats = county_accidents.groupby("Cluster_Label")["Quantity"].agg(["mean", "std", "count"])
print("📊 Statistik per kluster:\n", cluster_stats)

# 🔹 Scatterplot för klustringen
plt.figure(figsize=(10, 6))
cluster_colors = {"Lågrisk": "green", "Mellannivå": "orange", "Högrisk": "red"}
for label, color in cluster_colors.items():
    subset = county_accidents[county_accidents["Cluster_Label"] == label]
    plt.scatter(subset["County"], subset["Quantity"], label=label, color=color, edgecolors="black")

plt.title("Klustring av län baserat på antal olyckor", fontsize=14)
plt.xlabel("Län", fontsize=12)
plt.ylabel("Totalt antal olyckor", fontsize=12)
plt.xticks(rotation=90)
plt.legend(title="Risknivå")
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 🔹 Linjediagram för de 10 största länen
top_10_counties = [
    "Skåne län", "Stockholms län", "Västra Götalands län",
    "Västerbottens län", "Östergötlands län", "Västmanlands län",
    "Hallands län", "Värmlands län", "Västernorrlands län", "Jönköpings län"
]

df_top_10 = df[df["County"].isin(top_10_counties)]

df_filtered = df_top_10[~df_top_10["Year"].isin([2000, 2024])]  # Tar bort åren 2000 och 2024

yearly_accidents_top_10 = df_filtered.groupby(["Year", "County"])["Quantity"].sum().unstack()

#yearly_accidents_top_10 = df_top_10.groupby(["Year", "County"])["Quantity"].sum().unstack()

# Exkludera första och sista kolumnen
#filtered_columns = yearly_accidents_top_10.columns[1:-1]

plt.figure(figsize=(12, 6))
# Loopa igenom de filtrerade kolumnerna
""" for county in filtered_columns:
    plt.plot(yearly_accidents_top_10.index, yearly_accidents_top_10[county], marker="o", label=county)
 """
# Exkludera åren 2000 och 2024
#filtered_columns = yearly_accidents_top_10.drop(columns=[2000, 2024])

# Loopa igenom de filtrerade kolumnerna
for county in yearly_accidents_top_10.columns:
    plt.plot(yearly_accidents_top_10.index, yearly_accidents_top_10[county], marker="o", label=county)

plt.title("Antal trafikolyckor per år - 10 största länen", fontsize=14)
plt.xlabel("År", fontsize=12)
plt.ylabel("Antal olyckor", fontsize=12)
plt.legend(title="Län", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🔹 Regression för framtida olycksprognoser
df_yearly = df.groupby("Year")["Quantity"].sum().reset_index()

X = df_yearly["Year"].values.reshape(-1, 1)
y = df_yearly["Quantity"].values

model = LinearRegression()
model.fit(X, y)

future_years = np.array(range(df_yearly["Year"].max() + 1, df_yearly["Year"].max() + 6)).reshape(-1, 1)
future_predictions = model.predict(future_years)

# 🔹 Skapa en DataFrame för framtida olycksprognoser
future_df = pd.DataFrame({
    "Year": future_years.flatten(),
    "Quantity": [None] * len(future_years),  # Ingen faktisk data
    "Prediction": future_predictions  # Förutsägelser
})

# 🔹 Slå ihop historisk data och framtida prognoser
df_regression = pd.concat([df_yearly, future_df], ignore_index=True)

# 🔹 Plotta regressionen
plt.figure(figsize=(10, 5))
plt.scatter(df_yearly["Year"], df_yearly["Quantity"], color="blue", label="Historiska data")
plt.plot(df_yearly["Year"], model.predict(X), color="red", linestyle="--", label="Trendlinje")
plt.plot(future_years, future_predictions, color="green", linestyle="--", label="Prognos (5 år framåt)")

plt.title("Förutsägelse av trafikolyckor (linjär regression)", fontsize=14)
plt.xlabel("År", fontsize=12)
plt.ylabel("Antal olyckor", fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# 🔹 korrigerad kod-->spara
with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Rådata", index=False)
    county_accidents.to_excel(writer, sheet_name="Klustring av län", index=False)
    df_regression.to_excel(writer, sheet_name="Regression (Olycksprognos)", index=False)



# Ta bort skadade kolumnen, för den tillför inga unika värden. enl dokumentationen för kolumnen skulle den datan vara specifik.
# Räkna ut procentull fördelning av dom olika typerna av olyckor per län
# Vi vill ta bort "okända" för den datan är inte användbar
#Har kollat  https://www.dataportal.se/datasets/272_5269 men inte hittat något mer användbart. 
#Klustring av grupper (län)
#Visualisera data med hjälp av nya diagram t.ex--> årsvis redovisning av olyckor (10 mest olycksdrabbade länen)
#Har undersökt SMHI öppen data för att försöka kombinera--> Deras data är utformad på ett helt annat sätt och inte applicerbar för oss.
#Nedan dom län med flest olyckor 

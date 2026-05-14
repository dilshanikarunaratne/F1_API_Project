from extract import get_race_results
from transform import clean_race_results


season = 2024

df_raw = get_race_results(season)
df_clean = clean_race_results(df_raw)

df_raw.to_csv(f"C:/Users/Dilshani/Documents/F1_API_Project/data/raw/f1_results_{season}_raw.csv", index=False)
df_clean.to_csv(f"C:/Users/Dilshani/Documents/F1_API_Project/data/processed/f1_results_{season}_clean.csv", index=False)

print("Pipeline completed.")
print(df_clean.head())
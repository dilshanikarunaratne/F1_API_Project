import requests
import pandas as pd


def get_race_results(season=2024):
    url = f"https://api.jolpi.ca/ergast/f1/{season}/results.json?limit=1000"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    races = data["MRData"]["RaceTable"]["Races"]

    rows = []

    for race in races:
        race_name = race["raceName"]
        round_no = race["round"]
        circuit_name = race["Circuit"]["circuitName"]
        date = race["date"]

        for result in race["Results"]:
            rows.append({
                "season": season,
                "round": round_no,
                "race_name": race_name,
                "circuit": circuit_name,
                "date": date,
                "position": result["position"],
                "driver_code": result["Driver"].get("code"),
                "driver_name": result["Driver"]["givenName"] + " " + result["Driver"]["familyName"],
                "constructor": result["Constructor"]["name"],
                "grid": result["grid"],
                "laps": result["laps"],
                "status": result["status"],
                "points": result["points"]
            })

    return pd.DataFrame(rows)
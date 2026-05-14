import requests
import json

url = "https://api.jolpi.ca/ergast/f1/2024/results.json?limit=1"

response = requests.get(url)

data = response.json()

print(json.dumps(data, indent=2))
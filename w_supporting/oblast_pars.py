import json
import requests

url = "https://raw.githubusercontent.com/EugeneBorshch/ukraine_geojson/master/UA_FULL_Ukraine.geojson"

response = requests.get(url)
data = response.json()

results = []

for feature in data["features"]:
    properties = feature["properties"]
    item = {
        "koatuu": properties.get("koatuu", ""),
        "name": properties.get("name", ""),
        "name:en": properties.get("name:en", "")
    }
    results.append(item)

with open("parsed_ukraine_geojson.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("ready")
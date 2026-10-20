import json
import os
import sys
import urllib.request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from adapters.base_adapter import BaseAdapter


class WorldBankAdapter(BaseAdapter):
    def __init__(self):
        self.name = "WorldBankAdapter"
        self.overview_file = "data/indicators/india-overview.json"

    def _fetch_latest_non_null(self, indicator_code):
        # API results are newest-first; skip years whose values are still null.
        url = (
            "https://api.worldbank.org/v2/country/IN/indicator/"
            f"{indicator_code}?format=json&per_page=100"
        )
        request = urllib.request.Request(url)
        request.add_header("User-Agent", "IndiaMetrix-DataBot/1.0")
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
            raise RuntimeError(f"Unexpected World Bank API response for {indicator_code}")
        for observation in payload[1]:
            if isinstance(observation, dict) and observation.get("value") is not None and observation.get("date"):
                return {"value": float(observation["value"]), "year": str(observation["date"])}
        return None

    def fetch(self):
        """Fetch the latest published non-null population and nominal GDP values."""
        data = {}
        for indicator_id, code in {
            "population": "SP.POP.TOTL",
            "gdp-current-usd": "NY.GDP.MKTP.CD",
        }.items():
            observation = self._fetch_latest_non_null(code)
            if observation is not None:
                data[indicator_id] = observation
        if not data:
            raise RuntimeError("World Bank API returned no usable population or GDP observations")
        return data

    def update_local_data(self, fetched_data):
        if not os.path.exists(self.overview_file):
            raise FileNotFoundError(f"[{self.name}] Overview file not found: {self.overview_file}")
        with open(self.overview_file, "r", encoding="utf-8") as f:
            local_data = json.load(f)

        updated = False
        for item in local_data.get("indicators", []):
            indicator_id = item.get("id")
            if indicator_id not in fetched_data:
                continue
            fetched_year = int(fetched_data[indicator_id]["year"])
            fetched_value = float(fetched_data[indicator_id]["value"])
            local_year = int(item["year"])
            local_value = float(item["value"])
            if fetched_year > local_year or (fetched_year == local_year and fetched_value != local_value):
                print(f"[{self.name}] Updating {indicator_id}: {local_value} ({local_year}) -> {fetched_value} ({fetched_year})")
                item["year"] = fetched_year
                item["value"] = fetched_value
                if indicator_id == "population":
                    billions = fetched_value / 1_000_000_000
                    item["display"]["en"] = f"{billions:.2f} billion"
                    item["display"]["hi"] = f"{billions:.2f} अरब"
                elif indicator_id == "gdp-current-usd":
                    trillions = fetched_value / 1_000_000_000_000
                    item["display"]["en"] = f"${trillions:.2f} trillion"
                    item["display"]["hi"] = f"${trillions:.2f} ट्रिलियन"
                updated = True
        if updated:
            with open(self.overview_file, "w", encoding="utf-8") as f:
                json.dump(local_data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        return updated

import urllib.request
import json
import os
import sys

# Ensure we can import from parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from adapters.base_adapter import BaseAdapter

class WorldBankAdapter(BaseAdapter):
    def __init__(self):
        self.name = "WorldBankAdapter"
        self.overview_file = "data/indicators/india-overview.json"
        
    def fetch(self):
        """Fetch latest Population and GDP from World Bank API for India."""
        # SP.POP.TOTL = Total Population
        # NY.GDP.MKTP.CD = GDP (current US$)
        
        data = {}
        
        # Fetch Population
        req = urllib.request.Request("http://api.worldbank.org/v2/country/IN/indicator/SP.POP.TOTL?format=json&per_page=1")
        req.add_header('User-Agent', 'IndiaMetrix-DataBot/1.0')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            if isinstance(res, list) and len(res) > 1 and isinstance(res[1], list) and len(res[1]) > 0:
                latest = res[1][0]
                if isinstance(latest, dict) and latest.get('value') is not None:
                    data['population'] = {
                        'value': latest['value'],
                        'year': latest['date']
                    }
                    
        # Fetch GDP
        req = urllib.request.Request("http://api.worldbank.org/v2/country/IN/indicator/NY.GDP.MKTP.CD?format=json&per_page=1")
        req.add_header('User-Agent', 'IndiaMetrix-DataBot/1.0')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            if isinstance(res, list) and len(res) > 1 and isinstance(res[1], list) and len(res[1]) > 0:
                latest = res[1][0]
                if isinstance(latest, dict) and latest.get('value') is not None:
                    data['gdp-current-usd'] = {
                        'value': latest['value'],
                        'year': latest['date']
                    }
                    
        return data

    def update_local_data(self, fetched_data):
        if not os.path.exists(self.overview_file):
            print(f"[{self.name}] Overview file not found.")
            return False
            
        with open(self.overview_file, "r", encoding="utf-8") as f:
            local_data = json.load(f)
            
        updated = False
        
        for item in local_data['indicators']:
            ind_id = item['id']
            if ind_id in fetched_data:
                fetched_year = fetched_data[ind_id]['year']
                fetched_val = fetched_data[ind_id]['value']
                
                # Check if we have newer data based on year
                # OR if the year is the same but the value was revised
                if (int(fetched_year) > int(item['year'])) or (int(fetched_year) == int(item['year']) and float(fetched_val) != float(item['value'])):
                    print(f"[{self.name}] Updating {ind_id}: {item['value']} ({item['year']}) -> {fetched_val} ({fetched_year})")
                    item['year'] = fetched_year
                    item['value'] = fetched_val
                    
                    # Format value based on indicator
                    if ind_id == "population":
                        # Format as billions e.g. 1.43 billion
                        val_in_b = fetched_val / 1000000000
                        item['display']['en'] = f"{val_in_b:.2f} billion"
                        item['display']['hi'] = f"{val_in_b:.2f} अरब"
                    elif ind_id == "gdp-current-usd":
                        # Format as trillions e.g. $3.5 trillion
                        val_in_t = fetched_val / 1000000000000
                        item['display']['en'] = f"${val_in_t:.2f} trillion"
                        item['display']['hi'] = f"${val_in_t:.2f} ट्रिलियन"
                        
                    updated = True
                    
        if updated:
            with open(self.overview_file, "w", encoding="utf-8") as f:
                json.dump(local_data, f, indent=2, ensure_ascii=False)
                
        return updated

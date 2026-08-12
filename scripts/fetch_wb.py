import urllib.request
import json
import os
import time

def fetch_worldbank_indicators(limit=1000): # fetch list of 1000, we'll try to find 50 valid ones for now
    print("Fetching World Bank indicators list...")
    req = urllib.request.Request(f"http://api.worldbank.org/v2/indicator?format=json&per_page={limit}")
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        
    indicators = res[1]
    
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'indicators', 'worldbank')
    os.makedirs(out_dir, exist_ok=True)
    
    count = 0
    valid_count = 0
    for ind in indicators:
        ind_id = ind['id']
        ind_name = ind['name']
        
        # Now fetch data for India
        req_url = f"http://api.worldbank.org/v2/country/IN/indicator/{ind_id}?format=json&per_page=1"
        try:
            req = urllib.request.Request(req_url)
            with urllib.request.urlopen(req) as response:
                data_res = json.loads(response.read().decode())
                
                if isinstance(data_res, list) and len(data_res) > 1 and isinstance(data_res[1], list) and len(data_res[1]) > 0:
                    latest = data_res[1][0]
                    if latest.get('value') is not None:
                        # We have data!
                        val = latest['value']
                        year = latest['date']
                        
                        # Create JSON
                        out_json = {
                            "id": ind_id.lower().replace('.', '-'),
                            "category": "economy",
                            "name": {
                                "en": ind_name,
                                "hi": ind_name
                            },
                            "unit": "",
                            "geography_level": "country",
                            "geography_id": "india",
                            "year": year,
                            "value": val,
                            "display": {
                                "en": str(val),
                                "hi": str(val)
                            },
                            "source_id": "world-bank",
                            "source_url": "https://data.worldbank.org/indicator/" + ind_id,
                            "last_checked": "2026-08-12",
                            "last_updated": "2026-08-12",
                            "methodology_note": ind.get('sourceNote', ''),
                            "is_estimate": False
                        }
                        
                        filepath = os.path.join(out_dir, f"{out_json['id']}.json")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(out_json, f, indent=2, ensure_ascii=False)
                        valid_count += 1
                        print(f"Saved {valid_count}: {ind_name} ({ind_id})")
                        
                        # Let's limit to 50 real indicators so the user isn't waiting hours
                        if valid_count >= 50:
                            break
                            
        except Exception as e:
            # Silently skip failed API calls
            pass
            
        time.sleep(0.05) # Be nice to API

    print(f"Finished fetching {valid_count} REAL indicators.")

if __name__ == "__main__":
    fetch_worldbank_indicators()

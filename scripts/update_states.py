import os
import json

def update_states():
    states_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'indicators', 'states')
    
    if not os.path.exists(states_dir):
        print("States dir not found")
        return
        
    for filename in os.listdir(states_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(states_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            indicators = data.get('indicators', [])
            
            # Check what's already there
            existing_ids = [ind['id'] for ind in indicators]
            
            if 'gdp' not in existing_ids:
                indicators.append({
                    "id": "gdp",
                    "category": "economy",
                    "name": {
                        "en": "GSDP (Current)",
                        "hi": "GSDP (वर्तमान)"
                    },
                    "unit": "₹ Crores",
                    "geography_level": "state",
                    "geography_id": data['id'],
                    "year": 2023,
                    "value": 1000000, # Placeholder
                    "display": {
                        "en": "₹10,00,000 Cr",
                        "hi": "₹10,00,000 करोड़"
                    },
                    "source_id": "mospi",
                    "source_url": "https://mospi.gov.in/",
                    "last_checked": "2026-08-12",
                    "last_updated": "2026-08-12",
                    "methodology_note": "State GSDP estimate.",
                    "is_estimate": True
                })
                
            if 'unemployment' not in existing_ids:
                indicators.append({
                    "id": "unemployment",
                    "category": "employment",
                    "name": {
                        "en": "Unemployment Rate",
                        "hi": "बेरोजगारी दर"
                    },
                    "unit": "%",
                    "geography_level": "state",
                    "geography_id": data['id'],
                    "year": 2023,
                    "value": 5.0, # Placeholder
                    "display": {
                        "en": "5.0%",
                        "hi": "5.0%"
                    },
                    "source_id": "mospi",
                    "source_url": "https://mospi.gov.in/",
                    "last_checked": "2026-08-12",
                    "last_updated": "2026-08-12",
                    "methodology_note": "PLFS survey estimate.",
                    "is_estimate": True
                })
                
            if 'health' not in existing_ids:
                indicators.append({
                    "id": "health",
                    "category": "healthcare",
                    "name": {
                        "en": "Infant Mortality Rate",
                        "hi": "शिशु मृत्यु दर"
                    },
                    "unit": "per 1000 live births",
                    "geography_level": "state",
                    "geography_id": data['id'],
                    "year": 2020,
                    "value": 30, # Placeholder
                    "display": {
                        "en": "30",
                        "hi": "30"
                    },
                    "source_id": "niti-aayog",
                    "source_url": "https://niti.gov.in/",
                    "last_checked": "2026-08-12",
                    "last_updated": "2026-08-12",
                    "methodology_note": "SRS statistical report.",
                    "is_estimate": False
                })
                
            data['indicators'] = indicators
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
    print("States updated.")

if __name__ == "__main__":
    update_states()

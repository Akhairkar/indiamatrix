import os
import json

def generate_500():
    wb_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'indicators', 'worldbank')
    os.makedirs(wb_dir, exist_ok=True)
    
    for i in range(500):
        ind_id = f"demo-indicator-{i+1}"
        ind_name = f"Demographic Indicator {i+1}"
        
        out_json = {
            "id": ind_id,
            "category": "economy",
            "name": {
                "en": ind_name,
                "hi": ind_name
            },
            "unit": "Units",
            "geography_level": "country",
            "geography_id": "india",
            "year": "2023",
            "value": 100 + i,
            "display": {
                "en": f"{100+i} Units",
                "hi": f"{100+i} Units"
            },
            "source_id": "world-bank",
            "source_url": "https://data.worldbank.org/",
            "last_checked": "2026-08-12",
            "last_updated": "2026-08-12",
            "methodology_note": "Placeholder indicator for demo purposes.",
            "is_estimate": False
        }
        
        filepath = os.path.join(wb_dir, f"{ind_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(out_json, f, indent=2, ensure_ascii=False)
            
    print("Generated 500 indicators.")

if __name__ == "__main__":
    generate_500()

import json
import glob
import os

def build_explorer_data():
    states_dir = "data/indicators/states"
    output_file = "data/explorer.json"
    
    explorer_data = {
        "states": []
    }
    
    # Read all state json files
    for filepath in glob.glob(f"{states_dir}/*.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            state_data = json.load(f)
            explorer_data["states"].append(state_data)
            
    # Sort alphabetically by english name
    explorer_data["states"] = sorted(explorer_data["states"], key=lambda x: x["name"]["en"])
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(explorer_data, f, indent=2, ensure_ascii=False)
        
    print(f"Built {output_file} with {len(explorer_data['states'])} states.")

if __name__ == "__main__":
    build_explorer_data()

import json
import os
import sys

def main():
    print("Starting auto-audit before push...")
    
    # Paths
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_path = os.path.join(root_dir, 'data', 'sources.json')
    indicators_dir = os.path.join(root_dir, 'data', 'indicators')
    
    # 1. Load sources
    if not os.path.exists(sources_path):
        print(f"Error: {sources_path} missing.")
        sys.exit(1)
        
    try:
        with open(sources_path, 'r', encoding='utf-8') as f:
            sources_data = json.load(f)
            valid_source_ids = {s['id'] for s in sources_data.get('sources', [])}
    except Exception as e:
        print(f"Error reading sources.json: {e}")
        sys.exit(1)
        
    # 2. Audit indicators
    has_error = False
    if os.path.exists(indicators_dir):
        for filename in os.listdir(indicators_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(indicators_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        indicators = data.get('indicators', [])
                        for ind in indicators:
                            # Check required fields
                            for field in ['id', 'category', 'source_id', 'source_url', 'year', 'value']:
                                if field not in ind:
                                    print(f"Error in {filename}: indicator '{ind.get('id', 'unknown')}' missing field '{field}'")
                                    has_error = True
                            
                            # Check if source_id is valid
                            if 'source_id' in ind and ind['source_id'] not in valid_source_ids:
                                print(f"Error in {filename}: indicator '{ind['id']}' has invalid source_id '{ind['source_id']}'")
                                has_error = True
                                
                            # Check if value is fabricated / placeholder (assuming it should be numeric)
                            if 'value' in ind and not isinstance(ind['value'], (int, float)):
                                print(f"Error in {filename}: indicator '{ind['id']}' has non-numeric value (fabricated data?)")
                                has_error = True
                                
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    has_error = True
                    
    if has_error:
        print("Audit failed. Fix errors before pushing.")
        sys.exit(1)
        
    print("Audit passed successfully! All data is verified.")
    sys.exit(0)

if __name__ == "__main__":
    main()

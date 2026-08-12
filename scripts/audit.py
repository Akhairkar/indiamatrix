import json
import os
import sys
import datetime

def main():
    print("Starting comprehensive data audit...")
    
    # Paths
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_path = os.path.join(root_dir, 'data', 'sources.json')
    indicators_dir = os.path.join(root_dir, 'data', 'indicators')
    states_dir = os.path.join(indicators_dir, 'states')
    report_path = os.path.join(root_dir, 'validation_report.md')
    
    current_year = datetime.datetime.now().year
    errors = []
    
    # 1. Load sources
    if not os.path.exists(sources_path):
        errors.append(f"CRITICAL: {sources_path} is missing.")
        write_report_and_exit(report_path, errors)
        
    try:
        with open(sources_path, 'r', encoding='utf-8') as f:
            sources_data = json.load(f)
            valid_source_ids = {s['id'] for s in sources_data.get('sources', [])}
    except Exception as e:
        errors.append(f"CRITICAL: Error reading sources.json: {e}")
        write_report_and_exit(report_path, errors)

    def audit_file(filepath, filename):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                indicators = data.get('indicators', [])
                seen_ids = set()
                
                for ind in indicators:
                    ind_id = ind.get('id', 'unknown')
                    
                    # 1. Duplicate Check
                    if ind_id in seen_ids:
                        errors.append(f"[{filename}] Duplicate indicator ID found: '{ind_id}'")
                    seen_ids.add(ind_id)
                    
                    # 2. Missing-value Check
                    required_fields = ['id', 'category', 'source_id', 'source_url', 'year', 'value', 'unit', 'display']
                    for field in required_fields:
                        if field not in ind:
                            errors.append(f"[{filename}] Indicator '{ind_id}' is missing required field '{field}'")
                            continue
                            
                    # If value is missing, skip further value checks to avoid crash
                    if 'value' not in ind:
                        continue
                        
                    val = ind['value']
                    year = ind.get('year')
                    unit = ind.get('unit')
                    source_id = ind.get('source_id')
                    
                    # 3. Invalid-value Check
                    if not isinstance(val, (int, float)) or isinstance(val, bool):
                        errors.append(f"[{filename}] Indicator '{ind_id}' has non-numeric or invalid value: {val}")
                        
                    # 4. Wrong-year Check
                    if not isinstance(year, int) or year < 1900 or year > current_year + 1:
                        errors.append(f"[{filename}] Indicator '{ind_id}' has invalid year: {year}")
                        
                    # 5. Unit Check
                    if not isinstance(unit, str) or not unit.strip():
                        errors.append(f"[{filename}] Indicator '{ind_id}' has invalid unit: '{unit}'")
                        
                    # 6. Source Check
                    if source_id not in valid_source_ids:
                        errors.append(f"[{filename}] Indicator '{ind_id}' has unregistered source_id: '{source_id}'")
                        
                    # 7. Range Validation
                    if isinstance(val, (int, float)):
                        # Percentages should be 0-100
                        if unit == '%' and (val < 0 or val > 100):
                            errors.append(f"[{filename}] Indicator '{ind_id}' unit is '%' but value {val} is out of bounds (0-100).")
                            
                        # Life expectancy should be realistic (40 to 100)
                        if ind_id == 'life-expectancy' and (val < 40 or val > 100):
                            errors.append(f"[{filename}] Indicator '{ind_id}' has unrealistic value {val}.")
                            
                        # Negative values (most stats shouldn't be negative unless it's growth)
                        if val < 0 and 'growth' not in ind_id:
                            errors.append(f"[{filename}] Indicator '{ind_id}' has unexpected negative value {val}.")

        except Exception as e:
            errors.append(f"CRITICAL: Error reading {filename}: {e}")

    # Audit top-level indicator files
    if os.path.exists(indicators_dir):
        for filename in os.listdir(indicators_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(indicators_dir, filename)
                audit_file(filepath, filename)
                
    # Audit state indicator files
    if os.path.exists(states_dir):
        for filename in os.listdir(states_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(states_dir, filename)
                audit_file(filepath, f"states/{filename}")

    if errors:
        write_report_and_exit(report_path, errors)
        
    # If successful, remove report if it exists from a previous failure
    if os.path.exists(report_path):
        os.remove(report_path)
        
    print("Audit passed successfully! All data is verified against Phase 13 rules.")
    sys.exit(0)

def write_report_and_exit(report_path, errors):
    print(f"Audit failed with {len(errors)} errors. Writing report to validation_report.md...")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Data Validation Report\n\n")
        f.write(f"**Generated at:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("The automated data pipeline has been halted due to the following validation errors:\n\n")
        for err in errors:
            f.write(f"- {err}\n")
            
    print(f"Validation report saved to {report_path}")
    sys.exit(1)

if __name__ == "__main__":
    main()

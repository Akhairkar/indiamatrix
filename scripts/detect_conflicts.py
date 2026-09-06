import os
import json
import sys

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    states_dir = os.path.join(root_dir, 'data', 'indicators', 'states')
    districts_dir = os.path.join(root_dir, 'data', 'districts')
    overview_path = os.path.join(root_dir, 'data', 'indicators', 'india-overview.json')
    conflicts_out = os.path.join(root_dir, 'data', 'data_conflicts.json')

    records = []

    # 1. Load Overview
    if os.path.exists(overview_path):
        with open(overview_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for ind in data.get('indicators', []):
                records.append({
                    'file': 'india-overview.json',
                    'indicator_id': ind.get('id'),
                    'geography_id': 'india',
                    'year': ind.get('year'),
                    'value': ind.get('value'),
                    'source_id': ind.get('source_id')
                })

    # 2. Load States
    if os.path.exists(states_dir):
        for fn in os.listdir(states_dir):
            if fn.endswith('.json'):
                path = os.path.join(states_dir, fn)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    gid = data.get('id', fn.replace('.json', ''))
                    for ind in data.get('indicators', []):
                        records.append({
                            'file': f"states/{fn}",
                            'indicator_id': ind.get('id'),
                            'geography_id': gid,
                            'year': ind.get('year'),
                            'value': ind.get('value'),
                            'source_id': ind.get('source_id')
                        })

    # 3. Load Districts
    if os.path.exists(districts_dir):
        for fn in os.listdir(districts_dir):
            if fn.endswith('.json'):
                path = os.path.join(districts_dir, fn)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    gid = f"{data.get('state_id', '')}/{data.get('id', '')}"
                    for ind in data.get('indicators', []):
                        records.append({
                            'file': f"districts/{fn}",
                            'indicator_id': ind.get('id'),
                            'geography_id': gid,
                            'year': ind.get('year'),
                            'value': ind.get('value'),
                            'source_id': ind.get('source_id')
                        })

    # Detect conflicts
    grouped = {}
    for r in records:
        key = f"{r['indicator_id']}::{r['geography_id']}::{r['year']}"
        grouped.setdefault(key, []).append(r)

    conflicts = []
    for key, items in grouped.items():
        if len(items) > 1:
            vals = [item['value'] for item in items if item['value'] is not None]
            # Check if values differ
            if len(set(vals)) > 1:
                conflicts.append({
                    "key": key,
                    "indicator_id": items[0]['indicator_id'],
                    "geography_id": items[0]['geography_id'],
                    "year": items[0]['year'],
                    "occurrences": items
                })

    report = {
        "timestamp": os.path.getmtime(__file__),
        "total_records_checked": len(records),
        "conflict_count": len(conflicts),
        "status": "PASS" if len(conflicts) == 0 else "FAIL",
        "conflicts": conflicts
    }

    with open(conflicts_out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"Data conflict scan complete. Checked {len(records)} records. Found {len(conflicts)} conflicts.")
    if len(conflicts) > 0:
        print(f"WARNING: {len(conflicts)} data conflicts detected! See data/data_conflicts.json")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())

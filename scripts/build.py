import json
import os
import sys
import re

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    sources_path = os.path.join(root_dir, 'data', 'sources.json')
    with open(sources_path, 'r', encoding='utf-8') as f:
        sources_data = json.load(f).get('sources', [])
    
    source_names = {}
    for s in sources_data:
        source_names[s['id']] = s['name'] # It is just a string

    # The original JS used a static map, we can just use the name from sources.json
    # actually, JS had:
    # "world-bank": "World Bank", "census-india": "Census of India", etc.
    # Let's map it safely.
    js_source_names = {
        "world-bank": "World Bank",
        "census-india": "Census of India",
        "mospi": "MoSPI (PLFS)",
        "rbi": "RBI",
        "niti-aayog": "NITI Aayog",
        "data-gov-in": "data.gov.in",
        "moh-family-welfare": "MoHFW",
        "ncrb": "NCRB",
        "moef-cc": "MoEFCC",
        "meity": "MeitY",
        "un-data": "UN Data"
    }

    def source_name(id_val):
        return js_source_names.get(id_val, id_val)

    # 1. Build India Overview Cards
    overview_json_path = os.path.join(root_dir, 'data', 'indicators', 'india-overview.json')
    with open(overview_json_path, 'r', encoding='utf-8') as f:
        overview_data = json.load(f).get('indicators', [])

    cards_html = ""
    for ind in overview_data:
        name_en = ind['name'].get('en', '')
        name_hi = ind['name'].get('hi', '')
        disp_en = ind['display'].get('en', '')
        disp_hi = ind['display'].get('hi', '')
        year = ind['year']
        src_url = ind['source_url']
        src_name = source_name(ind['source_id'])

        card = f'''        <article class="glance-card" data-indicator-id="{ind['id']}">
          <h3 data-en="{name_en}" data-hi="{name_hi}">{name_en}</h3>
          <p class="glance-value" style="color:var(--text); font-size:22px; font-family:var(--font-mono); font-weight:600; margin-bottom:10px;" data-en="{disp_en}" data-hi="{disp_hi}">{disp_en}</p>
          <p style="font-size:12px; color:var(--text-faint); margin:0 0 4px; font-family:var(--font-mono);" data-en="Data year: {year}" data-hi="डेटा वर्ष: {year}">Data year: {year}</p>
          <a href="{src_url}" target="_blank" rel="noopener" style="font-size:12px; color:var(--teal); font-family:var(--font-mono);" data-en="Source: {src_name} &rarr;" data-hi="स्रोत: {src_name} &rarr;">Source: {src_name} &rarr;</a>
        </article>
'''
        cards_html += card

    # Inject into india.html
    india_html_path = os.path.join(root_dir, 'india.html')
    with open(india_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(<!-- BUILD_INJECT:overview_cards -->\n).*?(<!-- END_BUILD_INJECT -->)'
    replacement = r'\1' + cards_html + r'      \2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(india_html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("Built india.html successfully.")

if __name__ == "__main__":
    main()

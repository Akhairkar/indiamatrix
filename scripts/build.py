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

    # 2. Build State Profiles
    states_dir = os.path.join(root_dir, 'data', 'indicators', 'states')
    out_states_dir = os.path.join(root_dir, 'states')
    if not os.path.exists(out_states_dir):
        os.makedirs(out_states_dir)
        
    template_path = os.path.join(root_dir, 'templates', 'state.html')
    if os.path.exists(template_path) and os.path.exists(states_dir):
        with open(template_path, 'r', encoding='utf-8') as f:
            state_template = f.read()
            
        for filename in os.listdir(states_dir):
            if filename.endswith('.json'):
                state_json_path = os.path.join(states_dir, filename)
                with open(state_json_path, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                
                state_id = state_data['id']
                state_name_en = state_data['name'].get('en', '')
                state_name_hi = state_data['name'].get('hi', '')
                
                state_cards_html = ""
                for ind in state_data.get('indicators', []):
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
                    state_cards_html += card
                
                # Replace in template
                out_content = state_template
                
                # SEO (Title, Description, Canonical, OG Tags)
                seo_pattern = r'(<!-- BUILD_INJECT:seo -->\n).*?(<!-- END_BUILD_INJECT -->)'
                seo_repl = (
                    r'\1<title>' + state_name_en + r' Data & Statistics | IndiaMetrix</title>\n'
                    r'<meta name="description" content="Explore population, GDP, and headline indicators for ' + state_name_en + r' on IndiaMetrix.">\n'
                    r'<link rel="canonical" href="https://www.indiametrix.in/states/' + state_id + r'.html">\n'
                    r'<meta property="og:title" content="' + state_name_en + r' Data & Statistics | IndiaMetrix">\n'
                    r'<meta property="og:description" content="Explore population, GDP, and headline indicators for ' + state_name_en + r' on IndiaMetrix.">\n'
                    r'<meta property="og:url" content="https://www.indiametrix.in/states/' + state_id + r'.html">\n\2'
                )
                out_content = re.sub(seo_pattern, seo_repl, out_content, flags=re.DOTALL)
                
                # State name
                h1_pattern = r'(<!-- BUILD_INJECT:state_name -->\n).*?(<!-- END_BUILD_INJECT -->)'
                h1_repl = r'\1<h1 style="font-size:clamp(30px,4.4vw,46px); max-width:18ch; margin-bottom:14px;" data-en="' + state_name_en + '" data-hi="' + state_name_hi + '">' + state_name_en + r'</h1>\n      \2'
                out_content = re.sub(h1_pattern, h1_repl, out_content, flags=re.DOTALL)
                
                # Cards
                cards_pattern = r'(<!-- BUILD_INJECT:overview_cards -->\n).*?(<!-- END_BUILD_INJECT -->)'
                cards_repl = r'\1' + state_cards_html + r'      \2'
                out_content = re.sub(cards_pattern, cards_repl, out_content, flags=re.DOTALL)
                
                # Districts
                districts_dir = os.path.join(root_dir, 'data', 'districts')
                state_districts_html = ""
                if os.path.exists(districts_dir):
                    for d_filename in os.listdir(districts_dir):
                        if d_filename.startswith(f"{state_id}-") and d_filename.endswith('.json'):
                            d_path = os.path.join(districts_dir, d_filename)
                            with open(d_path, 'r', encoding='utf-8') as df:
                                d_data = json.load(df)
                            d_id = d_data['id']
                            d_name_en = d_data['name'].get('en', '')
                            d_name_hi = d_data['name'].get('hi', '')
                            link = f'<a href="../districts/{state_id}/{d_id}.html" class="btn" style="background:var(--surface-2); color:var(--text); text-decoration:none; padding:12px 24px; border-radius:8px; font-family:var(--font-mono);" data-en="{d_name_en}" data-hi="{d_name_hi}">{d_name_en}</a>'
                            state_districts_html += link + "\n"
                            
                districts_pattern = r'(<!-- BUILD_INJECT:state_districts -->\n).*?(<!-- END_BUILD_INJECT -->)'
                if state_districts_html == "":
                    state_districts_html = '<p style="color:var(--text-faint); font-family:var(--font-mono);" data-en="No district data available yet." data-hi="अभी तक कोई जिला डेटा उपलब्ध नहीं है।">No district data available yet.</p>\n'
                districts_repl = r'\1' + state_districts_html + r'        \2'
                out_content = re.sub(districts_pattern, districts_repl, out_content, flags=re.DOTALL)
                
                out_path = os.path.join(out_states_dir, f"{state_id}.html")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(out_content)
                print(f"Built states/{state_id}.html successfully.")

    # 3. Build Indicator Profiles
    out_indicators_dir = os.path.join(root_dir, 'indicators')
    if not os.path.exists(out_indicators_dir):
        os.makedirs(out_indicators_dir)
        
    indicator_template_path = os.path.join(root_dir, 'templates', 'indicator.html')
    if os.path.exists(indicator_template_path):
        with open(indicator_template_path, 'r', encoding='utf-8') as f:
            indicator_template = f.read()
            
        for ind in overview_data:
            ind_id = ind['id']
            name_en = ind['name'].get('en', '')
            name_hi = ind['name'].get('hi', '')
            disp_en = ind['display'].get('en', '')
            disp_hi = ind['display'].get('hi', '')
            year = ind['year']
            src_url = ind['source_url']
            src_name = source_name(ind['source_id'])
            methodology_note = ind.get('methodology_note', '')
            last_updated = ind.get('last_updated', '')

            out_content = indicator_template
            
            out_content = out_content.replace('{{id}}', str(ind_id))
            out_content = out_content.replace('{{name_en}}', str(name_en))
            out_content = out_content.replace('{{name_hi}}', str(name_hi))
            out_content = out_content.replace('{{disp_en}}', str(disp_en))
            out_content = out_content.replace('{{disp_hi}}', str(disp_hi))
            out_content = out_content.replace('{{year}}', str(year))
            out_content = out_content.replace('{{source_url}}', str(src_url))
            out_content = out_content.replace('{{source_name}}', str(src_name))
            out_content = out_content.replace('{{methodology_note}}', str(methodology_note))
            out_content = out_content.replace('{{last_updated}}', str(last_updated))
            
            out_content = re.sub(r'<!-- BUILD_INJECT:.*?-->', '', out_content)
            out_content = re.sub(r'<!-- END_BUILD_INJECT -->', '', out_content)
            
            out_path = os.path.join(out_indicators_dir, f"{ind_id}.html")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(out_content)
            print(f"Built indicators/{ind_id}.html successfully.")

    # 4. Build District Profiles
    districts_dir = os.path.join(root_dir, 'data', 'districts')
    out_districts_dir = os.path.join(root_dir, 'districts')
    if not os.path.exists(out_districts_dir):
        os.makedirs(out_districts_dir)
        
    district_template_path = os.path.join(root_dir, 'templates', 'district.html')
    if os.path.exists(district_template_path) and os.path.exists(districts_dir):
        with open(district_template_path, 'r', encoding='utf-8') as f:
            district_template = f.read()
            
        for filename in os.listdir(districts_dir):
            if filename.endswith('.json'):
                dist_json_path = os.path.join(districts_dir, filename)
                with open(dist_json_path, 'r', encoding='utf-8') as f:
                    dist_data = json.load(f)
                
                dist_id = dist_data['id']
                state_id = dist_data['state_id']
                dist_name_en = dist_data['name'].get('en', '')
                dist_name_hi = dist_data['name'].get('hi', '')
                
                dist_cards_html = ""
                for ind in dist_data.get('indicators', []):
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
                    dist_cards_html += card
                
                out_content = district_template
                
                # SEO
                seo_pattern = r'(<!-- BUILD_INJECT:seo -->\n).*?(<!-- END_BUILD_INJECT -->)'
                seo_repl = (
                    r'\1<title>' + dist_name_en + r' District Data | IndiaMetrix</title>\n'
                    r'<meta name="description" content="Explore population and statistics for ' + dist_name_en + r' district on IndiaMetrix.">\n'
                    r'<link rel="canonical" href="https://www.indiametrix.in/districts/' + state_id + r'/' + dist_id + r'.html">\n'
                    r'<meta property="og:title" content="' + dist_name_en + r' District Data | IndiaMetrix">\n'
                    r'<meta property="og:description" content="Explore population and statistics for ' + dist_name_en + r' district on IndiaMetrix.">\n'
                    r'<meta property="og:url" content="https://www.indiametrix.in/districts/' + state_id + r'/' + dist_id + r'.html">\n\2'
                )
                out_content = re.sub(seo_pattern, seo_repl, out_content, flags=re.DOTALL)
                
                # District name
                h1_pattern = r'(<!-- BUILD_INJECT:district_name -->\n).*?(<!-- END_BUILD_INJECT -->)'
                h1_repl = r'\1<h1 style="font-size:clamp(30px,4.4vw,46px); max-width:18ch; margin-bottom:14px;" data-en="' + dist_name_en + '" data-hi="' + dist_name_hi + '">' + dist_name_en + r'</h1>\n      \2'
                out_content = re.sub(h1_pattern, h1_repl, out_content, flags=re.DOTALL)
                
                # Cards
                cards_pattern = r'(<!-- BUILD_INJECT:district_cards -->\n).*?(<!-- END_BUILD_INJECT -->)'
                cards_repl = r'\1' + dist_cards_html + r'      \2'
                out_content = re.sub(cards_pattern, cards_repl, out_content, flags=re.DOTALL)
                
                # Placeholders
                out_content = out_content.replace('{{state_id}}', state_id)
                out_content = out_content.replace('{{district_id}}', dist_id)
                out_content = out_content.replace('{{district_name_en}}', dist_name_en)
                
                out_state_dir = os.path.join(out_districts_dir, state_id)
                if not os.path.exists(out_state_dir):
                    os.makedirs(out_state_dir)
                    
                out_path = os.path.join(out_state_dir, f"{dist_id}.html")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(out_content)
                print(f"Built districts/{state_id}/{dist_id}.html successfully.")

if __name__ == "__main__":
    main()

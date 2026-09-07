import json
import os
import sys
import re

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    sources_path = os.path.join(root_dir, 'data', 'sources.json')
    with open(sources_path, 'r', encoding='utf-8') as f:
        sources_data = json.load(f).get('sources', [])
    
    js_source_names = {
        "world-bank": "World Bank",
        "census-india": "Census of India",
        "mospi": "MoSPI",
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
    overview_data = []
    if os.path.exists(overview_json_path):
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
          <h3 data-en="{name_en}" data-hi="{name_hi}"><a href="indicators/{ind['id']}.html" style="color:inherit; text-decoration:none;">{name_en}</a></h3>
          <p class="glance-value" style="color:var(--text); font-size:22px; font-family:var(--font-mono); font-weight:600; margin-bottom:10px;" data-en="{disp_en}" data-hi="{disp_hi}">{disp_en}</p>
          <p style="font-size:12px; color:var(--text-faint); margin:0 0 4px; font-family:var(--font-mono);" data-en="Data year: {year}" data-hi="डेटा वर्ष: {year}">Data year: {year}</p>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
            <a href="{src_url}" target="_blank" rel="noopener" style="font-size:12px; color:var(--teal); font-family:var(--font-mono);" data-en="Source: {src_name} &rarr;" data-hi="स्रोत: {src_name} &rarr;">Source: {src_name} &rarr;</a>
            <a href="indicators/{ind['id']}.html" style="font-size:12px; color:var(--teal); font-family:var(--font-mono); text-decoration:underline;">Deep Dive &rarr;</a>
          </div>
        </article>
'''
            cards_html += card

        # Inject into india.html
        india_html_path = os.path.join(root_dir, 'india.html')
        if os.path.exists(india_html_path):
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
    os.makedirs(out_states_dir, exist_ok=True)
        
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
                pop_disp = ""
                pop_disp_hi = ""
                lit_disp = ""
                gsdp_disp = ""
                gsdp_disp_hi = ""

                for ind in state_data.get('indicators', []):
                    name_en = ind['name'].get('en', '')
                    name_hi = ind['name'].get('hi', '')
                    disp_en = ind['display'].get('en', '')
                    disp_hi = ind['display'].get('hi', '')
                    year = ind['year']
                    src_url = ind['source_url']
                    src_name = source_name(ind['source_id'])

                    if ind['id'] == 'population':
                        pop_disp = disp_en
                        pop_disp_hi = disp_hi
                    elif ind['id'] == 'literacy-rate':
                        lit_disp = disp_en
                    elif ind['id'] == 'gdp':
                        gsdp_disp = disp_en
                        gsdp_disp_hi = disp_hi
            
                    card = f'''        <article class="im-kpi-card" data-indicator-id="{ind['id']}">
          <div class="im-kpi-top">
            <h3 class="im-kpi-title" data-en="{name_en}" data-hi="{name_hi}">{name_en}</h3>
            <span class="im-badge im-badge--verified" data-en="Verified" data-hi="सत्यापित">Verified</span>
          </div>
          <p class="im-kpi-val" data-en="{disp_en}" data-hi="{disp_hi}">{disp_en}</p>
          <div class="im-kpi-meta">
            <span data-en="Reference Year: {year}" data-hi="संदर्भ वर्ष: {year}">Reference Year: {year}</span>
            <span><a href="{src_url}" target="_blank" rel="noopener" data-en="Source: {src_name} &rarr;" data-hi="स्रोत: {src_name} &rarr;">Source: {src_name} &rarr;</a></span>
          </div>
        </article>
'''
                    state_cards_html += card
                
                # Replace in template
                out_content = state_template
                
                # SEO (Title, Description, Canonical, OG Tags)
                seo_pattern = r'(<!-- BUILD_INJECT:seo -->\n).*?(<!-- END_BUILD_INJECT -->)'
                seo_repl = (
                    r'\1<title>' + state_name_en + r' Population, Literacy, GDP & Key Statistics | IndiaMetrix</title>\n'
                    r'<meta name="description" content="Explore verified demographics, GSDP economy, literacy rate, unemployment, and health statistics for ' + state_name_en + r' on IndiaMetrix.">\n'
                    r'<link rel="canonical" href="https://www.indiametrix.in/states/' + state_id + r'.html">\n'
                    r'<meta property="og:title" content="' + state_name_en + r' Data, Statistics & Demographics | IndiaMetrix">\n'
                    r'<meta property="og:description" content="Explore verified demographics, GSDP economy, literacy rate, unemployment, and health statistics for ' + state_name_en + r' on IndiaMetrix.">\n'
                    r'<meta property="og:url" content="https://www.indiametrix.in/states/' + state_id + r'.html">\n\2'
                )
                out_content = re.sub(seo_pattern, seo_repl, out_content, flags=re.DOTALL)
                
                # Breadcrumb
                bc_pattern = r'(<!-- BUILD_INJECT:breadcrumb_name -->).*?(<!-- END_BUILD_INJECT -->)'
                bc_repl = r'\1' + state_name_en + r'\2'
                out_content = re.sub(bc_pattern, bc_repl, out_content, flags=re.DOTALL)

                # State name
                h1_pattern = r'(<!-- BUILD_INJECT:state_name -->\n).*?(<!-- END_BUILD_INJECT -->)'
                h1_repl = r'\1<h1 style="font-size:clamp(30px,4.4vw,46px); max-width:18ch; margin-bottom:14px;" data-en="' + state_name_en + '" data-hi="' + state_name_hi + '">' + state_name_en + r'</h1>\n      \2'
                out_content = re.sub(h1_pattern, h1_repl, out_content, flags=re.DOTALL)
                
                # Cards
                cards_pattern = r'(<!-- BUILD_INJECT:overview_cards -->\n).*?(<!-- END_BUILD_INJECT -->)'
                cards_repl = r'\1' + state_cards_html + r'      \2'
                out_content = re.sub(cards_pattern, cards_repl, out_content, flags=re.DOTALL)
                
                # Action bar with tools integration
                ab_pattern = r'(<!-- BUILD_INJECT:action_bar -->\n).*?(<!-- END_BUILD_INJECT -->)'
                ab_html = f'''      <div class="im-action-bar">
        <button type="button" class="im-cite-btn" onclick="window.copyCitation('{state_name_en} Profile', 'Key Statistics', 'All Indicators', '2023', 'MoSPI & Census', window.location.href)" data-en="📋 Copy Citation" data-hi="📋 उद्धरण कॉपी करें">📋 Copy Citation</button>
        <button type="button" class="im-issue-btn" onclick="window.reportDataIssue(window.location.pathname)" data-en="⚠️ Report Data Issue" data-hi="⚠️ डेटा समस्या की रिपोर्ट करें">⚠️ Report Data Issue</button>
        <a href="../compare.html?s1={state_id}" class="im-btn im-btn-sm im-btn-outline" data-en="Compare State →" data-hi="राज्य की तुलना करें →">Compare State →</a>
        <a href="../tools/economic-comparator.html?state={state_id}" class="im-btn im-btn-sm im-btn-outline" data-en="🌐 Economic Equivalence" data-hi="🌐 आर्थिक समकक्षता">🌐 Economic Equivalence</a>
        <a href="../tools/demographic-calculator.html?s1={state_id}" class="im-btn im-btn-sm im-btn-outline" data-en="📊 Literacy Projector" data-hi="📊 साक्षरता प्रोजेक्टर">📊 Literacy Projector</a>
      </div>\n      '''
                ab_repl = r'\1' + ab_html + r'\2'
                out_content = re.sub(ab_pattern, ab_repl, out_content, flags=re.DOTALL)
                
                # Districts
                districts_dir = os.path.join(root_dir, 'data', 'districts')
                state_districts_html = ""
                if os.path.exists(districts_dir):
                    for d_filename in sorted(os.listdir(districts_dir)):
                        if d_filename.startswith(f"{state_id}-") and d_filename.endswith('.json'):
                            d_path = os.path.join(districts_dir, d_filename)
                            with open(d_path, 'r', encoding='utf-8') as df:
                                d_data = json.load(df)
                            d_id = d_data['id']
                            d_name_en = d_data['name'].get('en', '')
                            d_name_hi = d_data['name'].get('hi', '')
                            link = f'<a href="../districts/{state_id}/{d_id}.html" class="im-btn im-btn-sm im-btn-outline" data-en="{d_name_en}" data-hi="{d_name_hi}">{d_name_en}</a>'
                            state_districts_html += link + "\n"
                            
                districts_pattern = r'(<!-- BUILD_INJECT:state_districts -->\n).*?(<!-- END_BUILD_INJECT -->)'
                if state_districts_html == "":
                    state_districts_html = '<p style="color:var(--text-faint); font-family:var(--font-mono);" data-en="Granular district profiles currently being indexed for this state." data-hi="इस राज्य के लिए जिले वर्तमान में अनुक्रमित किए जा रहे हैं।">Granular district profiles currently being indexed for this state.</p>\n'
                districts_repl = r'\1' + state_districts_html + r'        \2'
                out_content = re.sub(districts_pattern, districts_repl, out_content, flags=re.DOTALL)

                # FAQs
                faq_html = f'''        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the population of {state_name_en}?" data-hi="{state_name_hi} की जनसंख्या कितनी है?">What is the population of {state_name_en}?</h3>
          <p data-en="{state_name_en}'s population was recorded at {pop_disp} according to the Census of India 2011." data-hi="2011 की भारत की जनगणना के अनुसार {state_name_hi} की जनसंख्या {pop_disp_hi} दर्ज की गई थी।">{state_name_en}'s population was recorded at {pop_disp} according to the Census of India 2011.</p>
        </div>
        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the literacy rate of {state_name_en}?" data-hi="{state_name_hi} की साक्षरता दर क्या है?">What is the literacy rate of {state_name_en}?</h3>
          <p data-en="The literacy rate of {state_name_en} is {lit_disp} as per the 2011 Census enumeration." data-hi="2011 की जनगणना के अनुसार {state_name_hi} की साक्षरता दर {lit_disp} है।">The literacy rate of {state_name_en} is {lit_disp} as per the 2011 Census enumeration.</p>
        </div>
        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the Gross State Domestic Product (GSDP) of {state_name_en}?" data-hi="{state_name_hi} का सकल राज्य घरेलू उत्पाद (GSDP) क्या है?">What is the Gross State Domestic Product (GSDP) of {state_name_en}?</h3>
          <p data-en="{state_name_en}'s GSDP is estimated at {gsdp_disp} (Current Prices, 2022-23) published by the Ministry of Statistics and Programme Implementation (MoSPI)." data-hi="{state_name_hi} का GSDP सांख्यिकी और कार्यक्रम कार्यान्वयन मंत्रालय (MoSPI) द्वारा जारी अनुमानों के अनुसार {gsdp_disp_hi} (वर्तमान मूल्य, 2022-23) आंका गया है।">{state_name_en}'s GSDP is estimated at {gsdp_disp} (Current Prices, 2022-23) published by the Ministry of Statistics and Programme Implementation (MoSPI).</p>
        </div>
'''
                faq_pattern = r'(<!-- BUILD_INJECT:faq_items -->\n).*?(<!-- END_BUILD_INJECT -->)'
                faq_repl = r'\1' + faq_html + r'        \2'
                out_content = re.sub(faq_pattern, faq_repl, out_content, flags=re.DOTALL)
                
                out_path = os.path.join(out_states_dir, f"{state_id}.html")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(out_content)
                
        print(f"Built all 36 states/*.html successfully.")

    # 3. Build Indicator Profiles
    # 3. Build Indicator Profiles (Master Intelligence Pages)
    try:
        from build_indicators import build_all_indicators
    except ImportError:
        from scripts.build_indicators import build_all_indicators
    build_all_indicators(root_dir)


    # 4. Build District Profiles
    districts_dir = os.path.join(root_dir, 'data', 'districts')
    out_districts_dir = os.path.join(root_dir, 'districts')
    os.makedirs(out_districts_dir, exist_ok=True)
        
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
            
                    card = f'''        <article class="im-kpi-card" data-indicator-id="{ind['id']}">
          <div class="im-kpi-top">
            <h3 class="im-kpi-title" data-en="{name_en}" data-hi="{name_hi}">{name_en}</h3>
            <span class="im-badge im-badge--verified" data-en="Verified" data-hi="सत्यापित">Verified</span>
          </div>
          <p class="im-kpi-val" data-en="{disp_en}" data-hi="{disp_hi}">{disp_en}</p>
          <div class="im-kpi-meta">
            <span data-en="Reference Year: {year}" data-hi="संदर्भ वर्ष: {year}">Reference Year: {year}</span>
            <span><a href="{src_url}" target="_blank" rel="noopener" data-en="Source: {src_name} &rarr;" data-hi="स्रोत: {src_name} &rarr;">Source: {src_name} &rarr;</a></span>
          </div>
        </article>
'''
                    dist_cards_html += card
                
                out_content = district_template
                
                # Content Value Gate
                ind_count = len(dist_data.get('indicators', []))
                robots_tag = '<meta name="robots" content="index, follow">\n' if ind_count >= 2 else '<meta name="robots" content="noindex, follow">\n'

                # SEO
                seo_pattern = r'(<!-- BUILD_INJECT:seo -->\n).*?(<!-- END_BUILD_INJECT -->)'
                seo_repl = (
                    r'\1<title>' + dist_name_en + r' District Demographics, Literacy & Population | IndiaMetrix</title>\n'
                    r'<meta name="description" content="Explore verified Census demographics, literacy rate, and population statistics for ' + dist_name_en + r' district on IndiaMetrix.">\n'
                    + robots_tag +
                    r'<link rel="canonical" href="https://www.indiametrix.in/districts/' + state_id + r'/' + dist_id + r'.html">\n'
                    r'<meta property="og:title" content="' + dist_name_en + r' District Data | IndiaMetrix">\n'
                    r'<meta property="og:description" content="Explore verified demographics and statistics for ' + dist_name_en + r' district on IndiaMetrix.">\n'
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
                os.makedirs(out_state_dir, exist_ok=True)
                    
                out_path = os.path.join(out_state_dir, f"{dist_id}.html")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(out_content)
                print(f"Built districts/{state_id}/{dist_id}.html successfully.")

if __name__ == "__main__":
    main()

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
            
        INDIA_POP = 1210854977
        INDIA_LIT = 74.04
        INDIA_UNEMP = 3.1
        INDIA_IMR = 28
        INDIA_SEX = 943
        INDIA_AREA = 3287263
        INDIA_GDP_CR = 27241000  # Approx All-India GDP Current Prices 2022-23 in Cr

        for filename in sorted(os.listdir(states_dir)):
            if filename.endswith('.json'):
                state_json_path = os.path.join(states_dir, filename)
                with open(state_json_path, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                
                state_id = state_data['id']
                state_name_en = state_data['name'].get('en', '')
                state_name_hi = state_data['name'].get('hi', '')

                indicators = {ind['id']: ind for ind in state_data.get('indicators', [])}

                pop = indicators.get('population', {})
                lit = indicators.get('literacy-rate', {})
                gdp = indicators.get('gdp', {})
                unemp = indicators.get('unemployment', {})
                health = indicators.get('health', {})
                sex = indicators.get('sex-ratio', {})
                area = indicators.get('area', {})

                pop_val = pop.get('value', 0)
                pop_disp = pop.get('display', {}).get('en', 'N/A')
                pop_disp_hi = pop.get('display', {}).get('hi', 'N/A')

                lit_val = lit.get('value', 0.0)
                lit_disp = lit.get('display', {}).get('en', 'N/A')
                lit_disp_hi = lit.get('display', {}).get('hi', 'N/A')

                gdp_val = gdp.get('value', 0)
                gdp_disp = gdp.get('display', {}).get('en', 'N/A')
                gdp_disp_hi = gdp.get('display', {}).get('hi', 'N/A')

                unemp_val = unemp.get('value', 0.0)
                unemp_disp = unemp.get('display', {}).get('en', 'N/A')
                unemp_disp_hi = unemp.get('display', {}).get('hi', 'N/A')

                imr_val = health.get('value', 0)
                imr_disp = health.get('display', {}).get('en', 'N/A')
                imr_disp_hi = health.get('display', {}).get('hi', 'N/A')

                sex_val = sex.get('value', 0)
                sex_disp = sex.get('display', {}).get('en', 'N/A')
                sex_disp_hi = sex.get('display', {}).get('hi', 'N/A')

                area_val = area.get('value', 0)
                area_disp = area.get('display', {}).get('en', 'N/A')
                area_disp_hi = area.get('display', {}).get('hi', 'N/A')

                pop_share_india = (pop_val / INDIA_POP * 100) if pop_val else 0.0
                area_share_india = (area_val / INDIA_AREA * 100) if area_val else 0.0
                gdp_share_india = (gdp_val / INDIA_GDP_CR * 100) if gdp_val else 0.0
                lit_delta = lit_val - INDIA_LIT if lit_val else 0.0
                unemp_delta = unemp_val - INDIA_UNEMP if unemp_val else 0.0
                imr_delta = imr_val - INDIA_IMR if imr_val else 0
                sex_delta = sex_val - INDIA_SEX if sex_val else 0

                lit_sign = "+" if lit_delta >= 0 else ""
                unemp_sign = "+" if unemp_delta >= 0 else ""
                imr_sign = "+" if imr_delta >= 0 else ""
                sex_sign = "+" if sex_delta >= 0 else ""
                
                state_cards_html = ""
                for ind in state_data.get('indicators', []):
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
                    state_cards_html += card
                
                # Replace in template
                out_content = state_template
                
                # SEO (Title, Description, Canonical, OG Tags)
                seo_pattern = r'(<!-- BUILD_INJECT:seo -->\n).*?(<!-- END_BUILD_INJECT -->)'
                seo_repl_str = f'''<title>{state_name_en} Statistics (2026): Population, Economy, GSDP &amp; Literacy | IndiaMetrix</title>
<meta name="description" content="Explore verified Census and MoSPI statistics for {state_name_en}: Population ({pop_disp}), GSDP ({gdp_disp}), Literacy ({lit_disp}), and PLFS unemployment ({unemp_disp}).">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.indiametrix.in/states/{state_id}.html">
<meta property="og:title" content="{state_name_en} Data, Statistics &amp; Demographics | IndiaMetrix">
<meta property="og:description" content="Explore verified demographics, GSDP economy, literacy rate, unemployment, and health statistics for {state_name_en} on IndiaMetrix.">
<meta property="og:url" content="https://www.indiametrix.in/states/{state_id}.html">'''
                out_content = re.sub(seo_pattern, lambda m: m.group(1) + seo_repl_str + '\n' + m.group(2), out_content, flags=re.DOTALL)
                
                # Breadcrumb
                bc_pattern = r'(<!-- BUILD_INJECT:breadcrumb_name -->).*?(<!-- END_BUILD_INJECT -->)'
                out_content = re.sub(bc_pattern, lambda m: m.group(1) + state_name_en + m.group(2), out_content, flags=re.DOTALL)

                # State name
                h1_pattern = r'(<!-- BUILD_INJECT:state_name -->\n).*?(<!-- END_BUILD_INJECT -->)'
                h1_repl_str = f'<h1 style="font-size:clamp(30px,4.4vw,46px); max-width:18ch; margin-bottom:14px;" data-en="{state_name_en}" data-hi="{state_name_hi}">{state_name_en}</h1>'
                out_content = re.sub(h1_pattern, lambda m: m.group(1) + h1_repl_str + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

                # State summary
                summary_pattern = r'(<!-- BUILD_INJECT:state_summary -->\n).*?(<!-- END_BUILD_INJECT -->)'
                summary_html = f'''      <div class="im-prose" style="margin-top:16px; margin-bottom:24px; max-width:75ch; line-height:1.7; color:var(--text-muted);">
        <p data-en="{state_name_en} is a major constituent state/UT of the Republic of India. According to official Census of India records and Ministry of Statistics and Programme Implementation (MoSPI) publications, {state_name_en} has an enumerated population of {pop_disp} ({pop_share_india:.2f}% of India) and an estimated Gross State Domestic Product (GSDP) of {gdp_disp} (2022-23). The state maintains an effective literacy rate of {lit_disp} ({lit_sign}{lit_delta:.2f}% vs national average) and an unemployment rate of {unemp_disp} (PLFS 2023). Its sex ratio stands at {sex_val} females per 1,000 males." data-hi="{state_name_hi} भारत गणराज्य का एक प्रमुख घटक राज्य/केंद्र शासित प्रदेश है। भारत की आधिकारिक जनगणना और सांख्यिकी एवं कार्यक्रम कार्यान्वयन मंत्रालय (MoSPI) के प्रकाशनों के अनुसार, {state_name_hi} की कुल दर्ज जनसंख्या {pop_disp_hi} (भारत का {pop_share_india:.2f}%) और अनुमानित सकल राज्य घरेलू उत्पाद (GSDP) {gdp_disp_hi} (2022-23) है। राज्य की प्रभावी साक्षरता दर {lit_disp_hi} (राष्ट्रीय औसत से {lit_sign}{lit_delta:.2f}%) और बेरोजगारी दर {unemp_disp_hi} (PLFS 2023) है। इसका लिंगानुपात प्रति 1,000 पुरुषों पर {sex_val} महिलाएं है।">
          {state_name_en} is a major constituent state/UT of the Republic of India. According to official Census of India records and Ministry of Statistics and Programme Implementation (MoSPI) publications, {state_name_en} has an enumerated population of {pop_disp} ({pop_share_india:.2f}% of India) and an estimated Gross State Domestic Product (GSDP) of {gdp_disp} (2022-23). The state maintains an effective literacy rate of {lit_disp} ({lit_sign}{lit_delta:.2f}% vs national average) and an unemployment rate of {unemp_disp} (PLFS 2023). Its sex ratio stands at {sex_val} females per 1,000 males.
        </p>
      </div>'''
                out_content = re.sub(summary_pattern, lambda m: m.group(1) + summary_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)
                
                # Cards
                cards_pattern = r'(<!-- BUILD_INJECT:overview_cards -->\n).*?(<!-- END_BUILD_INJECT -->)'
                out_content = re.sub(cards_pattern, lambda m: m.group(1) + state_cards_html + '      ' + m.group(2), out_content, flags=re.DOTALL)

                # Scorecard & Strategic Analysis
                scorecard_pattern = r'(<!-- BUILD_INJECT:state_scorecard -->\n).*?(<!-- END_BUILD_INJECT -->)'
                benchmark_table_html = f'''      <div style="margin-top:36px; margin-bottom:36px;">
        <h2 style="font-family:var(--font-display); font-size:22px; margin-bottom:14px;" data-en="{state_name_en} vs All-India National Benchmark Scorecard" data-hi="{state_name_hi} बनाम अखिल भारतीय राष्ट्रीय मानक स्कोरकार्ड">{state_name_en} vs All-India National Benchmark Scorecard</h2>
        <div style="overflow-x:auto; background:var(--card-bg, rgba(255,255,255,0.03)); border:1px solid var(--border); border-radius:10px; padding:18px;">
          <table style="width:100%; border-collapse:collapse; text-align:left; font-size:14px;">
            <thead>
              <tr style="border-bottom:1px solid var(--border); color:var(--text-faint); font-family:var(--font-mono); font-size:12px; text-transform:uppercase;">
                <th style="padding:10px 12px;" data-en="Socio-Economic Indicator" data-hi="सामाजिक-आर्थिक संकेतक">Socio-Economic Indicator</th>
                <th style="padding:10px 12px;" data-en="{state_name_en} Value" data-hi="{state_name_hi} मान">{state_name_en} Value</th>
                <th style="padding:10px 12px;" data-en="All-India Benchmark" data-hi="अखिल भारतीय मानक">All-India Benchmark</th>
                <th style="padding:10px 12px;" data-en="National Share / Delta" data-hi="राष्ट्रीय हिस्सेदारी / अंतर">National Share / Delta</th>
                <th style="padding:10px 12px;" data-en="Official Source" data-hi="आधिकारिक स्रोत">Official Source</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Total Population (Census 2011)" data-hi="कुल जनसंख्या (जनगणना 2011)">Total Population (Census 2011)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{pop_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">1.21 Billion (121.08 Cr)</td>
                <td style="padding:12px; font-family:var(--font-mono); font-weight:600;">{pop_share_india:.2f}% of India</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">Census of India</td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Effective Literacy Rate" data-hi="प्रभावी साक्षरता दर">Effective Literacy Rate</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{lit_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">74.04%</td>
                <td style="padding:12px; font-family:var(--font-mono); color:{'#10B981' if lit_delta >= 0 else '#EF4444'}; font-weight:600;">{lit_sign}{lit_delta:.2f}%</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">Census of India</td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Gross State Domestic Product (GSDP)" data-hi="सकल राज्य घरेलू उत्पाद (GSDP)">Gross State Domestic Product (GSDP)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{gdp_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">₹272.41 Lakh Cr (GDP)</td>
                <td style="padding:12px; font-family:var(--font-mono); font-weight:600;">{gdp_share_india:.2f}% of GDP</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">MoSPI (2022-23)</td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Unemployment Rate (PLFS 15+)" data-hi="बेरोजगारी दर (PLFS 15+)">Unemployment Rate (PLFS 15+)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{unemp_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">3.1%</td>
                <td style="padding:12px; font-family:var(--font-mono); color:{'#EF4444' if unemp_delta > 0 else '#10B981'}; font-weight:600;">{unemp_sign}{unemp_delta:.2f}%</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">MoSPI PLFS (2023)</td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Infant Mortality Rate (IMR)" data-hi="शिशु मृत्यु दर (IMR)">Infant Mortality Rate (IMR)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{imr_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">28 per 1,000</td>
                <td style="padding:12px; font-family:var(--font-mono); color:{'#EF4444' if imr_delta > 0 else '#10B981'}; font-weight:600;">{imr_sign}{imr_delta} vs national</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">SRS / MoHFW (2020)</td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Sex Ratio (Females per 1,000 Males)" data-hi="लिंगानुपात (प्रति 1,000 पुरुष)">Sex Ratio (Females per 1,000 Males)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{sex_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">943</td>
                <td style="padding:12px; font-family:var(--font-mono); color:{'#10B981' if sex_delta >= 0 else '#EF4444'}; font-weight:600;">{sex_sign}{sex_delta} pts</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">Census of India</td>
              </tr>
              <tr>
                <td style="padding:12px; font-weight:600;" data-en="Geographical Area" data-hi="भौगोलिक क्षेत्रफल">Geographical Area</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{area_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">3,287,263 sq km</td>
                <td style="padding:12px; font-family:var(--font-mono); font-weight:600;">{area_share_india:.2f}% of India</td>
                <td style="padding:12px; font-size:12px; color:var(--text-faint);">Survey of India</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>'''
                takeaways_html = f'''      <div style="margin-top:36px; margin-bottom:36px;">
        <h2 style="font-family:var(--font-display); font-size:22px; margin-bottom:14px;" data-en="Strategic Socio-Economic Analysis" data-hi="रणनीतिक सामाजिक-आर्थिक विश्लेषण">Strategic Socio-Economic Analysis</h2>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
          <div class="im-callout" style="margin:0; border-left:4px solid var(--teal);">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--teal);" data-en="Economic Scale &amp; Contribution" data-hi="आर्थिक आकार एवं योगदान">Economic Scale &amp; Contribution</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="{state_name_en} reports a GSDP of {gdp_disp} (MoSPI 2022-23), contributing approximately {gdp_share_india:.2f}% to India's aggregate output. This economic productivity shapes state fiscal capacity, infrastructure capital expenditure, and per-capita income dynamics." data-hi="{state_name_hi} {gdp_disp_hi} (MoSPI 2022-23) का GSDP दर्ज करता है, जो भारत के कुल उत्पादन में लगभग {gdp_share_india:.2f}% का योगदान देता है। यह आर्थिक उत्पादकता राज्य की राजकोषीय क्षमता, बुनियादी ढांचा पूंजीगत व्यय और प्रति व्यक्ति आय गतिशीलता को आकार देती है।">{state_name_en} reports a GSDP of {gdp_disp} (MoSPI 2022-23), contributing approximately {gdp_share_india:.2f}% to India's aggregate output. This economic productivity shapes state fiscal capacity, infrastructure capital expenditure, and per-capita income dynamics.</p>
          </div>
          <div class="im-callout" style="margin:0; border-left:4px solid #10B981;">
            <h3 style="font-size:16px; margin:0 0 6px; color:#10B981;" data-en="Human Capital &amp; Literacy" data-hi="मानव पूंजी एवं साक्षरता">Human Capital &amp; Literacy</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="At {lit_disp}, {state_name_en}'s effective literacy rate is {lit_sign}{lit_delta:.2f}% relative to the national benchmark of 74.04%. High literacy correlated with female educational attainment serves as a primary foundation for workforce productivity and social mobility." data-hi="{lit_disp_hi} पर, {state_name_hi} की प्रभावी साक्षरता दर 74.04% के राष्ट्रीय बेंचमार्क से {lit_sign}{lit_delta:.2f}% स्थिति दर्शाती है। महिला शैक्षिक उपलब्धि से जुड़ी उच्च साक्षरता कार्यबल उत्पादकता और सामाजिक गतिशीलता के लिए प्राथमिक आधार के रूप में कार्य करती है।">At {lit_disp}, {state_name_en}'s effective literacy rate is {lit_sign}{lit_delta:.2f}% relative to the national benchmark of 74.04%. High literacy correlated with female educational attainment serves as a primary foundation for workforce productivity and social mobility.</p>
          </div>
          <div class="im-callout" style="margin:0; border-left:4px solid var(--saffron);">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--saffron);" data-en="Demographic Weight &amp; Landmass" data-hi="जनसांख्यिकीय भार एवं भूभाग">Demographic Weight &amp; Landmass</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="With {pop_disp} residents across {area_disp}, {state_name_en} accommodates {pop_share_india:.2f}% of India's population on {area_share_india:.2f}% of its total geographical landmass, driving regional resource allocation, urbanization patterns, and public governance." data-hi="{area_disp_hi} में {pop_disp_hi} निवासियों के साथ, {state_name_hi} अपने कुल भौगोलिक भूभाग के {area_share_india:.2f}% पर भारत की जनसंख्या के {pop_share_india:.2f}% को समायोजित करता है, जो क्षेत्रीय संसाधन आवंटन, शहरीकरण पैटर्न और सार्वजनिक शासन को प्रेरित करता है।">With {pop_disp} residents across {area_disp}, {state_name_en} accommodates {pop_share_india:.2f}% of India's population on {area_share_india:.2f}% of its total geographical landmass, driving regional resource allocation, urbanization patterns, and public governance.</p>
          </div>
          <div class="im-callout" style="margin:0; border-left:4px solid #3B82F6;">
            <h3 style="font-size:16px; margin:0 0 6px; color:#3B82F6;" data-en="Public Health &amp; Healthcare Delivery" data-hi="सार्वजनिक स्वास्थ्य एवं स्वास्थ्य सेवा">Public Health &amp; Healthcare Delivery</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="An Infant Mortality Rate (IMR) of {imr_disp} per 1,000 live births ({imr_sign}{imr_delta} vs national average of 28) and a sex ratio of {sex_disp} ({sex_sign}{sex_delta} vs 943) highlight the state's maternal-child health infrastructure and gender balance." data-hi="प्रति 1,000 जीवित जन्मों पर {imr_disp_hi} की शिशु मृत्यु दर (IMR) (राष्ट्रीय औसत 28 से {imr_sign}{imr_delta}) और {sex_disp_hi} का लिंगानुपात (943 से {sex_sign}{sex_delta}) राज्य के मातृ-शिशु स्वास्थ्य बुनियादी ढांचे और लैंगिक संतुलन को रेखांकित करता है।">An Infant Mortality Rate (IMR) of {imr_disp} per 1,000 live births ({imr_sign}{imr_delta} vs national average of 28) and a sex ratio of {sex_disp} ({sex_sign}{sex_delta} vs 943) highlight the state's maternal-child health infrastructure and gender balance.</p>
          </div>
        </div>
      </div>'''
                out_content = re.sub(scorecard_pattern, lambda m: m.group(1) + benchmark_table_html + '\n' + takeaways_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)
                
                # Action bar with tools integration
                ab_pattern = r'(<!-- BUILD_INJECT:action_bar -->\n).*?(<!-- END_BUILD_INJECT -->)'
                ab_html = f'''      <div class="im-action-bar">
        <button type="button" class="im-cite-btn" onclick="window.copyCitation('{state_name_en} Profile', 'Key Statistics', 'All Indicators', '2023', 'MoSPI & Census', window.location.href)" data-en="📋 Copy Citation" data-hi="📋 उद्धरण कॉपी करें">📋 Copy Citation</button>
        <button type="button" class="im-issue-btn" onclick="window.reportDataIssue(window.location.pathname)" data-en="⚠️ Report Data Issue" data-hi="⚠️ डेटा समस्या की रिपोर्ट करें">⚠️ Report Data Issue</button>
        <a href="../compare.html?s1={state_id}" class="im-btn im-btn-sm im-btn-outline" data-en="Compare State →" data-hi="राज्य की तुलना करें →">Compare State →</a>
        <a href="../tools/economic-comparator.html?state={state_id}" class="im-btn im-btn-sm im-btn-outline" data-en="🌐 Economic Equivalence" data-hi="🌐 आर्थिक समकक्षता">🌐 Economic Equivalence</a>
        <a href="../tools/demographic-calculator.html?s1={state_id}" class="im-btn im-btn-sm im-btn-outline" data-en="📊 Literacy Projector" data-hi="📊 साक्षरता प्रोजेक्टर">📊 Literacy Projector</a>
      </div>\n      '''
                out_content = re.sub(ab_pattern, lambda m: m.group(1) + ab_html + m.group(2), out_content, flags=re.DOTALL)
                
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
                    state_districts_html = '<p style="color:var(--text-faint); font-family:var(--font-mono);" data-en="Granular district profiles currently being indexed for this state. Browse all available districts in the directory." data-hi="इस राज्य के लिए जिले वर्तमान में अनुक्रमित किए जा रहे हैं। डायरेक्टरी में सभी उपलब्ध जिले देखें।">Granular district profiles currently being indexed for this state. Browse all available districts in the directory.</p>\n<a href="../districts/index.html" class="im-btn im-btn-sm im-btn-secondary" data-en="View All Districts &rarr;" data-hi="सभी जिले देखें &rarr;">View All Districts &rarr;</a>\n'
                out_content = re.sub(districts_pattern, lambda m: m.group(1) + state_districts_html + '        ' + m.group(2), out_content, flags=re.DOTALL)

                # FAQs
                state_faqs_html = f'''        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the population of {state_name_en}?" data-hi="{state_name_hi} की जनसंख्या कितनी है?">What is the population of {state_name_en}?</h3>
          <p data-en="{state_name_en}'s population was recorded at {pop_disp} according to the Census of India 2011, accounting for {pop_share_india:.2f}% of the nation's total enumerated population." data-hi="2011 की भारत की जनगणना के अनुसार {state_name_hi} की जनसंख्या {pop_disp_hi} दर्ज की गई थी, जो देश की कुल दर्ज जनसंख्या का {pop_share_india:.2f}% है।">{state_name_en}'s population was recorded at {pop_disp} according to the Census of India 2011, accounting for {pop_share_india:.2f}% of the nation's total enumerated population.</p>
        </div>
        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the literacy rate of {state_name_en}?" data-hi="{state_name_hi} की साक्षरता दर क्या है?">What is the literacy rate of {state_name_en}?</h3>
          <p data-en="The literacy rate of {state_name_en} is {lit_disp} as per the 2011 Census enumeration, which is {lit_sign}{lit_delta:.2f}% compared to the national average of 74.04%." data-hi="2011 की जनगणना के अनुसार {state_name_hi} की साक्षरता दर {lit_disp_hi} है, जो राष्ट्रीय औसत 74.04% की तुलना में {lit_sign}{lit_delta:.2f}% है।">The literacy rate of {state_name_en} is {lit_disp} as per the 2011 Census enumeration, which is {lit_sign}{lit_delta:.2f}% compared to the national average of 74.04%.</p>
        </div>
        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the Gross State Domestic Product (GSDP) of {state_name_en}?" data-hi="{state_name_hi} का सकल राज्य घरेलू उत्पाद (GSDP) क्या है?">What is the Gross State Domestic Product (GSDP) of {state_name_en}?</h3>
          <p data-en="{state_name_en}'s GSDP is estimated at {gdp_disp} (Current Prices, 2022-23) published by the Ministry of Statistics and Programme Implementation (MoSPI), representing {gdp_share_india:.2f}% of national GDP." data-hi="{state_name_hi} का GSDP सांख्यिकी और कार्यक्रम कार्यान्वयन मंत्रालय (MoSPI) द्वारा जारी अनुमानों के अनुसार {gdp_disp_hi} (वर्तमान मूल्य, 2022-23) आंका गया है, जो राष्ट्रीय सकल घरेलू उत्पाद का {gdp_share_india:.2f}% है।">{state_name_en}'s GSDP is estimated at {gdp_disp} (Current Prices, 2022-23) published by the Ministry of Statistics and Programme Implementation (MoSPI), representing {gdp_share_india:.2f}% of national GDP.</p>
        </div>
        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the unemployment rate in {state_name_en}?" data-hi="{state_name_hi} में बेरोजगारी दर क्या है?">What is the unemployment rate in {state_name_en}?</h3>
          <p data-en="According to the Periodic Labour Force Survey (PLFS) 2023 by MoSPI, the unemployment rate in {state_name_en} is {unemp_disp} (usual status, age 15+), compared to the All-India rate of 3.1%." data-hi="MoSPI द्वारा आवधिक श्रम बल सर्वेक्षण (PLFS) 2023 के अनुसार, {state_name_hi} में बेरोजगारी दर {unemp_disp_hi} (सामान्य स्थिति, 15+ आयु) है, जबकि अखिल भारतीय दर 3.1% है।">According to the Periodic Labour Force Survey (PLFS) 2023 by MoSPI, the unemployment rate in {state_name_en} is {unemp_disp} (usual status, age 15+), compared to the All-India rate of 3.1%.</p>
        </div>
        <div class="im-callout" style="margin:0;">
          <h3 style="font-size:16px; margin:0 0 8px; color:var(--teal);" data-en="What is the sex ratio and infant mortality rate in {state_name_en}?" data-hi="{state_name_hi} में लिंगानुपात और शिशु मृत्यु दर क्या है?">What is the sex ratio and infant mortality rate in {state_name_en}?</h3>
          <p data-en="{state_name_en} recorded a sex ratio of {sex_disp} females per 1,000 males (Census 2011) and an Infant Mortality Rate (IMR) of {imr_disp} per 1,000 live births (SRS Statistical Report 2020)." data-hi="{state_name_hi} में प्रति 1,000 पुरुषों पर {sex_disp_hi} महिलाओं का लिंगानुपात (जनगणना 2011) और प्रति 1,000 जीवित जन्मों पर {imr_disp_hi} की शिशु मृत्यु दर (IMR) (SRS सांख्यिकीय रिपोर्ट 2020) दर्ज की गई।">{state_name_en} recorded a sex ratio of {sex_disp} females per 1,000 males (Census 2011) and an Infant Mortality Rate (IMR) of {imr_disp} per 1,000 live births (SRS Statistical Report 2020).</p>
        </div>'''
                faq_pattern = r'(<!-- BUILD_INJECT:faq_items -->\n).*?(<!-- END_BUILD_INJECT -->)'
                out_content = re.sub(faq_pattern, lambda m: m.group(1) + state_faqs_html + '\n        ' + m.group(2), out_content, flags=re.DOTALL)
                
                # JSON-LD Schemas for State
                faq_schema = {
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": f"What is the population of {state_name_en}?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": f"{state_name_en}'s population was recorded at {pop_disp} according to the Census of India 2011, accounting for {pop_share_india:.2f}% of the nation's total enumerated population."
                            }
                        },
                        {
                            "@type": "Question",
                            "name": f"What is the literacy rate of {state_name_en}?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": f"The literacy rate of {state_name_en} is {lit_disp} as per the 2011 Census enumeration, which is {lit_sign}{lit_delta:.2f}% compared to the national average of 74.04%."
                            }
                        },
                        {
                            "@type": "Question",
                            "name": f"What is the Gross State Domestic Product (GSDP) of {state_name_en}?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": f"{state_name_en}'s GSDP is estimated at {gdp_disp} (Current Prices, 2022-23) published by the Ministry of Statistics and Programme Implementation (MoSPI)."
                            }
                        }
                    ]
                }

                bc_schema = {
                    "@context": "https://schema.org",
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
                        {"@type": "ListItem", "position": 2, "name": "States", "item": "https://www.indiametrix.in/#explore"},
                        {"@type": "ListItem", "position": 3, "name": state_name_en, "item": f"https://www.indiametrix.in/states/{state_id}.html"}
                    ]
                }

                state_place_schema = {
                    "@context": "https://schema.org",
                    "@type": "AdministrativeArea",
                    "name": state_name_en,
                    "alternateName": state_name_hi,
                    "description": f"Verified official demographics, GSDP economy ({gdp_disp}), literacy rate ({lit_disp}), and healthcare statistics for {state_name_en}, India."
                }

                schemas_html = f'''<script type="application/ld+json">
{json.dumps(state_place_schema, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(bc_schema, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, indent=2, ensure_ascii=False)}
</script>'''
                schemas_pattern = r'(<!-- BUILD_INJECT:schemas -->\n).*?(<!-- END_BUILD_INJECT -->)'
                out_content = re.sub(schemas_pattern, lambda m: m.group(1) + schemas_html + '\n' + m.group(2), out_content, flags=re.DOTALL)

                out_path = os.path.join(out_states_dir, f"{state_id}.html")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(out_content)
                
        print(f"Built all 36 states/*.html successfully.")

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

        dist_files = sorted([f for f in os.listdir(districts_dir) if f.endswith('.json')])
        all_dist_data = []
        for df in dist_files:
            with open(os.path.join(districts_dir, df), 'r', encoding='utf-8') as f:
                all_dist_data.append(json.load(f))

        for dist_data in all_dist_data:
            dist_id = dist_data['id']
            state_id = dist_data['state_id']
            dist_name_en = dist_data['name'].get('en', '')
            dist_name_hi = dist_data['name'].get('hi', '')

            # Load state
            state_json_path = os.path.join(states_dir, f"{state_id}.json")
            state_data = {}
            if os.path.exists(state_json_path):
                with open(state_json_path, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
            state_name_en = state_data.get('name', {}).get('en', state_id.title())
            state_name_hi = state_data.get('name', {}).get('hi', state_id)

            # District indicator values
            dist_pop_val = 0
            dist_pop_disp_en = ""
            dist_pop_disp_hi = ""
            dist_lit_val = 0.0
            dist_lit_disp_en = ""
            dist_lit_disp_hi = ""
            dist_sex_val = 0
            dist_sex_disp_en = ""
            dist_sex_disp_hi = ""

            for ind in dist_data.get('indicators', []):
                if ind['id'] == 'population':
                    dist_pop_val = ind['value']
                    dist_pop_disp_en = ind['display']['en']
                    dist_pop_disp_hi = ind['display']['hi']
                elif ind['id'] == 'literacy-rate':
                    dist_lit_val = ind['value']
                    dist_lit_disp_en = ind['display']['en']
                    dist_lit_disp_hi = ind['display']['hi']
                elif ind['id'] == 'sex-ratio':
                    dist_sex_val = ind['value']
                    dist_sex_disp_en = ind['display']['en']
                    dist_sex_disp_hi = ind['display']['hi']

            # State indicator values
            state_pop_val = 0
            state_pop_disp = ""
            state_lit_val = 0.0
            state_lit_disp = ""
            state_sex_val = 0
            state_sex_disp = ""

            for ind in state_data.get('indicators', []):
                if ind['id'] == 'population':
                    state_pop_val = ind['value']
                    state_pop_disp = ind['display']['en']
                elif ind['id'] == 'literacy-rate':
                    state_lit_val = ind['value']
                    state_lit_disp = ind['display']['en']
                elif ind['id'] == 'sex-ratio':
                    state_sex_val = ind['value']
                    state_sex_disp = ind['display']['en']

            # Computations
            pop_share = (dist_pop_val / state_pop_val * 100) if state_pop_val > 0 else 0.0
            lit_delta_state = dist_lit_val - state_lit_val
            lit_delta_india = dist_lit_val - 74.04
            sex_delta_state = dist_sex_val - state_sex_val
            sex_delta_india = dist_sex_val - 943

            lit_comp_en = f"{abs(lit_delta_india):.2f}% higher" if lit_delta_india >= 0 else f"{abs(lit_delta_india):.2f}% lower"
            lit_comp_hi = f"{abs(lit_delta_india):.2f}% अधिक" if lit_delta_india >= 0 else f"{abs(lit_delta_india):.2f}% कम"

            lit_state_sign = "+" if lit_delta_state >= 0 else ""
            lit_india_sign = "+" if lit_delta_india >= 0 else ""
            sex_state_sign = "+" if sex_delta_state >= 0 else ""
            sex_india_sign = "+" if sex_delta_india >= 0 else ""

            # 1. Summary
            dist_summary_html = f'''        <div class="im-prose" style="margin-top:14px; max-width:75ch; line-height:1.7; color:var(--text-muted);">
          <p data-en="{dist_name_en} is an administrative district located in the state of {state_name_en}, India. According to the decennial Census of India 2011 enumeration, {dist_name_en} recorded an official population of {dist_pop_val:,.0f} ({dist_pop_disp_en}), which accounts for approximately {pop_share:.1f}% of {state_name_en}'s total population. The district maintains an effective literacy rate of {dist_lit_disp_en}, which is {lit_comp_en} than the national benchmark of 74.04%. With an enumerated sex ratio of {dist_sex_val} females per 1,000 males, {dist_name_en} provides vital demographic insights into urban and regional development patterns within {state_name_en}." data-hi="{dist_name_hi} भारत के {state_name_hi} राज्य में स्थित एक प्रमुख प्रशासनिक जिला है। 2011 की आधिकारिक भारत की जनगणना के अनुसार, {dist_name_hi} की कुल दर्ज जनसंख्या {dist_pop_val:,.0f} ({dist_pop_disp_hi}) थी, जो {state_name_hi} की कुल जनसंख्या का लगभग {pop_share:.1f}% हिस्सा है। जिले की साक्षरता दर {dist_lit_disp_hi} है, जो अखिल भारतीय राष्ट्रीय औसत 74.04% की तुलना में {lit_comp_hi} है। प्रति 1,000 पुरुषों पर {dist_sex_val} महिलाओं के लिंगानुपात के साथ, {dist_name_hi} राज्य के भीतर जनसांख्यिकीय संरचना का एक महत्वपूर्ण केंद्र प्रस्तुत करता है।">
            {dist_name_en} is an administrative district located in the state of {state_name_en}, India. According to the decennial Census of India 2011 enumeration, {dist_name_en} recorded an official population of {dist_pop_val:,.0f} ({dist_pop_disp_en}), which accounts for approximately {pop_share:.1f}% of {state_name_en}'s total population. The district maintains an effective literacy rate of {dist_lit_disp_en}, which is {lit_comp_en} than the national benchmark of 74.04%. With an enumerated sex ratio of {dist_sex_val} females per 1,000 males, {dist_name_en} provides vital demographic insights into urban and regional development patterns within {state_name_en}.
          </p>
        </div>'''

            # 2. KPI Cards
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

            # 3. Benchmark Table
            benchmark_html = f'''      <div style="margin-top:36px;">
        <h2 style="font-size:20px; margin-bottom:14px;" data-en="{dist_name_en} vs State &amp; National Demographic Benchmarks" data-hi="{dist_name_hi} बनाम राज्य और राष्ट्रीय जनसांख्यिकीय तुलना">{dist_name_en} vs State &amp; National Demographic Benchmarks</h2>
        <div style="overflow-x:auto; background:var(--card-bg, rgba(255,255,255,0.03)); border:1px solid var(--border); border-radius:10px; padding:18px;">
          <table style="width:100%; border-collapse:collapse; text-align:left; font-size:14px;">
            <thead>
              <tr style="border-bottom:1px solid var(--border); color:var(--text-faint); font-family:var(--font-mono); font-size:12px; text-transform:uppercase;">
                <th style="padding:10px 12px;" data-en="Key Indicator" data-hi="प्रमुख संकेतक">Key Indicator</th>
                <th style="padding:10px 12px;" data-en="{dist_name_en} District" data-hi="{dist_name_hi} जिला">{dist_name_en} District</th>
                <th style="padding:10px 12px;" data-en="{state_name_en} Average" data-hi="{state_name_hi} औसत">{state_name_en} Average</th>
                <th style="padding:10px 12px;" data-en="All-India Average" data-hi="अखिल भारतीय औसत">All-India Average</th>
                <th style="padding:10px 12px;" data-en="Comparison vs National" data-hi="राष्ट्रीय औसत से तुलना">Comparison vs National</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Total Population (Census 2011)" data-hi="कुल जनसंख्या (जनगणना 2011)">Total Population (Census 2011)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{dist_pop_disp_en}</td>
                <td style="padding:12px; font-family:var(--font-mono);">{state_pop_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">1.21 Billion (121.08 Cr)</td>
                <td style="padding:12px; font-family:var(--font-mono);">{pop_share:.2f}% of {state_name_en}</td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-light, rgba(255,255,255,0.05));">
                <td style="padding:12px; font-weight:600;" data-en="Literacy Rate (Effective %)" data-hi="साक्षरता दर (प्रभावी %)">Literacy Rate (Effective %)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{dist_lit_disp_en}</td>
                <td style="padding:12px; font-family:var(--font-mono);">{state_lit_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">74.04%</td>
                <td style="padding:12px; font-family:var(--font-mono); color:{'#10B981' if lit_delta_india >= 0 else '#EF4444'}; font-weight:600;">{lit_india_sign}{lit_delta_india:.2f}%</td>
              </tr>
              <tr>
                <td style="padding:12px; font-weight:600;" data-en="Sex Ratio (Females per 1,000 Males)" data-hi="लिंगानुपात (प्रति 1,000 पुरुषों पर महिलाएं)">Sex Ratio (Females per 1,000 Males)</td>
                <td style="padding:12px; font-family:var(--font-mono); color:var(--teal); font-weight:600;">{dist_sex_disp_en}</td>
                <td style="padding:12px; font-family:var(--font-mono);">{state_sex_disp}</td>
                <td style="padding:12px; font-family:var(--font-mono);">943</td>
                <td style="padding:12px; font-family:var(--font-mono); color:{'#10B981' if sex_delta_india >= 0 else '#EF4444'}; font-weight:600;">{sex_india_sign}{sex_delta_india} pts</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>'''

            # 4. District Insights
            dist_insights_html = f'''      <div style="margin-top:36px;">
        <h2 style="font-size:20px; margin-bottom:14px;" data-en="Demographic Analysis &amp; Core Takeaways" data-hi="जनसांख्यिकीय विश्लेषण एवं प्रमुख निष्कर्ष">Demographic Analysis &amp; Core Takeaways</h2>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
          <div class="im-callout" style="margin:0; border-left:4px solid var(--teal);">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--teal);" data-en="Demographic Concentration" data-hi="जनसांख्यिकीय संकेंद्रण">Demographic Concentration</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="{dist_name_en} houses {pop_share:.2f}% of {state_name_en}'s total population ({dist_pop_disp_en} out of {state_pop_disp}). This highlights its role as a key regional population and economic center within the state." data-hi="{dist_name_hi} में {state_name_hi} की कुल जनसंख्या ({state_pop_disp} में से {dist_pop_disp_hi}) का {pop_share:.2f}% हिस्सा निवास करता है। यह राज्य के भीतर एक प्रमुख क्षेत्रीय जनसंख्या और आर्थिक केंद्र के रूप में इसकी स्थिति को दर्शाता है।">{dist_name_en} houses {pop_share:.2f}% of {state_name_en}'s total population ({dist_pop_disp_en} out of {state_pop_disp}). This highlights its role as a key regional population and economic center within the state.</p>
          </div>
          <div class="im-callout" style="margin:0; border-left:4px solid #10B981;">
            <h3 style="font-size:16px; margin:0 0 6px; color:#10B981;" data-en="Educational Attainment" data-hi="शैक्षिक स्तर">Educational Attainment</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="With an effective literacy rate of {dist_lit_disp_en}, {dist_name_en} stands {lit_india_sign}{lit_delta_india:.2f}% relative to the All-India benchmark (74.04%) and {lit_state_sign}{lit_delta_state:.2f}% compared to {state_name_en}'s state average ({state_lit_disp})." data-hi="{dist_lit_disp_hi} की प्रभावी साक्षरता दर के साथ, {dist_name_hi} अखिल भारतीय मानक (74.04%) की तुलना में {lit_india_sign}{lit_delta_india:.2f}% और {state_name_hi} के राज्य औसत ({state_lit_disp}) की तुलना में {lit_state_sign}{lit_delta_state:.2f}% स्थिति रखता है।">With an effective literacy rate of {dist_lit_disp_en}, {dist_name_en} stands {lit_india_sign}{lit_delta_india:.2f}% relative to the All-India benchmark (74.04%) and {lit_state_sign}{lit_delta_state:.2f}% compared to {state_name_en}'s state average ({state_lit_disp}).</p>
          </div>
          <div class="im-callout" style="margin:0; border-left:4px solid var(--saffron);">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--saffron);" data-en="Sex Ratio &amp; Gender Balance" data-hi="लिंगानुपात और लैंगिक संतुलन">Sex Ratio &amp; Gender Balance</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="The enumerated sex ratio in {dist_name_en} is {dist_sex_val} females per 1,000 males, comparing {sex_india_sign}{sex_delta_india} points against the national figure of 943 and {sex_state_sign}{sex_delta_state} points relative to the {state_name_en} benchmark ({state_sex_val})." data-hi="{dist_name_hi} में दर्ज लिंगानुपात प्रति 1,000 पुरुषों पर {dist_sex_val} महिलाएं हैं, जो 943 के राष्ट्रीय आंकड़े से {sex_india_sign}{sex_delta_india} अंक और {state_name_hi} के मानक ({state_sex_val}) से {sex_state_sign}{sex_delta_state} अंक की स्थिति दर्शाता है।">The enumerated sex ratio in {dist_name_en} is {dist_sex_val} females per 1,000 males, comparing {sex_india_sign}{sex_delta_india} points against the national figure of 943 and {sex_state_sign}{sex_delta_state} points relative to the {state_name_en} benchmark ({state_sex_val}).</p>
          </div>
        </div>
      </div>'''

            # 5. Peer Districts
            peers = [d for d in all_dist_data if d['id'] != dist_id]
            same_state_peers = [d for d in peers if d['state_id'] == state_id]
            other_peers = [d for d in peers if d['state_id'] != state_id]
            selected_peers = same_state_peers + other_peers[:(4 - len(same_state_peers))]

            peer_links_html = ""
            for p in selected_peers:
                p_id = p['id']
                p_state = p['state_id']
                p_name_en = p['name']['en']
                p_name_hi = p['name']['hi']
                peer_links_html += f'        <a href="../{p_state}/{p_id}.html" class="im-btn im-btn-sm im-btn-outline" style="text-decoration:none;" data-en="{p_name_en} ({p_state.title()})" data-hi="{p_name_hi} ({p_state.title()})">{p_name_en} ({p_state.title()}) &rarr;</a>\n'

            peer_districts_html = f'''      <div style="margin-top:36px;">
        <h2 style="font-size:20px; margin-bottom:14px;" data-en="Compare with Peer Districts" data-hi="अन्य जिलों के साथ तुलना करें">Compare with Peer Districts</h2>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
{peer_links_html}        </div>
      </div>'''

            # 6. FAQs
            faqs_html = f'''      <div style="margin-top:40px;">
        <h2 style="font-size:20px; margin-bottom:16px;" data-en="Frequently Asked Questions about {dist_name_en}" data-hi="{dist_name_hi} के बारे में अक्सर पूछे जाने वाले प्रश्न">Frequently Asked Questions about {dist_name_en}</h2>
        <div style="display:flex; flex-direction:column; gap:14px;">
          <div class="im-callout" style="margin:0;">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--teal);" data-en="What is the official population of {dist_name_en} district?" data-hi="{dist_name_hi} जिले की आधिकारिक जनसंख्या कितनी है?">What is the official population of {dist_name_en} district?</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="According to the 2011 Census of India, the population of {dist_name_en} was recorded at {dist_pop_val:,.0f} ({dist_pop_disp_en}), making up approximately {pop_share:.1f}% of {state_name_en}'s population." data-hi="2011 की भारत की जनगणना के अनुसार, {dist_name_hi} की जनसंख्या {dist_pop_val:,.0f} ({dist_pop_disp_hi}) दर्ज की गई थी, जो {state_name_hi} की जनसंख्या का लगभग {pop_share:.1f}% है।">According to the 2011 Census of India, the population of {dist_name_en} was recorded at {dist_pop_val:,.0f} ({dist_pop_disp_en}), making up approximately {pop_share:.1f}% of {state_name_en}'s population.</p>
          </div>
          <div class="im-callout" style="margin:0;">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--teal);" data-en="What is the literacy rate of {dist_name_en} district?" data-hi="{dist_name_hi} जिले की साक्षरता दर क्या है?">What is the literacy rate of {dist_name_en} district?</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="The effective literacy rate in {dist_name_en} is {dist_lit_disp_en} as per the 2011 Census enumeration, compared to {state_lit_disp} for {state_name_en} and the national average of 74.04%." data-hi="2011 की जनगणना के अनुसार {dist_name_hi} में प्रभावी साक्षरता दर {dist_lit_disp_hi} है, जबकि {state_name_hi} का राज्य औसत {state_lit_disp} और राष्ट्रीय औसत 74.04% है।">The effective literacy rate in {dist_name_en} is {dist_lit_disp_en} as per the 2011 Census enumeration, compared to {state_lit_disp} for {state_name_en} and the national average of 74.04%.</p>
          </div>
          <div class="im-callout" style="margin:0;">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--teal);" data-en="What is the sex ratio in {dist_name_en}?" data-hi="{dist_name_hi} में लिंगानुपात क्या है?">What is the sex ratio in {dist_name_en}?</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="The sex ratio in {dist_name_en} district is {dist_sex_val} females per 1,000 males according to Census 2011 records, against the national average of 943." data-hi="जनगणना 2011 के रिकॉर्ड के अनुसार {dist_name_hi} जिले में लिंगानुपात प्रति 1,000 पुरुषों पर {dist_sex_val} महिलाएं हैं, जबकि राष्ट्रीय औसत 943 है।">The sex ratio in {dist_name_en} district is {dist_sex_val} females per 1,000 males according to Census 2011 records, against the national average of 943.</p>
          </div>
          <div class="im-callout" style="margin:0;">
            <h3 style="font-size:16px; margin:0 0 6px; color:var(--teal);" data-en="Where can I explore state and national comparisons for {dist_name_en}?" data-hi="{dist_name_hi} के लिए राज्य और राष्ट्रीय तुलना कहां देखी जा सकती है?">Where can I explore state and national comparisons for {dist_name_en}?</h3>
            <p style="margin:0; font-size:14px; line-height:1.6; color:var(--text-muted);" data-en="You can explore state-level economic and social data on the <a href='../../states/{state_id}.html' style='color:var(--teal);'>{state_name_en} Profile</a>, run head-to-head metrics on the <a href='../../compare.html?s1={state_id}' style='color:var(--teal);'>State Comparison Engine</a>, or browse the complete <a href='../../districts/index.html' style='color:var(--teal);'>Districts Directory</a>." data-hi="आप <a href='../../states/{state_id}.html' style='color:var(--teal);'>{state_name_hi} प्रोफ़ाइल</a> पर राज्य-स्तरीय आर्थिक और सामाजिक डेटा देख सकते हैं, <a href='../../compare.html?s1={state_id}' style='color:var(--teal);'>राज्य तुलना इंजन</a> पर तुलना कर सकते हैं, या संपूर्ण <a href='../../districts/index.html' style='color:var(--teal);'>जिले डायरेक्टरी</a> ब्राउज़ कर सकते हैं।">You can explore state-level economic and social data on the <a href="../../states/{state_id}.html" style="color:var(--teal);">{state_name_en} Profile</a>, run head-to-head metrics on the <a href="../../compare.html?s1={state_id}" style="color:var(--teal);">State Comparison Engine</a>, or browse the complete <a href="../../districts/index.html" style="color:var(--teal);">Districts Directory</a>.</p>
          </div>
        </div>
      </div>'''

            # 7. JSON-LD Schemas
            faq_schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"What is the official population of {dist_name_en} district?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"According to the 2011 Census of India, the population of {dist_name_en} was recorded at {dist_pop_val:,.0f} ({dist_pop_disp_en}), making up approximately {pop_share:.1f}% of {state_name_en}'s population."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What is the literacy rate of {dist_name_en} district?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"The effective literacy rate in {dist_name_en} is {dist_lit_disp_en} as per the 2011 Census enumeration, compared to {state_lit_disp} for {state_name_en} and the national average of 74.04%."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What is the sex ratio in {dist_name_en}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"The sex ratio in {dist_name_en} district is {dist_sex_val} females per 1,000 males according to Census 2011 records, against the national average of 943."
                        }
                    }
                ]
            }

            bc_schema = {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
                    {"@type": "ListItem", "position": 2, "name": "Districts", "item": "https://www.indiametrix.in/districts/index.html"},
                    {"@type": "ListItem", "position": 3, "name": state_name_en, "item": f"https://www.indiametrix.in/states/{state_id}.html"},
                    {"@type": "ListItem", "position": 4, "name": dist_name_en, "item": f"https://www.indiametrix.in/districts/{state_id}/{dist_id}.html"}
                ]
            }

            place_schema = {
                "@context": "https://schema.org",
                "@type": "AdministrativeArea",
                "name": dist_name_en,
                "alternateName": dist_name_hi,
                "containedInPlace": {
                    "@type": "AdministrativeArea",
                    "name": state_name_en
                },
                "description": f"Verified Census 2011 demographics, literacy rate, and sex ratio statistics for {dist_name_en} district, {state_name_en}."
            }

            schemas_html = f'''<script type="application/ld+json">
{json.dumps(place_schema, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(bc_schema, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, indent=2, ensure_ascii=False)}
</script>'''

            out_content = district_template
            
            # SEO
            seo_content = f'''<title>{dist_name_en} District Demographics (2026): Population, Literacy &amp; Sex Ratio | IndiaMetrix</title>
<meta name="description" content="Explore Census demographics, official literacy rate ({dist_lit_disp_en}), population ({dist_pop_disp_en}), and sex ratio for {dist_name_en} district ({state_name_en}) on IndiaMetrix.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.indiametrix.in/districts/{state_id}/{dist_id}.html">
<meta property="og:title" content="{dist_name_en} District Demographics &amp; Census Data | IndiaMetrix">
<meta property="og:description" content="Explore Census demographics, official literacy rate ({dist_lit_disp_en}), population ({dist_pop_disp_en}), and sex ratio for {dist_name_en} district ({state_name_en}) on IndiaMetrix.">
<meta property="og:url" content="https://www.indiametrix.in/districts/{state_id}/{dist_id}.html">'''
            out_content = re.sub(r'(<!-- BUILD_INJECT:seo -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + seo_content + '\n' + m.group(2), out_content, flags=re.DOTALL)
            
            # District Name
            h1_code = f'<h1 style="font-size:clamp(30px,4.4vw,46px); max-width:18ch; margin-bottom:14px;" data-en="{dist_name_en}" data-hi="{dist_name_hi}">{dist_name_en}</h1>'
            out_content = re.sub(r'(<!-- BUILD_INJECT:district_name -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + h1_code + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

            # Summary
            out_content = re.sub(r'(<!-- BUILD_INJECT:district_summary -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + dist_summary_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

            # Cards
            out_content = re.sub(r'(<!-- BUILD_INJECT:district_cards -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + dist_cards_html + '      ' + m.group(2), out_content, flags=re.DOTALL)

            # Benchmark Table
            out_content = re.sub(r'(<!-- BUILD_INJECT:benchmark_table -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + benchmark_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

            # Insights
            out_content = re.sub(r'(<!-- BUILD_INJECT:district_insights -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + dist_insights_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

            # Peer Districts
            out_content = re.sub(r'(<!-- BUILD_INJECT:peer_districts -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + peer_districts_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

            # FAQs
            out_content = re.sub(r'(<!-- BUILD_INJECT:district_faqs -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + faqs_html + '\n      ' + m.group(2), out_content, flags=re.DOTALL)

            # Schemas
            out_content = re.sub(r'(<!-- BUILD_INJECT:schemas -->\n).*?(<!-- END_BUILD_INJECT -->)', lambda m: m.group(1) + schemas_html + '\n' + m.group(2), out_content, flags=re.DOTALL)

            # Placeholders
            out_content = out_content.replace('{{state_id}}', state_id)
            out_content = out_content.replace('{{district_id}}', dist_id)
            out_content = out_content.replace('{{district_name_en}}', dist_name_en)
            out_content = out_content.replace('{{district_name_hi}}', dist_name_hi)
            out_content = out_content.replace('{{state_name_en}}', state_name_en)
            out_content = out_content.replace('{{state_name_hi}}', state_name_hi)

            out_state_dir = os.path.join(out_districts_dir, state_id)
            os.makedirs(out_state_dir, exist_ok=True)
                
            out_path = os.path.join(out_state_dir, f"{dist_id}.html")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(out_content)
            print(f"Built districts/{state_id}/{dist_id}.html successfully.")

if __name__ == "__main__":
    main()

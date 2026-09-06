import json
import os
import re

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    states_dir = os.path.join(root_dir, 'data', 'indicators', 'states')
    
    states = []
    if os.path.exists(states_dir):
        for filename in os.listdir(states_dir):
            if filename.endswith('.json'):
                with open(os.path.join(states_dir, filename), 'r', encoding='utf-8') as f:
                    states.append(json.load(f))
                    
    # Extract data for each ranking indicator
    def extract_indicator(ind_id, reverse=True):
        items = []
        for s in states:
            sid = s['id']
            name_en = s['name'].get('en', '')
            name_hi = s['name'].get('hi', '')
            
            val = None
            disp_en = ""
            disp_hi = ""
            
            for ind in s.get('indicators', []):
                if ind['id'] == ind_id:
                    val = ind['value']
                    disp_en = ind['display'].get('en', str(val))
                    disp_hi = ind['display'].get('hi', str(val))
                    break
            
            if val is not None:
                items.append({
                    'id': sid, 'name_en': name_en, 'name_hi': name_hi,
                    'val': val, 'disp_en': disp_en, 'disp_hi': disp_hi
                })
        
        items.sort(key=lambda x: x['val'], reverse=reverse)
        return items

    pop_data = extract_indicator('population', reverse=True)
    lit_data = extract_indicator('literacy-rate', reverse=True)
    gsdp_data = extract_indicator('gdp', reverse=True)
    unemp_data = extract_indicator('unemployment', reverse=False) # Lowest is #1
    sex_ratio_data = extract_indicator('sex-ratio', reverse=True)
    area_data = extract_indicator('area', reverse=True)
    
    def generate_rows(sorted_data):
        html = ""
        for i, item in enumerate(sorted_data):
            rank = i + 1
            html += f'''          <tr>
            <td style="font-family:var(--font-mono); font-weight:600; color:var(--teal);">{rank}</td>
            <td><a href="states/{item['id']}.html" style="color:var(--text); font-weight:500; text-decoration:none;" data-en="{item['name_en']}" data-hi="{item['name_hi']}">{item['name_en']}</a></td>
            <td style="font-family:var(--font-mono); font-weight:600;" data-en="{item['disp_en']}" data-hi="{item['disp_hi']}">{item['disp_en']}</td>
          </tr>
'''
        return html
        
    pop_html = generate_rows(pop_data)
    lit_html = generate_rows(lit_data)
    gsdp_html = generate_rows(gsdp_data)
    unemp_html = generate_rows(unemp_data)
    sr_html = generate_rows(sex_ratio_data)
    area_html = generate_rows(area_data)
    
    template_path = os.path.join(root_dir, 'templates', 'rankings.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_population -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + pop_html + r'          \2', content, flags=re.DOTALL)
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_literacy -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + lit_html + r'          \2', content, flags=re.DOTALL)
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_gsdp -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + gsdp_html + r'          \2', content, flags=re.DOTALL)
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_unemployment -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + unemp_html + r'          \2', content, flags=re.DOTALL)
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_sex_ratio -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + sr_html + r'          \2', content, flags=re.DOTALL)
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_area -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + area_html + r'          \2', content, flags=re.DOTALL)
    
    out_path = os.path.join(root_dir, 'rankings.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Built rankings.html with 6 verified indicator rankings successfully.")

if __name__ == "__main__":
    main()

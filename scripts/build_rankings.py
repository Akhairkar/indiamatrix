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
                    
    # Extract data for sorting
    pop_data = []
    lit_data = []
    
    for s in states:
        sid = s['id']
        name_en = s['name'].get('en', '')
        name_hi = s['name'].get('hi', '')
        
        pop = 0
        pop_disp_en = ""
        pop_disp_hi = ""
        
        lit = 0
        lit_disp_en = ""
        lit_disp_hi = ""
        
        for ind in s.get('indicators', []):
            if ind['id'] == 'population':
                pop = ind['value']
                pop_disp_en = ind['display'].get('en', str(pop))
                pop_disp_hi = ind['display'].get('hi', str(pop))
            elif ind['id'] == 'literacy-rate':
                lit = ind['value']
                lit_disp_en = ind['display'].get('en', str(lit))
                lit_disp_hi = ind['display'].get('hi', str(lit))
                
        pop_data.append({
            'id': sid, 'name_en': name_en, 'name_hi': name_hi,
            'val': pop, 'disp_en': pop_disp_en, 'disp_hi': pop_disp_hi
        })
        
        lit_data.append({
            'id': sid, 'name_en': name_en, 'name_hi': name_hi,
            'val': lit, 'disp_en': lit_disp_en, 'disp_hi': lit_disp_hi
        })

    # Sort
    pop_data.sort(key=lambda x: x['val'], reverse=True)
    lit_data.sort(key=lambda x: x['val'], reverse=True)
    
    def generate_rows(sorted_data):
        html = ""
        for i, item in enumerate(sorted_data):
            rank = i + 1
            html += f'''          <tr>
            <td class="ranking-rank">{rank}</td>
            <td><a href="states/{item['id']}.html" style="color:var(--text); text-decoration:none;" data-en="{item['name_en']}" data-hi="{item['name_hi']}">{item['name_en']}</a></td>
            <td class="ranking-val" data-en="{item['disp_en']}" data-hi="{item['disp_hi']}">{item['disp_en']}</td>
          </tr>
'''
        return html
        
    pop_html = generate_rows(pop_data)
    lit_html = generate_rows(lit_data)
    
    template_path = os.path.join(root_dir, 'templates', 'rankings.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_population -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + pop_html + r'          \2', content, flags=re.DOTALL)
    content = re.sub(r'(<!-- BUILD_INJECT:rankings_literacy -->\n).*?(<!-- END_BUILD_INJECT -->)', r'\1' + lit_html + r'          \2', content, flags=re.DOTALL)
    
    out_path = os.path.join(root_dir, 'rankings.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Built rankings.html successfully.")

if __name__ == "__main__":
    main()

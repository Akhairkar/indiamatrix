import os
import glob
import re
import json
from bs4 import BeautifulSoup

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

html_files = []
for p in glob.glob(os.path.join(root_dir, '**', '*.html'), recursive=True):
    rel = os.path.relpath(p, root_dir).replace('\\', '/')
    if not rel.startswith('templates/') and not rel.startswith('.git/'):
        html_files.append((rel, p))

html_files.sort()
print(f"Total HTML files analyzed: {len(html_files)}")

results = []

for rel, full_path in html_files:
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    
    # Title
    t_tag = soup.find('title')
    title = t_tag.get_text().strip() if t_tag else ""
    
    # Meta Description
    d_tag = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
    desc = d_tag.get('content', '').strip() if d_tag else ""
    
    # Canonical
    c_tag = soup.find('link', attrs={'rel': 'canonical'})
    canonical = c_tag.get('href', '').strip() if c_tag else ""
    
    # Open Graph
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    og_url = soup.find('meta', attrs={'property': 'og:url'})
    og_type = soup.find('meta', attrs={'property': 'og:type'})
    og_site_name = soup.find('meta', attrs={'property': 'og:site_name'})
    
    # Twitter
    tw_card = soup.find('meta', attrs={'name': 'twitter:card'})
    tw_title = soup.find('meta', attrs={'name': 'twitter:title'})
    tw_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    tw_image = soup.find('meta', attrs={'name': 'twitter:image'})
    
    # Headings
    h1s = [h.get_text().strip() for h in soup.find_all('h1')]
    h2s = [h.get_text().strip() for h in soup.find_all('h2')]
    h3s = [h.get_text().strip() for h in soup.find_all('h3')]
    
    # Heading hierarchy check
    headings_sequence = []
    for h in soup.find_all(re.compile(r'^h[1-6]$')):
        level = int(h.name[1])
        headings_sequence.append(level)
        
    skipped_level = False
    for i in range(len(headings_sequence) - 1):
        if headings_sequence[i+1] > headings_sequence[i] + 1:
            skipped_level = True
            break
            
    # JSON-LD Schemas
    json_lds = []
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(s.string)
            if isinstance(data, list):
                for item in data:
                    json_lds.append(item.get('@type', 'UnknownList'))
            elif isinstance(data, dict):
                json_lds.append(data.get('@type', 'UnknownDict'))
        except Exception as e:
            json_lds.append(f"ERROR: {e}")
            
    # Performance
    scripts_non_deferred = []
    for sc in soup.find_all('script'):
        src = sc.get('src')
        if src and ('defer' not in sc.attrs) and ('async' not in sc.attrs):
            scripts_non_deferred.append(src)
            
    results.append({
        'rel': rel,
        'title': title,
        'title_len': len(title),
        'desc': desc,
        'desc_len': len(desc),
        'canonical': canonical,
        'og_complete': bool(og_title and og_desc and og_image and og_url and og_type and og_site_name),
        'tw_complete': bool(tw_card and tw_title and tw_desc and tw_image),
        'h1_count': len(h1s),
        'skipped_level': skipped_level,
        'json_lds': json_lds,
        'non_deferred_scripts': scripts_non_deferred
    })

# Summary output
title_bad = [r for r in results if r['title_len'] < 50 or r['title_len'] > 65]
desc_bad = [r for r in results if r['desc_len'] < 140 or r['desc_len'] > 165]
og_bad = [r for r in results if not r['og_complete']]
tw_bad = [r for r in results if not r['tw_complete']]
h1_bad = [r for r in results if r['h1_count'] != 1]
heading_jump = [r for r in results if r['skipped_level']]
no_jsonld = [r for r in results if len(r['json_lds']) == 0]
has_blocking_scripts = [r for r in results if len(r['non_deferred_scripts']) > 0]

print("\n===== AUDIT SUMMARY =====")
print(f"Titles not 50-65 chars: {len(title_bad)} / {len(results)}")
print(f"Descriptions not 140-165 chars: {len(desc_bad)} / {len(results)}")
print(f"Incomplete Open Graph: {len(og_bad)} / {len(results)}")
print(f"Incomplete Twitter Cards: {len(tw_bad)} / {len(results)}")
print(f"H1 count != 1: {len(h1_bad)} / {len(results)}")
print(f"Skipped heading levels: {len(heading_jump)} / {len(results)}")
print(f"No JSON-LD: {len(no_jsonld)} / {len(results)}")
print(f"Pages with render-blocking script src: {len(has_blocking_scripts)} / {len(results)}")

if heading_jump:
    print("\n--- Heading jumps found in ---")
    for r in heading_jump[:10]:
        print(f"  {r['rel']}")

if has_blocking_scripts:
    print("\n--- Pages with non-deferred external scripts ---")
    for r in has_blocking_scripts[:10]:
        print(f"  {r['rel']}: {r['non_deferred_scripts']}")

print("\n--- Title length breakdown by category ---")
for cat in ['root', 'states', 'indicators', 'districts', 'stories', 'tools']:
    cat_items = [r for r in results if (r['rel'].startswith(cat + '/') if cat != 'root' else '/' not in r['rel'])]
    if cat_items:
        avg_len = sum(r['title_len'] for r in cat_items) / len(cat_items)
        sample = cat_items[0]
        print(f"  {cat} ({len(cat_items)} pages): sample title ({sample['title_len']} chars): '{sample['title']}'")

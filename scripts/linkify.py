import os
import re
import json

def get_keywords(root_dir):
    states_dir = os.path.join(root_dir, 'data', 'indicators', 'states')
    
    keywords = {
        "GDP": "/explorer.html",
        "Population": "/explorer.html",
        "Literacy Rate": "/explorer.html",
        "Life Expectancy": "/explorer.html",
        "Unemployment Rate": "/explorer.html"
    }
    
    if os.path.exists(states_dir):
        for filename in os.listdir(states_dir):
            if filename.endswith('.json'):
                state_id = filename.replace('.json', '')
                with open(os.path.join(states_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    name_en = data['name'].get('en', '')
                    if name_en:
                        keywords[name_en] = f"/states/{state_id}.html"
    return keywords

def linkify_html(html, keywords):
    # Split into tokens: tags/comments and text
    tokens = re.split(r'(<!--.*?-->|<[^>]*>)', html, flags=re.DOTALL)
    
    # Tags we do NOT want to inject links inside
    ignore_tags = {'a', 'script', 'style', 'button', 'option', 'title', 'h1', 'h2', 'h3', 'nav', 'header', 'footer'}
    current_ignored_tag = None
    
    sorted_kws = sorted(keywords.keys(), key=len, reverse=True)
    used_kws = set()
    
    new_tokens = []
    
    for token in tokens:
        if not token:
            continue
            
        # If it's a tag or comment
        if token.startswith('<'):
            new_tokens.append(token)
            
            if token.startswith('<!--'):
                continue
                
            # Check if it's opening or closing an ignored tag
            match = re.match(r'</?([a-zA-Z0-9\-]+)', token)
            if match:
                tag_name = match.group(1).lower()
                is_closing = token.startswith('</')
                
                if tag_name in ignore_tags:
                    if not is_closing:
                        # Opening tag
                        if current_ignored_tag is None:
                            current_ignored_tag = tag_name
                    else:
                        # Closing tag
                        if current_ignored_tag == tag_name:
                            current_ignored_tag = None
            continue
            
        # It's a text node
        if current_ignored_tag is not None:
            new_tokens.append(token)
            continue
            
        # We can linkify this text node
        text = token
        for kw in sorted_kws:
            if kw in used_kws:
                continue
                
            # Only match if it's a word boundary
            pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
            if pattern.search(text):
                # Replace only the first occurrence in this file
                url = keywords[kw]
                text = pattern.sub(rf'<a href="{url}" class="internal-link" style="color:var(--teal); text-decoration:underline; text-decoration-color:rgba(45, 212, 191, 0.3);">\1</a>', text, count=1)
                used_kws.add(kw)
                
        new_tokens.append(text)
        
    return ''.join(new_tokens)

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    keywords = get_keywords(root_dir)
    print(f"Loaded {len(keywords)} keywords for internal linking.")
    
    target_dirs = [
        os.path.join(root_dir, 'states'),
        os.path.join(root_dir, 'stories')
    ]
    
    processed_count = 0
    
    for d in target_dirs:
        if not os.path.exists(d):
            continue
        for filename in os.listdir(d):
            if filename.endswith('.html'):
                filepath = os.path.join(d, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    html = f.read()
                    
                new_html = linkify_html(html, keywords)
                
                if new_html != html:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_html)
                    processed_count += 1
                    
    print(f"Successfully applied internal links to {processed_count} files.")

if __name__ == "__main__":
    main()

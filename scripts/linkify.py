import os
import re
import json

def get_state_names(root_dir):
    states_dir = os.path.join(root_dir, 'data', 'indicators', 'states')
    states = {}
    if os.path.exists(states_dir):
        for filename in os.listdir(states_dir):
            if filename.endswith('.json'):
                state_id = filename.replace('.json', '')
                with open(os.path.join(states_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    name_en = data.get('name', {}).get('en', '')
                    if name_en:
                        states[name_en] = state_id
    return states

def linkify_file(filepath, root_dir, states):
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    is_in_states = rel_path.startswith('states/')
    is_in_stories = rel_path.startswith('stories/')
    
    current_state_id = None
    if is_in_states:
        current_state_id = os.path.basename(filepath).replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Determine relative prefixes
    if is_in_states or is_in_stories:
        to_root = '../'
        to_states = '' if is_in_states else '../states/'
    else:
        to_root = './'
        to_states = 'states/'

    keywords = {
        "Literacy Rate": f"{to_root}rankings.html#rank-literacy-rate",
        "Unemployment Rate": f"{to_root}rankings.html#rank-unemployment-rate",
        "Sex Ratio": f"{to_root}rankings.html#rank-sex-ratio",
        "Data Explorer": f"{to_root}explorer.html",
        "Compare States": f"{to_root}compare.html"
    }

    # Add other states (exclude current state)
    for state_name, s_id in states.items():
        if s_id != current_state_id:
            keywords[state_name] = f"{to_states}{s_id}.html"

    tokens = re.split(r'(<!--.*?-->|<(?:[^"\'>]|"[^"]*"|\'[^\']*\')*>)', html, flags=re.DOTALL)
    ignore_tags = {'a', 'script', 'style', 'button', 'option', 'title', 'h1', 'h2', 'nav', 'header', 'footer', 'select', 'textarea'}
    current_ignored_tag = None
    a_depth = 0
    
    sorted_kws = sorted(keywords.keys(), key=len, reverse=True)
    used_kws = set()
    new_tokens = []
    
    for token in tokens:
        if not token:
            continue
            
        if token.startswith('<'):
            new_tokens.append(token)
            if token.startswith('<!--'):
                continue
                
            match = re.match(r'</?([a-zA-Z0-9\-]+)', token)
            if match:
                tag_name = match.group(1).lower()
                is_closing = token.startswith('</')
                if tag_name in ignore_tags:
                    if not is_closing:
                        if tag_name == 'a':
                            a_depth += 1
                        elif current_ignored_tag is None:
                            current_ignored_tag = tag_name
                    else:
                        if tag_name == 'a':
                            a_depth = max(0, a_depth - 1)
                        elif current_ignored_tag == tag_name:
                            current_ignored_tag = None
            continue
            
        if current_ignored_tag is not None or a_depth > 0:
            new_tokens.append(token)
            continue
            
        text = token
        for kw in sorted_kws:
            if kw in used_kws:
                continue
                
            pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
            if pattern.search(text):
                url = keywords[kw]
                text = pattern.sub(rf'<a href="{url}" class="im-inline-link" style="color:var(--teal); text-decoration:underline; text-decoration-color:rgba(45, 212, 191, 0.3);">\1</a>', text, count=1)
                used_kws.add(kw)
                
        new_tokens.append(text)
        
    new_html = ''.join(new_tokens)
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    states = get_state_names(root_dir)
    print(f"Loaded {len(states)} state targets for contextual internal linking.")
    
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
                if linkify_file(filepath, root_dir, states):
                    processed_count += 1
                    
    print(f"Successfully applied contextual internal links to {processed_count} files.")

if __name__ == "__main__":
    main()

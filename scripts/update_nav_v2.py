import glob
import re
import os

files = ["index.html", "india.html", "compare.html", "history.html", "world.html", "explorer.html", "templates/rankings.html", "templates/state.html"]
stories = glob.glob("stories/*.html")
files.extend(stories)

def modify_nav(content):
    # Only insert if explorer.html is not already present
    if "explorer.html" in content:
        return content

    # Find world.html line and insert explorer.html after it
    pattern = r'( *<a href="([^"]*)world\.html".*?</a>)'
    
    def rep(m):
        indent_and_line = m.group(1)
        prefix = m.group(2)
        return indent_and_line + f'\n      <a href="{prefix}explorer.html" data-en="Explorer" data-hi="एक्सप्लोरर">Explorer</a>'
        
    return re.sub(pattern, rep, content)

for f in files:
    if not os.path.exists(f):
        continue
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    new_content = modify_nav(content)
    
    if new_content != content:
        with open(f, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Updated {f}")
    else:
        print(f"Skipped {f} (already has it or world.html not found)")

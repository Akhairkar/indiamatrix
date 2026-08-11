import glob
import re

files = ["index.html", "india.html", "compare.html", "history.html", "world.html", "templates/rankings.html", "templates/state.html"]

def modify_nav(content, level):
    pattern = r'( *<a href="([^"]*)compare\.html".*?</a>)'
    
    def rep(m):
        indent_and_line = m.group(1)
        prefix = m.group(2)
        return indent_and_line + f'\n      <a href="{prefix}history.html" data-en="History" data-hi="इतिहास">History</a>\n      <a href="{prefix}world.html" data-en="World" data-hi="विश्व">World</a>'
        
    return re.sub(pattern, rep, content)

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    new_content = modify_nav(content, "root")
    
    with open(f, "w", encoding="utf-8") as file:
        file.write(new_content)
    
    print(f"Updated {f}")

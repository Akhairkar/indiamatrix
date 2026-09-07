import glob
import os
import re

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cleaned_count = 0

for p in sorted(glob.glob(os.path.join(root_dir, '**', '*.html'), recursive=True)):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    def clean_attr(m):
        attr = m.group(1)
        val = m.group(2)
        clean_val = re.sub(r'<[^>]+>', '', val)
        return f'{attr}="{clean_val}"'

    pattern = re.compile(r'(data-(?:en|hi))="([^"]*?<[a-zA-Z][^"]*?)"')
    new_content = pattern.sub(clean_attr, content)

    # Also clean single-quoted attributes if any
    def clean_attr_sq(m):
        attr = m.group(1)
        val = m.group(2)
        clean_val = re.sub(r'<[^>]+>', '', val)
        return f"{attr}='{clean_val}'"

    pattern_sq = re.compile(r"(data-(?:en|hi))='([^']*?<[a-zA-Z][^']*?)'")
    new_content = pattern_sq.sub(clean_attr_sq, new_content)

    if new_content != content:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_content)
        cleaned_count += 1
        print(f"Cleaned attributes in: {os.path.relpath(p, root_dir)}")

print(f"Total files with HTML inside data-en/data-hi cleaned: {cleaned_count}")

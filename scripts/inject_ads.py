import os
import glob

def process_file(filepath, base_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 1. Inject AdSense script before </head>
    adsense_script = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXX" crossorigin="anonymous"></script>'
    if adsense_script not in content and '</head>' in content:
        content = content.replace('</head>', f'  {adsense_script}\n</head>')
        
    # 2. Fix methodology link
    # Determine depth to root
    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    # Prefix for relative links
    prefix = '../' * depth if depth > 0 else ''
    if prefix == '':
        prefix = './'
    if filepath.endswith('index.html') or filepath.endswith('methodology.html'):
        prefix = '' # root files usually can just use filename
        
    meth_link = f'"{prefix}methodology.html"'
    
    # Replace `<a href="#" data-en="Methodology"` or `<a href="../#" data-en="Methodology"`
    import re
    # We look for <a href="..." data-en="Methodology"
    pattern = r'<a href="[^"]*" data-en="Methodology"'
    replacement = f'<a href={meth_link} data-en="Methodology"'
    content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Find all html files
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    
    count = 0
    for f in html_files:
        if process_file(f, base_dir):
            count += 1
            
    print(f"Processed {count} HTML files for AdSense and Methodology links.")

if __name__ == "__main__":
    main()

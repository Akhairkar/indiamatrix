import os
import glob

def fix_footer():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Collect all HTML files
    all_files = glob.glob(os.path.join(root_dir, "*.html"))
    all_files.extend(glob.glob(os.path.join(root_dir, "templates", "*.html")))
    
    for filepath in all_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Replace broken links
        content = content.replace('<a href="../#"', '<a href="../about.html"') # fallback
        # Wait, the footer has:
        # <a href="../#" data-en="Data Sources" data-hi="डेटा स्रोत">Data Sources</a>
        # Let's do a more robust regex or just replace specifically:
        content = content.replace('href="../#"', 'href="../disclaimer.html"') # Just a catch-all if any remain
        
        # Specific replaces:
        content = content.replace('"../#" data-en="Data Sources"', '"../methodology.html" data-en="Data Sources"')
        content = content.replace('"../#" data-en="Contact"', '"../contact.html" data-en="Contact"')
        content = content.replace('"../#" data-en="Privacy Policy"', '"../privacy.html" data-en="Privacy Policy"')
        content = content.replace('"../#" data-en="Terms"', '"../terms.html" data-en="Terms"')
        content = content.replace('"../#" data-en="Disclaimer"', '"../disclaimer.html" data-en="Disclaimer"')
        content = content.replace('"../#" data-en="Corrections"', '"../contact.html" data-en="Corrections"')

        # Same for root files that use href="#"
        content = content.replace('href="#" data-en="Data Sources"', 'href="methodology.html" data-en="Data Sources"')
        content = content.replace('href="#" data-en="Contact"', 'href="contact.html" data-en="Contact"')
        content = content.replace('href="#" data-en="Privacy Policy"', 'href="privacy.html" data-en="Privacy Policy"')
        content = content.replace('href="#" data-en="Terms"', 'href="terms.html" data-en="Terms"')
        content = content.replace('href="#" data-en="Disclaimer"', 'href="disclaimer.html" data-en="Disclaimer"')
        content = content.replace('href="#" data-en="Corrections"', 'href="contact.html" data-en="Corrections"')

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated footer links in {filepath}")

if __name__ == "__main__":
    fix_footer()

import os
import shutil

def create_stubs():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template = os.path.join(root_dir, 'methodology.html')
    
    pages = [
        ('about.html', 'About IndiaMetrix'),
        ('privacy.html', 'Privacy Policy'),
        ('terms.html', 'Terms of Service'),
        ('contact.html', 'Contact Us'),
        ('disclaimer.html', 'Disclaimer')
    ]
    
    with open(template, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for page, title in pages:
        filepath = os.path.join(root_dir, page)
        if not os.path.exists(filepath):
            # very dirty string replacement for a stub
            page_content = content.replace('Data Methodology', title)
            page_content = page_content.replace('Our principles for sourcing, verifying, and presenting data.', 'Information about ' + title)
            
            # replace the article content
            start_article = page_content.find('<div class="story-content">')
            end_article = page_content.find('</article>')
            
            if start_article != -1 and end_article != -1:
                page_content = page_content[:start_article + 27] + f'<p>This is a placeholder page for {title}. Content coming soon.</p></div>' + page_content[end_article:]
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_content)
            print(f"Created {page}")

if __name__ == "__main__":
    create_stubs()

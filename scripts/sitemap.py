import os
import glob
from datetime import datetime

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_url = "https://www.indiametrix.in"
    
    # 1. Collect all static pages at the root
    root_files = glob.glob(os.path.join(root_dir, "*.html"))
    
    # 2. Collect all state pages
    states_files = glob.glob(os.path.join(root_dir, "states", "*.html"))
    
    # 3. Collect all story pages
    stories_files = glob.glob(os.path.join(root_dir, "stories", "*.html"))
    
    # 4. Collect all ranking pages
    rankings_files = glob.glob(os.path.join(root_dir, "rankings", "*.html"))
    
    # 5. Collect all indicator pages
    indicators_files = glob.glob(os.path.join(root_dir, "indicators", "*.html"))
    
    # 6. Collect all district pages (they are in subfolders)
    districts_files = glob.glob(os.path.join(root_dir, "districts", "**", "*.html"), recursive=True)
    
    all_files = root_files + states_files + stories_files + rankings_files + indicators_files + districts_files
    
    # Determine the date for <lastmod>
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Keep track of added URLs to avoid duplicates
    added_urls = set()
    
    for filepath in all_files:
        # Ignore template files or unwanted files if any (though we are only globbing specific directories)
        
        # Calculate the relative URL path
        relative_path = os.path.relpath(filepath, root_dir)
        
        # Convert windows backslashes to forward slashes for URLs
        relative_path = relative_path.replace("\\", "/")
        
        url_loc = f"{base_url}/{relative_path}"
        
        # Optionally, for index.html we can just output the root /
        if relative_path == "index.html":
            url_loc = f"{base_url}/"
            
        if url_loc in added_urls:
            continue
            
        added_urls.add(url_loc)
        
        sitemap_content += "  <url>\n"
        sitemap_content += f"    <loc>{url_loc}</loc>\n"
        sitemap_content += f"    <lastmod>{current_date}</lastmod>\n"
        # Optional: changefreq, priority
        if relative_path == "index.html" or relative_path == "explorer.html":
            sitemap_content += "    <priority>1.0</priority>\n"
            sitemap_content += "    <changefreq>daily</changefreq>\n"
        elif relative_path.startswith("states/"):
            sitemap_content += "    <priority>0.8</priority>\n"
            sitemap_content += "    <changefreq>weekly</changefreq>\n"
        else:
            sitemap_content += "    <priority>0.6</priority>\n"
            
        sitemap_content += "  </url>\n"
        
    sitemap_content += "</urlset>\n"
    
    out_path = os.path.join(root_dir, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
        
    print(f"Successfully generated sitemap.xml with {len(added_urls)} URLs.")

if __name__ == "__main__":
    main()

import os
import glob
from datetime import datetime

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_url = "https://www.indiametrix.in"
    
    # 1. Collect candidate files
    root_files = glob.glob(os.path.join(root_dir, "*.html"))
    states_files = glob.glob(os.path.join(root_dir, "states", "*.html"))
    stories_files = glob.glob(os.path.join(root_dir, "stories", "*.html"))
    rankings_files = glob.glob(os.path.join(root_dir, "rankings", "*.html"))
    indicators_files = glob.glob(os.path.join(root_dir, "indicators", "*.html"))
    districts_files = glob.glob(os.path.join(root_dir, "districts", "**", "*.html"), recursive=True)
    tools_files = glob.glob(os.path.join(root_dir, "tools", "*.html"))
    
    all_candidates = root_files + states_files + stories_files + rankings_files + indicators_files + districts_files + tools_files
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    added_urls = set()
    skipped_noindex = 0
    
    for filepath in sorted(all_candidates):
        # Read file to check Content Value Gate (noindex)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # If page is marked noindex, omit from sitemap
                if 'name="robots" content="noindex' in content or "name='robots' content='noindex" in content:
                    skipped_noindex += 1
                    continue
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
            continue

        relative_path = os.path.relpath(filepath, root_dir).replace("\\", "/")
        
        if relative_path == "index.html":
            url_loc = f"{base_url}/"
        else:
            url_loc = f"{base_url}/{relative_path}"
            
        if url_loc in added_urls:
            continue
            
        added_urls.add(url_loc)
        
        # Priority and frequency logic
        priority = "0.7"
        changefreq = "monthly"
        
        if relative_path in ["index.html", "explorer.html", "india.html", "rankings.html"]:
            priority = "1.0"
            changefreq = "weekly"
        elif relative_path.startswith("states/"):
            priority = "0.9"
            changefreq = "monthly"
        elif relative_path.startswith("tools/"):
            priority = "0.9"
            changefreq = "weekly"
        elif relative_path in ["districts/index.html", "compare.html", "ask.html", "history.html", "world.html"]:
            priority = "0.8"
            changefreq = "weekly"
        elif relative_path.startswith("stories/"):
            priority = "0.8"
            changefreq = "monthly"
        elif relative_path.startswith("districts/"):
            priority = "0.7"
            changefreq = "monthly"
        elif relative_path in ["sources.html", "about.html", "methodology.html"]:
            priority = "0.6"
            changefreq = "monthly"
        else:
            priority = "0.5"
            changefreq = "yearly"

        sitemap_content += "  <url>\n"
        sitemap_content += f"    <loc>{url_loc}</loc>\n"
        sitemap_content += f"    <lastmod>{current_date}</lastmod>\n"
        sitemap_content += f"    <changefreq>{changefreq}</changefreq>\n"
        sitemap_content += f"    <priority>{priority}</priority>\n"
        sitemap_content += "  </url>\n"
        
    sitemap_content += "</urlset>\n"
    
    out_path = os.path.join(root_dir, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
        
    print(f"Successfully generated sitemap.xml with {len(added_urls)} URLs (excluded {skipped_noindex} noindex pages).")

if __name__ == "__main__":
    main()

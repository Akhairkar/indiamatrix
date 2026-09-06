import os
import re
import glob
from urllib.parse import urlparse

def get_all_html_files(root_dir):
    all_files = glob.glob(os.path.join(root_dir, "**", "*.html"), recursive=True)
    html_files = []
    for f in all_files:
        rel = os.path.relpath(f, root_dir).replace("\\", "/")
        if rel.startswith("templates/") or rel.startswith(".git/"):
            continue
        html_files.append(rel)
    return html_files

def is_indexable(filepath, root_dir):
    full_path = os.path.join(root_dir, filepath)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            return 'name="robots" content="noindex' not in content and "name='robots' content='noindex" not in content
    except Exception:
        return True

def extract_internal_links(filepath, root_dir):
    full_path = os.path.join(root_dir, filepath)
    links = set()
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return links

    # Find all hrefs
    raw_links = re.findall(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']*)["\']', content, re.IGNORECASE)
    
    file_dir = os.path.dirname(filepath)
    for raw in raw_links:
        # Strip query and fragments
        parsed = urlparse(raw)
        path = parsed.path
        if not path or raw.startswith("http://") or raw.startswith("https://") or raw.startswith("mailto:") or raw.startswith("#"):
            continue
            
        # Clean relative path
        if path.startswith("/"):
            target_rel = path.lstrip("/")
        else:
            target_rel = os.path.normpath(os.path.join(file_dir, path)).replace("\\", "/")

        if target_rel.endswith(".html") or target_rel == "" or target_rel == "index.html":
            if target_rel == "":
                target_rel = "index.html"
            links.add(target_rel)
            
    return links

def audit_orphans():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_files = get_all_html_files(root_dir)
    print(f"Auditing internal links across {len(html_files)} HTML pages...")

    link_graph = {f: set() for f in html_files}
    inbound_graph = {f: set() for f in html_files}

    for f in html_files:
        targets = extract_internal_links(f, root_dir)
        for t in targets:
            if t in link_graph:
                link_graph[f].add(t)
                inbound_graph[t].add(f)

    # Breadth-first search from index.html
    queue = [("index.html", 0)]
    visited = {"index.html": 0}

    while queue:
        curr, depth = queue.pop(0)
        for nxt in link_graph.get(curr, []):
            if nxt not in visited:
                visited[nxt] = depth + 1
                queue.append((nxt, depth + 1))

    # Identify indexable orphans
    orphans = []
    unreachable = []
    deep_pages = []

    for f in html_files:
        indexable = is_indexable(f, root_dir)
        in_count = len(inbound_graph[f])
        
        if f not in visited:
            if indexable:
                unreachable.append(f)
        else:
            depth = visited[f]
            if depth > 4 and indexable:
                deep_pages.append((f, depth))

        if in_count == 0 and f != "index.html":
            if indexable:
                orphans.append(f)

    print("\n--- Internal Linking Audit Results ---")
    print(f"Total HTML files indexed: {len(html_files)}")
    print(f"Reachable from homepage: {len(visited)}/{len(html_files)}")

    if orphans:
        print(f"\n[FAIL] Found {len(orphans)} indexable orphan pages (0 inbound links):")
        for o in orphans:
            print(f"  - {o}")
    else:
        print("\n[PASS] 0 indexable orphan pages found! All pages have inbound links.")

    if unreachable:
        print(f"\n[FAIL] Found {len(unreachable)} indexable pages unreachable from index.html:")
        for u in unreachable:
            print(f"  - {u}")
    else:
        print("[PASS] All indexable pages are directly reachable from index.html.")

    if deep_pages:
        print(f"\n[WARN] Pages with click depth > 4:")
        for dp, d in deep_pages:
            print(f"  - {dp} (depth: {d})")
    else:
        print("[PASS] All pages are within recommended click depth (<= 4).")

    if orphans or unreachable:
        return 1
    return 0

if __name__ == "__main__":
    exit(audit_orphans())

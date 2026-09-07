import os
import re
import json
from bs4 import BeautifulSoup

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

static_configs = {
    'index.html': {
        'title': 'India Data & State Statistics Intelligence | IndiaMetrix',
        'desc': 'Explore verified Indian data intelligence across 36 states: Census population, GSDP economic output, literacy rates, and interactive comparisons on IndiaMetrix.',
        'canonical': 'https://www.indiametrix.in/',
        'og_type': 'website',
        'subfolder_depth': 0,
        'schemas': [
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "IndiaMetrix",
                "url": "https://www.indiametrix.in/",
                "description": "Open public data intelligence platform for verified Indian state demographics, economy, and statistics.",
                "inLanguage": ["en", "hi"],
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": "https://www.indiametrix.in/explorer.html?q={search_term_string}"
                    },
                    "query-input": "required name=search_term_string"
                }
            },
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "IndiaMetrix",
                "url": "https://www.indiametrix.in",
                "logo": "https://www.indiametrix.in/assets/images/logo.png"
            }
        ]
    },
    'india.html': {
        'title': 'India Key Indicators: GDP, Population & Stats | IndiaMetrix',
        'desc': "Explore India's verified headline indicators: Population (1.46B), GDP ($3.96T), Literacy (74.04%), and Unemployment (3.1%) with official government sources.",
        'canonical': 'https://www.indiametrix.in/india.html',
        'og_type': 'website',
        'subfolder_depth': 0,
    },
    'compare.html': {
        'title': 'Compare Indian States: GDP, Literacy & Pop | IndiaMetrix',
        'desc': 'Compare Indian states head-to-head across verified GSDP economy, Census population, literacy rates, and health indicators. Side-by-side data analysis.',
        'canonical': 'https://www.indiametrix.in/compare.html',
        'og_type': 'website',
        'subfolder_depth': 0,
    },
    'explorer.html': {
        'title': 'India States Data Explorer: Search & Datasets | IndiaMetrix',
        'desc': 'Interactive data explorer for Indian states. Search, filter, and compare population, GSDP, literacy, and health indicators with instant CSV dataset export.',
        'canonical': 'https://www.indiametrix.in/explorer.html',
        'og_type': 'website',
        'subfolder_depth': 0,
    },
    'history.html': {
        'title': 'India Historical Economic & Census Trends | IndiaMetrix',
        'desc': "Track India's multi-decadal transformation from 1951 to 2026 across GDP growth, population trajectory, life expectancy, literacy, and digital connectivity.",
        'canonical': 'https://www.indiametrix.in/history.html',
        'og_type': 'website',
        'subfolder_depth': 0,
    },
    'world.html': {
        'title': 'India vs World: GDP, Population & Economy | IndiaMetrix',
        'desc': 'Compare India against the World, China, and the United States across GDP ($3.96T), population (1.43B), per-capita income, literacy, and health indicators.',
        'canonical': 'https://www.indiametrix.in/world.html',
        'og_type': 'website',
        'subfolder_depth': 0,
    },
    'ask.html': {
        'title': 'Ask IndiaMetrix AI: Instant Indian Data | IndiaMetrix',
        'desc': "Ask questions and get instant verified statistics on India's GDP, population, literacy, unemployment, and state metrics sourced from MoSPI, Census, and RBI.",
        'canonical': 'https://www.indiametrix.in/ask.html',
        'og_type': 'website',
        'subfolder_depth': 0,
    },
    'about.html': {
        'title': 'About IndiaMetrix: Mission, Data Ethics & Team | IndiaMetrix',
        'desc': 'Learn about IndiaMetrix: our mission to democratize Indian public statistics, open data principles, sovereign source standards, and non-partisan governance.',
        'canonical': 'https://www.indiametrix.in/about.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'add_breadcrumb': ('About', 'https://www.indiametrix.in/about.html')
    },
    'sources.html': {
        'title': 'Official Data Sources & Statistical Directory | IndiaMetrix',
        'desc': 'Complete directory of official Indian government ministries, central agencies, and international statistical organizations that power IndiaMetrix.',
        'canonical': 'https://www.indiametrix.in/sources.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'schemas': [
            {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": "Official Data Sources & Statistical Directory",
                "description": "Complete directory of official Indian government ministries, central agencies, and international statistical organizations that power IndiaMetrix.",
                "url": "https://www.indiametrix.in/sources.html"
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
                    {"@type": "ListItem", "position": 2, "name": "Data Sources", "item": "https://www.indiametrix.in/sources.html"}
                ]
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "What primary sources provide data for IndiaMetrix?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "IndiaMetrix exclusively integrates verified datasets from official entities including the Census of India (MHA), MoSPI, Reserve Bank of India, NITI Aayog, and the World Bank."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "How frequently are data sources audited and synchronized?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "All metrics undergo automated 7-phase validation pipeline checks on every build, ensuring zero placeholder data and complete provenance citations."
                        }
                    }
                ]
            }
        ]
    },
    'methodology.html': {
        'title': 'Statistical Methodology & Data Governance | IndiaMetrix',
        'desc': "Discover IndiaMetrix's 7-phase validation pipeline, sovereign data hierarchy, temporal reconciliation, and zero-fabrication statistical standards.",
        'canonical': 'https://www.indiametrix.in/methodology.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'add_breadcrumb': ('Methodology', 'https://www.indiametrix.in/methodology.html')
    },
    'contact.html': {
        'title': 'Contact & Official Data Verification Desk | IndiaMetrix',
        'desc': 'Contact the IndiaMetrix editorial team. Submit data corrections, suggest verified official datasets, or request research citations with a 48h audit review.',
        'canonical': 'https://www.indiametrix.in/contact.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'add_breadcrumb': ('Contact', 'https://www.indiametrix.in/contact.html')
    },
    'privacy.html': {
        'title': 'Privacy Policy & Data Protection Standards | IndiaMetrix',
        'desc': 'IndiaMetrix Privacy Policy: Zero personally identifiable information collection, client-side localStorage disclosures, and Google AdSense cookie compliance.',
        'canonical': 'https://www.indiametrix.in/privacy.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'add_breadcrumb': ('Privacy Policy', 'https://www.indiametrix.in/privacy.html')
    },
    'terms.html': {
        'title': 'Terms of Service & Open Data License | IndiaMetrix',
        'desc': 'Review the IndiaMetrix Terms of Service: Open Data Re-use rights, CC BY 4.0 licensing, acceptable automated access policies, and legal platform disclaimers.',
        'canonical': 'https://www.indiametrix.in/terms.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'add_breadcrumb': ('Terms of Service', 'https://www.indiametrix.in/terms.html')
    },
    'disclaimer.html': {
        'title': 'Legal Disclaimer & Non-Affiliation Disclosure | IndiaMetrix',
        'desc': 'Review the legal disclaimer for IndiaMetrix: an independent public data platform not affiliated with the Government of India. Statistical limitations and terms.',
        'canonical': 'https://www.indiametrix.in/disclaimer.html',
        'og_type': 'website',
        'subfolder_depth': 0,
        'add_breadcrumb': ('Disclaimer', 'https://www.indiametrix.in/disclaimer.html')
    },
    'districts/index.html': {
        'title': 'India Districts Directory: Census Demographics | IndiaMetrix',
        'desc': 'Browse verified Census demographics, literacy rates, and population statistics across Indian districts. Granular sub-district intelligence and rankings.',
        'canonical': 'https://www.indiametrix.in/districts/index.html',
        'og_type': 'website',
        'subfolder_depth': 1,
    },
    'tools/index.html': {
        'title': 'Data Tools, Simulators & State Calculators | IndiaMetrix',
        'desc': 'Explore interactive calculators, economic equivalence models, demographic projectors, and comparison engines for Indian states and indicators on IndiaMetrix.',
        'canonical': 'https://www.indiametrix.in/tools/index.html',
        'og_type': 'website',
        'subfolder_depth': 1,
        'add_breadcrumb': ('Data Tools', 'https://www.indiametrix.in/tools/index.html')
    },
    'tools/demographic-calculator.html': {
        'title': 'Demographic & Universal Literacy Projector | IndiaMetrix',
        'desc': 'Calculate and project universal 100% literacy milestones for Indian states. Analyze state-to-state education gaps and sex ratio demographic balances.',
        'canonical': 'https://www.indiametrix.in/tools/demographic-calculator.html',
        'og_type': 'website',
        'subfolder_depth': 1,
        'add_breadcrumb_sub': ('Data Tools', 'https://www.indiametrix.in/tools/index.html', 'Demographic Calculator', 'https://www.indiametrix.in/tools/demographic-calculator.html')
    },
    'tools/economic-comparator.html': {
        'title': 'State Economic Power & Country Equivalence | IndiaMetrix',
        'desc': 'Calculate and compare Indian state GSDP to sovereign countries worldwide. Explore per capita output, national share, and projected $1 Trillion milestones.',
        'canonical': 'https://www.indiametrix.in/tools/economic-comparator.html',
        'og_type': 'website',
        'subfolder_depth': 1,
        'add_breadcrumb_sub': ('Data Tools', 'https://www.indiametrix.in/tools/index.html', 'Economic Comparator', 'https://www.indiametrix.in/tools/economic-comparator.html')
    },
    'stories/digital.html': {
        'title': 'India Digital Transformation: UPI & Data Boom | IndiaMetrix',
        'desc': "In-depth analysis of India's digital public infrastructure, from the Aadhaar-UPI stack to 850M+ internet users and rural connectivity transitions.",
        'canonical': 'https://www.indiametrix.in/stories/digital.html',
        'og_type': 'article',
        'subfolder_depth': 1,
        'add_breadcrumb_sub': ('Stories', 'https://www.indiametrix.in/#stories', "India's Digital Transformation", 'https://www.indiametrix.in/stories/digital.html')
    },
    'stories/growth.html': {
        'title': 'How Indian States Compare: Economic Growth | IndiaMetrix',
        'desc': 'Explore economic divergence across Indian states: GSDP powerhouses, per capita income variations, manufacturing corridors, and heartland growth engines.',
        'canonical': 'https://www.indiametrix.in/stories/growth.html',
        'og_type': 'article',
        'subfolder_depth': 1,
        'add_breadcrumb_sub': ('Stories', 'https://www.indiametrix.in/#stories', 'State Economic Growth', 'https://www.indiametrix.in/stories/growth.html')
    },
    'stories/literacy.html': {
        'title': "Story of India's Literacy: Education Divide | IndiaMetrix",
        'desc': "Analyze India's literacy transition: Census trends from 18% in 1951 to 80%+, the female literacy surge, urban-rural convergence, and regional human capital.",
        'canonical': 'https://www.indiametrix.in/stories/literacy.html',
        'og_type': 'article',
        'subfolder_depth': 1,
        'add_breadcrumb_sub': ('Stories', 'https://www.indiametrix.in/#stories', "Story of India's Literacy", 'https://www.indiametrix.in/stories/literacy.html')
    },
    'stories/population.html': {
        'title': 'India Population Transition & Demographics | IndiaMetrix',
        'desc': "Analyze India's demographic transition: fertility rate drops, regional youth vs aging cohorts, urban migration, and the 2045 demographic dividend window.",
        'canonical': 'https://www.indiametrix.in/stories/population.html',
        'og_type': 'article',
        'subfolder_depth': 1,
        'add_breadcrumb_sub': ('Stories', 'https://www.indiametrix.in/#stories', "India's Population Transition", 'https://www.indiametrix.in/stories/population.html')
    }
}

for rel_path, cfg in static_configs.items():
    full_path = os.path.join(root_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    depth = cfg['subfolder_depth']
    prefix = '../' * depth

    title = cfg['title']
    desc = cfg['desc']
    canonical = cfg['canonical']
    og_type = cfg['og_type']

    # 1. Favicons
    favicons_html = f'''<link rel="icon" type="image/svg+xml" href="{prefix}assets/images/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/images/apple-touch-icon.png">'''

    # 2. Hreflang
    hreflang_html = f'''<link rel="alternate" hreflang="en-IN" href="{canonical}">
<link rel="alternate" hreflang="hi-IN" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">'''

    # 3. Preconnect
    preconnect_html = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'''

    # 4. Open Graph & Twitter Cards
    social_meta = f'''<meta name="robots" content="index, follow">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="IndiaMetrix">
<meta property="og:locale" content="en_IN">
<meta property="og:locale:alternate" content="hi_IN">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://www.indiametrix.in/assets/images/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@IndiaMetrix">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://www.indiametrix.in/assets/images/og-cover.png">
<meta name="twitter:image:alt" content="{title}">'''

    # Replace Title
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, count=1, flags=re.DOTALL)

    # Replace or add Meta Description
    if re.search(r'<meta\s+name=["\']description["\'][^>]*>', content, re.IGNORECASE):
        content = re.sub(r'<meta\s+name=["\']description["\'][^>]*>', f'<meta name="description" content="{desc}">', content, count=1, flags=re.IGNORECASE)
    else:
        content = content.replace(f'<title>{title}</title>', f'<title>{title}</title>\n<meta name="description" content="{desc}">')

    # Replace or add Canonical
    if re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', content, re.IGNORECASE):
        content = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>', f'<link rel="canonical" href="{canonical}">', content, count=1, flags=re.IGNORECASE)
    else:
        content = content.replace(f'<meta name="description" content="{desc}">', f'<meta name="description" content="{desc}">\n<link rel="canonical" href="{canonical}">')

    # Clean existing og: and twitter: meta tags from <head> to avoid duplication
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if head_match:
        head_inner = head_match.group(1)
        
        # Remove old og: tags
        head_inner = re.sub(r'\s*<meta\s+property=["\']og:[^"\']+["\'][^>]*>', '', head_inner)
        # Remove old twitter: tags
        head_inner = re.sub(r'\s*<meta\s+name=["\']twitter:[^"\']+["\'][^>]*>', '', head_inner)
        # Remove old robots tag
        head_inner = re.sub(r'\s*<meta\s+name=["\']robots["\'][^>]*>', '', head_inner)
        # Remove old hreflang tags
        head_inner = re.sub(r'\s*<link\s+rel=["\']alternate["\'][^>]*hreflang=[^>]*>', '', head_inner)
        # Remove old favicon/icon tags
        head_inner = re.sub(r'\s*<link\s+rel=["\'](?:icon|apple-touch-icon)["\'][^>]*>', '', head_inner)

        # Place the new unified social, favicons, hreflang right after canonical
        canonical_tag = f'<link rel="canonical" href="{canonical}">'
        replacement_block = f'''{canonical_tag}

{social_meta}

{favicons_html}

{hreflang_html}'''
        head_inner = head_inner.replace(canonical_tag, replacement_block, 1)

        # Ensure preconnect is present
        if 'https://fonts.gstatic.com' not in head_inner:
            head_inner = head_inner.replace('<meta name="theme-color"', f'{preconnect_html}\n<meta name="theme-color"')

        # Check schemas
        if 'schemas' in cfg:
            # Remove existing ld+json if rewriting schemas completely
            head_inner = re.sub(r'\s*<script\s+type=["\']application/ld\+json["\']>.*?</script>', '', head_inner, flags=re.DOTALL)
            schema_scripts = "\n".join([f'<script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n</script>' for s in cfg['schemas']])
            head_inner += f"\n{schema_scripts}\n"
        elif 'add_breadcrumb' in cfg:
            b_name, b_url = cfg['add_breadcrumb']
            bc_schema = {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
                    {"@type": "ListItem", "position": 2, "name": b_name, "item": b_url}
                ]
            }
            if 'BreadcrumbList' not in head_inner:
                head_inner += f'\n<script type="application/ld+json">\n{json.dumps(bc_schema, indent=2, ensure_ascii=False)}\n</script>\n'
        elif 'add_breadcrumb_sub' in cfg:
            p_name, p_url, c_name, c_url = cfg['add_breadcrumb_sub']
            bc_schema = {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
                    {"@type": "ListItem", "position": 2, "name": p_name, "item": p_url},
                    {"@type": "ListItem", "position": 3, "name": c_name, "item": c_url}
                ]
            }
            if 'BreadcrumbList' not in head_inner:
                head_inner += f'\n<script type="application/ld+json">\n{json.dumps(bc_schema, indent=2, ensure_ascii=False)}\n</script>\n'

        content = content[:head_match.start(1)] + head_inner + content[head_match.end(1):]

    # Add defer to non-async external script tags across the entire file
    def defer_repl(match):
        tag = match.group(0)
        if 'async' in tag or 'defer' in tag:
            return tag
        return tag.replace('<script ', '<script defer ')

    content = re.sub(r'<script\s+(?![^>]*\b(?:async|defer)\b)[^>]*src=["\'][^"\']+["\'][^>]*>', defer_repl, content)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully upgraded SEO for {rel_path}")

print("\nAll 22 static pages upgraded successfully!")

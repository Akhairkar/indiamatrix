import os
import re
import json

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Update robots.txt
robots_txt = """User-agent: *
Allow: /

# Host
Host: https://www.indiametrix.in

# Sitemaps
Sitemap: https://www.indiametrix.in/sitemap.xml
"""
with open(os.path.join(root_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_txt)
print("Updated robots.txt")

# 2. Update templates/state.html
state_tmpl_path = os.path.join(root_dir, 'templates', 'state.html')
with open(state_tmpl_path, 'r', encoding='utf-8') as f:
    state_tmpl = f.read()

# Replace <head> area in state.html
head_search = re.compile(r'<head>.*?</head>', re.DOTALL)
new_state_head = """<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- BUILD_INJECT:seo -->
<title>State Overview | IndiaMetrix</title>
<meta name="description" content="State headline indicators.">
<link rel="canonical" href="https://www.indiametrix.in/">
<!-- END_BUILD_INJECT -->
<meta name="theme-color" content="#0D1424">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="../assets/css/style.css">
</head>"""
state_tmpl = head_search.sub(new_state_head, state_tmpl, count=1)
state_tmpl = state_tmpl.replace('<script src="../assets/js/main.js"></script>', '<script defer src="../assets/js/main.js"></script>')
with open(state_tmpl_path, 'w', encoding='utf-8') as f:
    f.write(state_tmpl)
print("Updated templates/state.html")

# 3. Update templates/district.html
district_tmpl_path = os.path.join(root_dir, 'templates', 'district.html')
with open(district_tmpl_path, 'r', encoding='utf-8') as f:
    district_tmpl = f.read()

new_district_head = """<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- BUILD_INJECT:seo -->
<title>{{district_name_en}} District Data | IndiaMetrix</title>
<meta name="description" content="Explore population and statistics for {{district_name_en}} district.">
<link rel="canonical" href="https://www.indiametrix.in/districts/{{state_id}}/{{district_id}}.html">
<!-- END_BUILD_INJECT -->
<meta name="theme-color" content="#0D1424">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="../../assets/css/style.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXX" crossorigin="anonymous"></script>
</head>"""
district_tmpl = head_search.sub(new_district_head, district_tmpl, count=1)
district_tmpl = district_tmpl.replace('<script src="../../assets/js/main.js"></script>', '<script defer src="../../assets/js/main.js"></script>')
with open(district_tmpl_path, 'w', encoding='utf-8') as f:
    f.write(district_tmpl)
print("Updated templates/district.html")

# 4. Update templates/indicator.html
ind_tmpl_path = os.path.join(root_dir, 'templates', 'indicator.html')
with open(ind_tmpl_path, 'r', encoding='utf-8') as f:
    ind_tmpl = f.read()

new_ind_head = """<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- BUILD_INJECT:seo -->
<title>{{seo_title}}</title>
<meta name="description" content="{{seo_desc}}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.indiametrix.in/indicators/{{id}}.html">

<meta property="og:type" content="website">
<meta property="og:site_name" content="IndiaMetrix">
<meta property="og:locale" content="en_IN">
<meta property="og:locale:alternate" content="hi_IN">
<meta property="og:title" content="{{seo_title}}">
<meta property="og:description" content="{{seo_desc}}">
<meta property="og:url" content="https://www.indiametrix.in/indicators/{{id}}.html">
<meta property="og:image" content="https://www.indiametrix.in/assets/images/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{{seo_title}}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@IndiaMetrix">
<meta name="twitter:title" content="{{seo_title}}">
<meta name="twitter:description" content="{{seo_desc}}">
<meta name="twitter:image" content="https://www.indiametrix.in/assets/images/og-cover.png">
<meta name="twitter:image:alt" content="{{seo_title}}">

<link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/images/apple-touch-icon.png">

<link rel="alternate" hreflang="en-IN" href="https://www.indiametrix.in/indicators/{{id}}.html">
<link rel="alternate" hreflang="hi-IN" href="https://www.indiametrix.in/indicators/{{id}}.html">
<link rel="alternate" hreflang="x-default" href="https://www.indiametrix.in/indicators/{{id}}.html">
<!-- END_BUILD_INJECT -->
<meta name="theme-color" content="#0D1424">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="../assets/css/style.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXX" crossorigin="anonymous"></script>

<!-- BUILD_INJECT:indicator_schemas -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "{{name_en}} across Indian States & Union Territories",
  "description": "{{seo_desc}}",
  "url": "https://www.indiametrix.in/indicators/{{id}}.html",
  "creator": {
    "@type": "Organization",
    "name": "{{source_name}}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "IndiaMetrix",
    "url": "https://www.indiametrix.in"
  },
  "temporalCoverage": "1951/2026",
  "spatialCoverage": {
    "@type": "Place",
    "name": "India"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
    {"@type": "ListItem", "position": 2, "name": "Indicators", "item": "https://www.indiametrix.in/explorer.html"},
    {"@type": "ListItem", "position": 3, "name": "{{name_en}}", "item": "https://www.indiametrix.in/indicators/{{id}}.html"}
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the national benchmark for {{name_en}} in India?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{name_en}} in India stands at {{disp_en}} (reference year {{year}}), verified through official {{source_name}} publications."
      }
    },
    {
      "@type": "Question",
      "name": "Where can I explore state-by-state comparisons for {{name_en}}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "IndiaMetrix provides a complete 36-state verified leaderboard and decadal trend visualization for {{name_en}} on this dashboard."
      }
    }
  ]
}
</script>
<!-- END_BUILD_INJECT -->
</head>"""

ind_tmpl = head_search.sub(new_ind_head, ind_tmpl, count=1)
ind_tmpl = ind_tmpl.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', '<script defer src="https://cdn.jsdelivr.net/npm/chart.js"></script>')
ind_tmpl = ind_tmpl.replace('<script src="../assets/js/main.js"></script>', '<script defer src="../assets/js/main.js"></script>')
ind_tmpl = ind_tmpl.replace('<script src="../assets/js/indicator-page.js"></script>', '<script defer src="../assets/js/indicator-page.js"></script>')

with open(ind_tmpl_path, 'w', encoding='utf-8') as f:
    f.write(ind_tmpl)
print("Updated templates/indicator.html")

# 5. Update templates/rankings.html
rank_tmpl_path = os.path.join(root_dir, 'templates', 'rankings.html')
with open(rank_tmpl_path, 'r', encoding='utf-8') as f:
    rank_tmpl = f.read()

new_rank_head = """<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Indian State Rankings: GDP, Literacy & Pop | IndiaMetrix</title>
<meta name="description" content="Compare official rankings of all 36 Indian states and Union Territories across GSDP economy, Census population, literacy rates, and unemployment benchmarks.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.indiametrix.in/rankings.html">

<meta property="og:type" content="website">
<meta property="og:site_name" content="IndiaMetrix">
<meta property="og:locale" content="en_IN">
<meta property="og:locale:alternate" content="hi_IN">
<meta property="og:title" content="Indian State Rankings: GDP, Literacy & Pop | IndiaMetrix">
<meta property="og:description" content="Compare official rankings of all 36 Indian states and Union Territories across GSDP economy, Census population, literacy rates, and unemployment benchmarks.">
<meta property="og:url" content="https://www.indiametrix.in/rankings.html">
<meta property="og:image" content="https://www.indiametrix.in/assets/images/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Indian State Rankings - IndiaMetrix">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@IndiaMetrix">
<meta name="twitter:title" content="Indian State Rankings: GDP, Literacy & Pop | IndiaMetrix">
<meta name="twitter:description" content="Compare official rankings of all 36 Indian states and Union Territories across GSDP economy, Census population, literacy rates, and unemployment benchmarks.">
<meta name="twitter:image" content="https://www.indiametrix.in/assets/images/og-cover.png">
<meta name="twitter:image:alt" content="Indian State Rankings - IndiaMetrix">

<link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/images/apple-touch-icon.png">

<link rel="alternate" hreflang="en-IN" href="https://www.indiametrix.in/rankings.html">
<link rel="alternate" hreflang="hi-IN" href="https://www.indiametrix.in/rankings.html">
<link rel="alternate" hreflang="x-default" href="https://www.indiametrix.in/rankings.html">
<meta name="theme-color" content="#0D1424">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Indian State & UT Socio-Economic Rankings (2026)",
  "description": "Verified rankings of all 36 Indian states and Union Territories across GSDP, population, literacy, unemployment, and sex ratio.",
  "url": "https://www.indiametrix.in/rankings.html"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.indiametrix.in/"},
    {"@type": "ListItem", "position": 2, "name": "Rankings", "item": "https://www.indiametrix.in/rankings.html"}
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Which Indian state has the highest Gross State Domestic Product (GSDP)?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Maharashtra ranks #1 among Indian states with a GSDP of ₹38.79 Lakh Crore, followed by Tamil Nadu, Gujarat, and Karnataka."
      }
    },
    {
      "@type": "Question",
      "name": "Which state has the highest literacy rate in India?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Kerala ranks #1 in India with a 94.00% literacy rate according to Census records, followed by Lakshadweep (91.85%) and Mizoram (91.33%)."
      }
    }
  ]
}
</script>"""

rank_tmpl = head_search.sub(new_rank_head, rank_tmpl, count=1)
rank_tmpl = rank_tmpl.replace('<script src="assets/js/main.js"></script>', '<script defer src="assets/js/main.js"></script>')
with open(rank_tmpl_path, 'w', encoding='utf-8') as f:
    f.write(rank_tmpl)
print("Updated templates/rankings.html")

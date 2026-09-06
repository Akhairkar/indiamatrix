import re
import os
import json

def get_svg_map():
    # Coordinated simplified polygonal SVG map of India on 600x700 viewBox
    states_coords = {
        "ladakh": "M 210,35 L 285,45 L 320,85 L 290,115 L 245,100 L 225,65 Z",
        "jammu-kashmir": "M 165,75 L 225,65 L 245,100 L 210,125 L 165,110 Z",
        "himachal-pradesh": "M 210,125 L 255,105 L 280,135 L 245,160 L 205,145 Z",
        "punjab": "M 170,125 L 205,145 L 215,180 L 165,175 Z",
        "chandigarh": "M 215,165 L 225,165 L 225,175 L 215,175 Z",
        "uttarakhand": "M 245,160 L 280,135 L 315,170 L 275,195 Z",
        "haryana": "M 205,170 L 240,170 L 245,215 L 195,205 Z",
        "delhi": "M 235,195 L 250,195 L 250,210 L 235,210 Z",
        "rajasthan": "M 115,185 L 195,205 L 225,250 L 180,305 L 110,265 Z",
        "uttar-pradesh": "M 245,200 L 325,185 L 380,245 L 315,285 L 240,245 Z",
        "bihar": "M 375,235 L 435,235 L 445,275 L 380,285 Z",
        "west-bengal": "M 425,275 L 455,275 L 475,340 L 440,375 L 420,335 Z",
        "jharkhand": "M 370,285 L 430,285 L 425,340 L 375,340 Z",
        "odisha": "M 360,340 L 425,340 L 435,400 L 385,445 L 345,410 Z",
        "chhattisgarh": "M 315,315 L 365,315 L 350,420 L 315,400 Z",
        "madhya-pradesh": "M 205,255 L 315,255 L 325,335 L 230,345 L 195,305 Z",
        "gujarat": "M 75,265 L 145,265 L 175,325 L 135,365 L 75,325 Z",
        "maharashtra": "M 155,335 L 255,335 L 285,415 L 205,455 L 155,405 Z",
        "goa": "M 175,475 L 190,475 L 190,495 L 175,495 Z",
        "karnataka": "M 180,445 L 235,435 L 245,545 L 195,545 Z",
        "telangana": "M 245,395 L 315,385 L 305,465 L 245,445 Z",
        "andhra-pradesh": "M 245,465 L 340,435 L 350,515 L 265,555 Z",
        "kerala": "M 195,545 L 225,545 L 220,645 L 190,625 Z",
        "tamil-nadu": "M 225,545 L 275,545 L 270,645 L 220,645 Z",
        "puducherry": "M 275,575 L 285,575 L 285,585 L 275,585 Z",
        "sikkim": "M 425,195 L 445,195 L 445,225 L 425,225 Z",
        "assam": "M 465,225 L 545,225 L 535,265 L 465,265 Z",
        "arunachal-pradesh": "M 505,165 L 590,165 L 575,220 L 515,210 Z",
        "nagaland": "M 550,230 L 585,230 L 580,265 L 545,265 Z",
        "manipur": "M 545,270 L 580,270 L 575,310 L 540,310 Z",
        "mizoram": "M 525,315 L 555,315 L 550,365 L 520,355 Z",
        "tripura": "M 495,305 L 520,305 L 520,345 L 495,335 Z",
        "meghalaya": "M 470,255 L 515,255 L 515,280 L 470,280 Z",
        "dadra-nagar-haveli-daman-diu": "M 135,365 L 148,365 L 148,378 L 135,378 Z",
        "lakshadweep": "M 135,590 L 155,590 L 155,620 L 135,620 Z",
        "andaman-nicobar": "M 515,520 L 535,520 L 535,620 L 515,620 Z"
    }
    
    svg = '<svg viewBox="0 0 620 680" class="india-vector-map" aria-label="Interactive Map of Indian States" role="img">\n'
    svg += '  <defs>\n'
    svg += '    <filter id="glow-teal" x="-20%" y="-20%" width="140%" height="140%">\n'
    svg += '      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#2BB7A0" flood-opacity="0.6"/>\n'
    svg += '    </filter>\n'
    svg += '  </defs>\n'
    svg += '  <g class="map-subcontinent" stroke="rgba(232,236,248,0.18)" stroke-width="1.2">\n'
    
    for sid, d in states_coords.items():
        name = sid.replace("-", " ").title()
        svg += f'    <path d="{d}" data-state-id="{sid}" id="map-path-{sid}"><title>{name} - Click for profile</title></path>\n'
        
    svg += '  </g>\n'
    svg += '</svg>\n'
    return svg

def build():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(root, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update Hero Visual
    new_hero_visual = """      <div class="hero-visual">
        <a href="indicators/gdp-current-usd.html" class="orbit-card orbit-card--1" title="India GDP Deep Dive">
          <span class="orbit-label">National GDP</span>
          <span class="orbit-value">$3.96T</span>
        </a>
        <a href="indicators/literacy-rate.html" class="orbit-card orbit-card--2" title="India Literacy Deep Dive">
          <span class="orbit-label">Literacy Rate</span>
          <span class="orbit-value">74.04%</span>
        </a>
        <a href="rankings.html" class="orbit-card orbit-card--3" title="State Rankings">
          <span class="orbit-label">States &amp; UTs</span>
          <span class="orbit-value">36 Leaderboards</span>
        </a>
        <a href="states/maharashtra.html" class="orbit-card orbit-card--4" title="#1 Economy: Maharashtra">
          <span class="orbit-label">#1 GSDP (MH)</span>
          <span class="orbit-value">₹38.8L Cr</span>
        </a>
        
        <!-- Animated India Geodesic Matrix Core -->
        <div class="india-dotmark" style="display:flex; align-items:center; justify-content:center; flex-direction:column; text-align:center;">
          <svg viewBox="0 0 200 200" style="width: 140px; height: 140px; filter: drop-shadow(0 0 12px var(--teal));" aria-hidden="true">
            <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(43,183,160,0.2)" stroke-width="2" stroke-dasharray="4 6"/>
            <circle cx="100" cy="100" r="70" fill="none" stroke="rgba(242,169,59,0.3)" stroke-width="1.5"/>
            <circle cx="100" cy="100" r="48" fill="rgba(16,24,43,0.85)" stroke="var(--teal)" stroke-width="2"/>
            <text x="100" y="96" text-anchor="middle" fill="var(--text)" font-family="var(--font-mono)" font-size="12" font-weight="700">INDIA</text>
            <text x="100" y="112" text-anchor="middle" fill="var(--teal)" font-family="var(--font-mono)" font-size="10">METRIX</text>
            <circle cx="70" cy="80" r="4" fill="var(--saffron)"/>
            <circle cx="130" cy="85" r="4" fill="var(--teal)"/>
            <circle cx="95" cy="130" r="4" fill="var(--saffron)"/>
            <circle cx="115" cy="65" r="3" fill="#2ecc71"/>
          </svg>
          <span style="font-family: var(--font-mono); font-size: 11px; color: var(--teal); margin-top: 6px; letter-spacing: 0.08em; text-transform: uppercase;">Verified Data Matrix</span>
        </div>
      </div>"""
    html = re.sub(r'<div class="hero-visual" aria-hidden="true">.*?</div>\s*</div>\s*</section>', new_hero_visual + '\n    </div>\n  </section>', html, flags=re.DOTALL)

    # 2. Update India at a Glance
    new_glance = """  <!-- INDIA AT A GLANCE -->
  <section class="section glance" id="glance">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow" data-en="Live Snapshot" data-hi="लाइव स्नैपशॉट">Live Snapshot</p>
        <h2 data-en="India at a Glance" data-hi="भारत एक नज़र में">India at a Glance</h2>
        <p class="section-sub" data-en="Headline indicators, connected to verified official sources across all 36 States & UTs." data-hi="मुख्य संकेतक — सभी 36 राज्यों और केंद्र शासित प्रदेशों में सत्यापित आधिकारिक स्रोतों से जुड़े हुए।">Headline indicators, connected to verified official sources across all 36 States & UTs.</p>
        <a class="btn btn-outline" href="india.html" style="margin-top:18px;" data-en="View Full India Overview →" data-hi="पूरा भारत अवलोकन देखें →">View Full India Overview →</a>
      </header>

      <div class="glance-grid">
        <a href="indicators/population.html" class="glance-card">
          <div>
            <span class="glance-icon" aria-hidden="true">👥</span>
            <h3 data-en="Population" data-hi="जनसंख्या">Population</h3>
            <p class="glance-value" style="font-family:var(--font-mono); font-weight:700; font-size:22px; color:var(--text);" data-en="1.46 billion" data-hi="1.46 अरब">1.46 billion</p>
            <p style="font-size:11px; color:var(--text-faint); margin-bottom:12px;">2025 Est. • World Bank</p>
          </div>
          <span style="font-size:12px; color:var(--teal); font-family:var(--font-mono); font-weight:600;">Deep Dive &amp; State Breakdown →</span>
        </a>
        <a href="indicators/gdp-current-usd.html" class="glance-card">
          <div>
            <span class="glance-icon" aria-hidden="true">📈</span>
            <h3 data-en="GDP" data-hi="जीडीपी">GDP</h3>
            <p class="glance-value" style="font-family:var(--font-mono); font-weight:700; font-size:22px; color:var(--text);" data-en="$3.96 trillion" data-hi="$3.96 ट्रिलियन">$3.96 trillion</p>
            <p style="font-size:11px; color:var(--text-faint); margin-bottom:12px;">2025 • World Bank</p>
          </div>
          <span style="font-size:12px; color:var(--teal); font-family:var(--font-mono); font-weight:600;">Deep Dive &amp; State Breakdown →</span>
        </a>
        <a href="indicators/literacy-rate.html" class="glance-card">
          <div>
            <span class="glance-icon" aria-hidden="true">📖</span>
            <h3 data-en="Literacy" data-hi="साक्षरता">Literacy</h3>
            <p class="glance-value" style="font-family:var(--font-mono); font-weight:700; font-size:22px; color:var(--text);" data-en="74.04%" data-hi="74.04%">74.04%</p>
            <p style="font-size:11px; color:var(--text-faint); margin-bottom:12px;">2011 • Census of India</p>
          </div>
          <span style="font-size:12px; color:var(--teal); font-family:var(--font-mono); font-weight:600;">Deep Dive &amp; State Breakdown →</span>
        </a>
        <a href="indicators/unemployment-rate.html" class="glance-card">
          <div>
            <span class="glance-icon" aria-hidden="true">💼</span>
            <h3 data-en="Unemployment" data-hi="बेरोज़गारी">Unemployment</h3>
            <p class="glance-value" style="font-family:var(--font-mono); font-weight:700; font-size:22px; color:var(--text);" data-en="3.1%" data-hi="3.1%">3.1%</p>
            <p style="font-size:11px; color:var(--text-faint); margin-bottom:12px;">2025 • MoSPI PLFS</p>
          </div>
          <span style="font-size:12px; color:var(--teal); font-family:var(--font-mono); font-weight:600;">Deep Dive &amp; State Breakdown →</span>
        </a>
        <a href="indicators/life-expectancy.html" class="glance-card">
          <div>
            <span class="glance-icon" aria-hidden="true">❤️</span>
            <h3 data-en="Life Expectancy" data-hi="जीवन प्रत्याशा">Life Expectancy</h3>
            <p class="glance-value" style="font-family:var(--font-mono); font-weight:700; font-size:22px; color:var(--text);" data-en="72.0 years" data-hi="72.0 वर्ष">72.0 years</p>
            <p style="font-size:11px; color:var(--text-faint); margin-bottom:12px;">2023 • World Bank</p>
          </div>
          <span style="font-size:12px; color:var(--teal); font-family:var(--font-mono); font-weight:600;">Deep Dive &amp; State Breakdown →</span>
        </a>
        <a href="indicators/internet-users.html" class="glance-card">
          <div>
            <span class="glance-icon" aria-hidden="true">🌐</span>
            <h3 data-en="Internet Users" data-hi="इंटरनेट उपयोगकर्ता">Internet Users</h3>
            <p class="glance-value" style="font-family:var(--font-mono); font-weight:700; font-size:22px; color:var(--text);" data-en="55.9%" data-hi="55.9%">55.9%</p>
            <p style="font-size:11px; color:var(--text-faint); margin-bottom:12px;">2022 • World Bank / ITU</p>
          </div>
          <span style="font-size:12px; color:var(--teal); font-family:var(--font-mono); font-weight:600;">Deep Dive &amp; State Breakdown →</span>
        </a>
      </div>
    </div>
  </section>"""
    html = re.sub(r'<!-- INDIA AT A GLANCE -->.*?<!-- EXPLORE INDIA -->', new_glance + '\n\n  <!-- EXPLORE INDIA -->', html, flags=re.DOTALL)

    # 3. Update Explore India with SVG Map
    svg_map = get_svg_map()
    new_explore = f"""  <!-- EXPLORE INDIA -->
  <section class="section explore" id="explore">
    <div class="wrap explore-grid">
      <div class="explore-copy">
        <p class="eyebrow" data-en="Geospatial Intelligence" data-hi="भू-स्थानिक बुद्धिमत्ता">Geospatial Intelligence</p>
        <h2 data-en="Interactive India Data Map" data-hi="इंटरएक्टिव भारत डेटा मैप">Interactive India Data Map</h2>
        <p class="section-sub" data-en="Explore all 36 States & UTs. Hover over any state on the map to inspect GSDP, literacy, and demographic metrics in real time." data-hi="सभी 36 राज्यों और केंद्र शासित प्रदेशों को एक्सप्लोर करें। वास्तविक समय में जीएसडीपी, साक्षरता और जनसांख्यिकी मेट्रिक्स देखने के लिए मैप पर किसी भी राज्य पर होवर करें।">Explore all 36 States & UTs. Hover over any state on the map to inspect GSDP, literacy, and demographic metrics in real time.</p>

        <ol class="explore-levels">
          <li><a href="india.html" class="level-tag" style="text-decoration:none; display:inline-block;">India Overview</a><span data-en="National benchmarks and macroeconomic indicators." data-hi="राष्ट्रीय मानक और व्यापक आर्थिक संकेतक।">National benchmarks and macroeconomic indicators.</span></li>
          <li><a href="rankings.html" class="level-tag" style="text-decoration:none; display:inline-block;" data-en="States & UTs" data-hi="राज्य व केंद्र शासित प्रदेश">States &amp; UTs</a><span data-en="36 state profiles with verified economic and demographic data." data-hi="सत्यापित आर्थिक और जनसांख्यिकी डेटा के साथ 36 राज्य प्रोफ़ाइल।">36 state profiles with verified economic and demographic data.</span></li>
          <li><a href="districts/index.html" class="level-tag" style="text-decoration:none; display:inline-block;" data-en="Districts" data-hi="ज़िले">Districts</a><span data-en="District discovery hub and verified urban/rural profiles." data-hi="ज़िला खोज हब और सत्यापित शहरी/ग्रामीण प्रोफ़ाइल।">District discovery hub and verified urban/rural profiles.</span></li>
          <li><a href="explorer.html" class="level-tag" style="text-decoration:none; display:inline-block;" data-en="Indicators" data-hi="संकेतक">Indicators</a><span data-en="Cross-state dataset visualizer and CSV export." data-hi="क्रॉस-स्टेट डेटासेट विज़ुअलाइज़र और सीएसवी निर्यात।">Cross-state dataset visualizer and CSV export.</span></li>
        </ol>

        <!-- Quick 36-States Grid -->
        <div style="margin-top: 24px;">
          <p style="font-size: 13px; font-weight: 600; color: var(--text-muted); margin-bottom: 8px;">Direct 1-Click State Profiles:</p>
          <div class="home-states-quickgrid" id="home-states-quickgrid">
            <!-- Injected by home.js -->
          </div>
        </div>
      </div>

      <div class="explore-visual">
        <div class="home-map-panel">
          <div class="home-map-toolbar">
            <span style="font-family:var(--font-mono); font-size:12px; color:var(--text-faint); text-transform:uppercase; font-weight:600;">Choropleth Layer:</span>
            <div class="home-map-metric-group">
              <button type="button" class="map-metric-btn is-active" data-map-metric="gdp">⚡ GSDP</button>
              <button type="button" class="map-metric-btn" data-map-metric="lit">🎓 Literacy</button>
              <button type="button" class="map-metric-btn" data-map-metric="pop">👥 Population</button>
            </div>
          </div>

          <div class="home-map-svg-wrap" id="home-map-container">
            {svg_map}
          </div>

          <!-- Dynamic Floating State HUD -->
          <div class="home-map-hud" id="home-map-hud">
            <!-- Populated on hover by home.js -->
          </div>
        </div>
      </div>
    </div>
  </section>"""
    html = re.sub(r'<!-- EXPLORE INDIA -->.*?<!-- CATEGORIES -->', new_explore + '\n\n  <!-- CATEGORIES -->', html, flags=re.DOTALL)

    # 4. Update Categories with Static 18 Clickable Cards
    categories = [
        {"icon": "📊", "en": "Economy", "hi": "अर्थव्यवस्था", "enDesc": "GDP, growth, trade and inflation.", "hiDesc": "जीडीपी, विकास, व्यापार और महंगाई।", "url": "indicators/gdp-current-usd.html"},
        {"icon": "👥", "en": "Population", "hi": "जनसंख्या", "enDesc": "Census, density and demographics.", "hiDesc": "जनगणना, घनत्व और जनसांख्यिकी।", "url": "indicators/population.html"},
        {"icon": "🎓", "en": "Education", "hi": "शिक्षा", "enDesc": "Literacy, enrolment and outcomes.", "hiDesc": "साक्षरता, नामांकन और परिणाम।", "url": "indicators/literacy-rate.html"},
        {"icon": "🏥", "en": "Healthcare", "hi": "स्वास्थ्य", "enDesc": "Life expectancy, access and outcomes.", "hiDesc": "जीवन प्रत्याशा, पहुंच और परिणाम।", "url": "indicators/life-expectancy.html"},
        {"icon": "💼", "en": "Employment", "hi": "रोज़गार", "enDesc": "Jobs, wages and labour force data.", "hiDesc": "रोज़गार, वेतन और श्रम बल डेटा।", "url": "indicators/unemployment-rate.html"},
        {"icon": "🌾", "en": "Agriculture", "hi": "कृषि", "enDesc": "Crops, yield and rural livelihoods.", "hiDesc": "फसलें, उपज और ग्रामीण आजीविका।", "url": "explorer.html"},
        {"icon": "🏗️", "en": "Infrastructure", "hi": "बुनियादी ढांचा", "enDesc": "Roads, housing and connectivity.", "hiDesc": "सड़कें, आवास और कनेक्टिविटी।", "url": "explorer.html"},
        {"icon": "⚡", "en": "Energy", "hi": "ऊर्जा", "enDesc": "Power generation, access and mix.", "hiDesc": "बिजली उत्पादन, पहुंच और मिश्रण।", "url": "indicators/1-1_access-electricity-tot.html"},
        {"icon": "🌳", "en": "Environment", "hi": "पर्यावरण", "enDesc": "Emissions, forests and air quality.", "hiDesc": "उत्सर्जन, वन और वायु गुणवत्ता।", "url": "explorer.html"},
        {"icon": "🛡️", "en": "Crime & Safety", "hi": "अपराध व सुरक्षा", "enDesc": "Crime rates and public safety.", "hiDesc": "अपराध दर और सार्वजनिक सुरक्षा।", "url": "explorer.html"},
        {"icon": "👶", "en": "Women & Children", "hi": "महिला व बच्चे", "enDesc": "Health, safety and welfare indicators.", "hiDesc": "स्वास्थ्य, सुरक्षा और कल्याण संकेतक।", "url": "rankings.html#rank-sex-ratio"},
        {"icon": "🤝", "en": "Social Development", "hi": "सामाजिक विकास", "enDesc": "Human development and welfare.", "hiDesc": "मानव विकास और कल्याण।", "url": "history.html"},
        {"icon": "📱", "en": "Digital India", "hi": "डिजिटल इंडिया", "enDesc": "Internet, mobile and digital access.", "hiDesc": "इंटरनेट, मोबाइल और डिजिटल पहुंच।", "url": "stories/digital.html"},
        {"icon": "🏦", "en": "Banking & Finance", "hi": "बैंकिंग व वित्त", "enDesc": "Credit, inclusion and markets.", "hiDesc": "ऋण, समावेशन और बाज़ार।", "url": "tools/economic-comparator.html"},
        {"icon": "🏛️", "en": "Government & Governance", "hi": "सरकार व शासन", "enDesc": "Budgets, policy and administration.", "hiDesc": "बजट, नीति और प्रशासन।", "url": "methodology.html"},
        {"icon": "🗺️", "en": "States & Districts", "hi": "राज्य व ज़िले", "enDesc": "Regional profiles across India.", "hiDesc": "भारत भर के क्षेत्रीय प्रोफ़ाइल।", "url": "districts/index.html"},
        {"icon": "🌍", "en": "India vs World", "hi": "भारत बनाम विश्व", "enDesc": "Global rankings and benchmarks.", "hiDesc": "वैश्विक रैंकिंग और मानक।", "url": "world.html"},
        {"icon": "📈", "en": "Poverty", "hi": "गरीबी", "enDesc": "Income, deprivation and inequality.", "hiDesc": "आय, अभाव और असमानता।", "url": "explorer.html"}
    ]
    
    cat_cards = ""
    for c in categories:
        cat_cards += f"""        <a href="{c['url']}" class="category-card" style="text-decoration:none; color:inherit;">
          <span class="category-icon" aria-hidden="true">{c['icon']}</span>
          <h3 data-en="{c['en']}" data-hi="{c['hi']}">{c['en']}</h3>
          <p data-en="{c['enDesc']}" data-hi="{c['hiDesc']}">{c['enDesc']}</p>
          <span class="category-cta" data-en="Explore →" data-hi="एक्सप्लोर करें →">Explore →</span>
        </a>\n"""

    new_categories = f"""  <!-- CATEGORIES -->
  <section class="section categories" id="categories">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow" data-en="Categories" data-hi="श्रेणियां">Categories</p>
        <h2 data-en="Explore by Category" data-hi="श्रेणी अनुसार एक्सप्लोर करें">Explore by Category</h2>
        <p class="section-sub" data-en="Eighteen verified data categories connecting national, state, and district metrics." data-hi="अठारह सत्यापित डेटा श्रेणियां जो राष्ट्रीय, राज्य और ज़िला मेट्रिक्स को जोड़ती हैं।">Eighteen verified data categories connecting national, state, and district metrics.</p>
      </header>

      <div class="category-grid" id="category-grid">
{cat_cards}      </div>
    </div>
  </section>"""
    html = re.sub(r'<!-- CATEGORIES -->.*?<!-- COMPARE -->', new_categories + '\n\n  <!-- COMPARE -->', html, flags=re.DOTALL)

    # 5. Update Compare with Live Interactive Tool
    new_compare = """  <!-- COMPARE -->
  <section class="section compare" id="compare">
    <div class="wrap compare-grid">
      <div class="compare-copy">
        <p class="eyebrow" data-en="Comparison Engine" data-hi="तुलना इंजन">Comparison Engine</p>
        <h2 data-en="Compare Any Two States" data-hi="किन्हीं दो राज्यों की तुलना करें">Compare Any Two States</h2>
        <p class="section-sub" data-en="Pick any two states or UTs to instantly calculate relative economic power, literacy gap, unemployment variance, and demographic balance." data-hi="आर्थिक शक्ति, साक्षरता अंतर, बेरोज़गारी और जनसांख्यिकी संतुलन की तुरंत गणना करने के लिए किन्हीं दो राज्यों को चुनें।">Pick any two states or UTs to instantly calculate relative economic power, literacy gap, unemployment variance, and demographic balance.</p>
        <a class="btn btn-outline" id="home-cmp-launch-btn" href="compare.html?s1=maharashtra&s2=gujarat" data-en="Launch Full Deep Comparison →" data-hi="पूर्ण गहन तुलना खोलें →">Launch Full Deep Comparison →</a>
      </div>

      <div class="home-cmp-container">
        <div class="home-cmp-controls">
          <select id="home-cmp-state1" class="home-cmp-select" aria-label="Select State 1"></select>
          <span class="home-cmp-vs-badge">VS</span>
          <select id="home-cmp-state2" class="home-cmp-select" aria-label="Select State 2"></select>
        </div>

        <div id="home-cmp-results">
          <!-- Populated in real-time by home.js with live comparative bars -->
        </div>
      </div>
    </div>
  </section>"""
    html = re.sub(r'<!-- COMPARE -->.*?<!-- RANKINGS -->', new_compare + '\n\n  <!-- RANKINGS -->', html, flags=re.DOTALL)

    # 6. Update Rankings with Visual Horizontal Bar Charts
    new_rankings = """  <!-- RANKINGS -->
  <section class="section rankings" id="rankings">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow" data-en="Rankings" data-hi="रैंकिंग">Rankings</p>
        <h2 data-en="State Leaderboards &amp; Benchmark Charts" data-hi="राज्य लीडरबोर्ड एवं बेंचमार्क चार्ट">State Leaderboards &amp; Benchmark Charts</h2>
        <p class="section-sub" data-en="Top performing Indian states benchmarked across verified economic, educational, and demographic metrics." data-hi="सत्यापित आर्थिक, शैक्षिक और जनसांख्यिकी मेट्रिक्स में शीर्ष प्रदर्शन करने वाले भारतीय राज्य।">Top performing Indian states benchmarked across verified economic, educational, and demographic metrics.</p>
      </header>

      <div class="ranking-grid">
        <!-- Card 1: Literacy -->
        <a href="rankings.html#rank-literacy-rate" class="ranking-card">
          <h3 data-en="Top States by Literacy" data-hi="साक्षरता में शीर्ष राज्य">Top States by Literacy</h3>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#1 Kerala</span><span class="ranking-bar-val">94.0%</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--teal" style="width: 94%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#2 Lakshadweep</span><span class="ranking-bar-val">91.85%</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--teal" style="width: 91.85%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#3 Mizoram</span><span class="ranking-bar-val">91.33%</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--teal" style="width: 91.33%;"></div></div>
          </div>
          <span style="font-size:12px; color:var(--teal); font-weight:600; margin-top:16px; display:inline-block;">Full Literacy Table (36 States) →</span>
        </a>

        <!-- Card 2: GSDP -->
        <a href="rankings.html#rank-gdp" class="ranking-card">
          <h3 data-en="Top States by GSDP" data-hi="जीडीपी में शीर्ष राज्य">Top States by GSDP</h3>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#1 Maharashtra</span><span class="ranking-bar-val">₹38.79L Cr</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--saffron" style="width: 100%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#2 Tamil Nadu</span><span class="ranking-bar-val">₹23.64L Cr</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--saffron" style="width: 61%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#3 Gujarat</span><span class="ranking-bar-val">₹22.61L Cr</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--saffron" style="width: 58%;"></div></div>
          </div>
          <span style="font-size:12px; color:var(--teal); font-weight:600; margin-top:16px; display:inline-block;">Full GSDP Table (36 States) →</span>
        </a>

        <!-- Card 3: Unemployment -->
        <a href="rankings.html#rank-unemployment-rate" class="ranking-card">
          <h3 data-en="Lowest Unemployment" data-hi="न्यूनतम बेरोज़गारी वाले राज्य">Lowest Unemployment</h3>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#1 Sikkim</span><span class="ranking-bar-val">1.9%</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--green" style="width: 19%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#2 Madhya Pradesh</span><span class="ranking-bar-val">2.4%</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--green" style="width: 24%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#3 Gujarat</span><span class="ranking-bar-val">2.5%</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--green" style="width: 25%;"></div></div>
          </div>
          <span style="font-size:12px; color:var(--teal); font-weight:600; margin-top:16px; display:inline-block;">Full Employment Table (36 States) →</span>
        </a>

        <!-- Card 4: Sex Ratio -->
        <a href="rankings.html#rank-sex-ratio" class="ranking-card">
          <h3 data-en="Highest Sex Ratio" data-hi="उच्चतम लिंगानुपात">Highest Sex Ratio</h3>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#1 Kerala</span><span class="ranking-bar-val">1,084</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--purple" style="width: 100%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#2 Puducherry</span><span class="ranking-bar-val">1,037</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--purple" style="width: 95%;"></div></div>
          </div>
          <div class="ranking-bar-item">
            <div class="ranking-bar-meta"><span class="ranking-bar-name">#3 Tamil Nadu</span><span class="ranking-bar-val">996</span></div>
            <div class="ranking-bar-track"><div class="ranking-bar-fill ranking-bar-fill--purple" style="width: 92%;"></div></div>
          </div>
          <span style="font-size:12px; color:var(--teal); font-weight:600; margin-top:16px; display:inline-block;">Full Demographics Table (36 States) →</span>
        </a>
      </div>

      <a class="btn btn-outline" href="rankings.html" data-en="Explore All Rankings &amp; Tables →" data-hi="सभी रैंकिंग व तालिकाएं देखें →">Explore All Rankings &amp; Tables →</a>
    </div>
  </section>"""
    html = re.sub(r'<!-- RANKINGS -->.*?<!-- MASTER TOOLS & CALCULATORS -->', new_rankings + '\n\n  <!-- MASTER TOOLS & CALCULATORS -->', html, flags=re.DOTALL)

    # 7. Update Master Tools Section with Quick Mini Calculator
    new_tools = """  <!-- MASTER TOOLS & CALCULATORS -->
  <section class="section tools-preview" id="tools" style="background: rgba(255,255,255,0.02); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow" data-en="Interactive Engines" data-hi="इंटरएक्टिव इंजनों">Interactive Engines</p>
        <h2 data-en="Master Data Tools &amp; Simulators" data-hi="मास्टर डेटा टूल्स एवं सिमुलेटर">Master Data Tools &amp; Simulators</h2>
        <p class="section-sub" data-en="Dynamic calculators and comparative models projecting state trajectories, global benchmarks, and growth milestones." data-hi="राज्यों के विकास, वैश्विक समकक्षों और मील के पत्थरों का अनुमान लगाने वाले गतिशील कैलकुलेटर और मॉडल।">Dynamic calculators and comparative models projecting state trajectories, global benchmarks, and growth milestones.</p>
      </header>

      <!-- Quick Interactive Mini Tool -->
      <div class="quick-tool-card" style="margin-bottom: 32px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <span class="story-badge" style="background:var(--teal); color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:700; text-transform:uppercase;">Live Calculator</span>
            <h3 style="margin-top:6px; font-size:20px;">Quick Economic &amp; Sovereign Equivalence Matcher</h3>
          </div>
          <div style="min-width: 220px;">
            <label for="quick-tool-state" style="font-size:12px; font-family:var(--font-mono); color:var(--text-faint); display:block; margin-bottom:4px;">SELECT STATE:</label>
            <select id="quick-tool-state" class="quick-tool-select"></select>
          </div>
        </div>

        <div class="quick-tool-kpi-grid">
          <div class="quick-tool-kpi">
            <span class="quick-tool-kpi-label">Nominal GSDP (USD)</span>
            <span class="quick-tool-kpi-val" id="quick-tool-usd">$467 Billion</span>
          </div>
          <div class="quick-tool-kpi">
            <span class="quick-tool-kpi-label">Sovereign Country Match</span>
            <span class="quick-tool-kpi-val" id="quick-tool-country">🇨🇭 Switzerland</span>
          </div>
          <div class="quick-tool-kpi">
            <span class="quick-tool-kpi-label">National Economy Share</span>
            <span class="quick-tool-kpi-val" id="quick-tool-share">14.2% of India</span>
          </div>
          <div class="quick-tool-kpi">
            <span class="quick-tool-kpi-label">Economy Doubling Clock</span>
            <span class="quick-tool-kpi-val" id="quick-tool-doubling">7.2 Years (at 10% CAGR)</span>
          </div>
        </div>

        <div>
          <a id="quick-tool-link" href="tools/economic-comparator.html?state=maharashtra" class="btn btn-outline" style="font-size:13px; padding:8px 18px;">Open Full Economic Simulator →</a>
        </div>
      </div>

      <div class="story-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
        <a href="tools/economic-comparator.html" class="story-card" style="text-decoration:none; color:inherit; display:flex; flex-direction:column; justify-content:space-between; padding:24px; border:1px solid var(--border); border-radius:12px; background:var(--surface-1);">
          <div>
            <span class="story-badge" style="background:var(--saffron); color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;" data-en="Economic Model" data-hi="आर्थिक मॉडल">Economic Model</span>
            <h3 style="margin-top:14px; font-size:19px;" data-en="Economic Power &amp; Country Comparator" data-hi="आर्थिक शक्ति एवं देश तुलनित्र">Economic Power &amp; Country Comparator</h3>
            <p style="font-size:14px; color:var(--text-faint); margin-top:8px; line-height:1.6;" data-en="Convert state GSDP to nominal USD, map closest sovereign nations (e.g. Maharashtra ≈ Switzerland), and calculate GDP doubling time via Rule of 72." data-hi="राज्य जीएसडीपी को अमेरिकी डॉलर में बदलें, समकक्ष संप्रभु देशों का मिलान करें और विकास दर से अर्थव्यवस्था के दोगुना होने का समय निकालें।">Convert state GSDP to nominal USD, map closest sovereign nations (e.g. Maharashtra ≈ Switzerland), and calculate GDP doubling time via Rule of 72.</p>
          </div>
          <span style="font-size:13px; font-weight:600; color:var(--teal); margin-top:18px;">Launch Economic Engine →</span>
        </a>

        <a href="tools/demographic-calculator.html" class="story-card" style="text-decoration:none; color:inherit; display:flex; flex-direction:column; justify-content:space-between; padding:24px; border:1px solid var(--border); border-radius:12px; background:var(--surface-1);">
          <div>
            <span class="story-badge" style="background:var(--teal); color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;" data-en="Demographic Simulator" data-hi="जनसांख्यिकी सिमुलेटर">Demographic Simulator</span>
            <h3 style="margin-top:14px; font-size:19px;" data-en="Demographic &amp; Universal Literacy Projector" data-hi="जनसांख्यिकी एवं साक्षरता प्रक्षेपक">Demographic &amp; Universal Literacy Projector</h3>
            <p style="font-size:14px; color:var(--text-faint); margin-top:8px; line-height:1.6;" data-en="Simulate 100% universal literacy achievement years with adjustable gain rates, compare state-to-state parity gaps, and analyze gender sex ratios." data-hi="साक्षरता दर में वार्षिक वृद्धि के साथ 100% साक्षरता तक पहुंचने के वर्ष का अनुकरण करें, राज्यों के बीच अंतर और लिंगानुपात का विश्लेषण करें।">Simulate 100% universal literacy achievement years with adjustable gain rates, compare state-to-state parity gaps, and analyze gender sex ratios.</p>
          </div>
          <span style="font-size:13px; font-weight:600; color:var(--teal); margin-top:18px;">Launch Demographic Projector →</span>
        </a>

        <a href="explorer.html" class="story-card" style="text-decoration:none; color:inherit; display:flex; flex-direction:column; justify-content:space-between; padding:24px; border:1px solid var(--border); border-radius:12px; background:var(--surface-1);">
          <div>
            <span class="story-badge" style="background:#8e44ad; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;" data-en="Data Matrix" data-hi="डेटा मैट्रिक्स">Data Matrix</span>
            <h3 style="margin-top:14px; font-size:19px;" data-en="Interactive Cross-State Explorer" data-hi="इंटरएक्टिव क्रॉस-स्टेट एक्सप्लोरर">Interactive Cross-State Explorer</h3>
            <p style="font-size:14px; color:var(--text-faint); margin-top:8px; line-height:1.6;" data-en="Dynamic multi-metric matrix across all 36 States &amp; UTs with sorting, filtering, percentile distribution bars, and one-click CSV export." data-hi="सॉर्टिंग, फ़िल्टरिंग, प्रतिशत वितरण और एक-क्लिक सीएसवी निर्यात के साथ सभी 36 राज्यों और केंद्र शासित प्रदेशों का बहु-मीट्रिक मैट्रिक्स।">Dynamic multi-metric matrix across all 36 States &amp; UTs with sorting, filtering, percentile distribution bars, and one-click CSV export.</p>
          </div>
          <span style="font-size:13px; font-weight:600; color:var(--teal); margin-top:18px;">Open Data Explorer →</span>
        </a>
      </div>

      <div style="margin-top: 24px; display: flex; gap: 12px; flex-wrap: wrap;">
        <a class="btn btn-outline" href="tools/index.html" data-en="Explore All Master Tools →" data-hi="सभी मास्टर टूल्स देखें →">Explore All Master Tools →</a>
        <a class="btn btn-outline" href="compare.html" data-en="Side-by-Side Compare →" data-hi="साथ-साथ तुलना करें →">Side-by-Side Compare →</a>
      </div>
    </div>
  </section>"""
    html = re.sub(r'<!-- MASTER TOOLS & CALCULATORS -->.*?<!-- DATA STORIES -->', new_tools + '\n\n  <!-- DATA STORIES -->', html, flags=re.DOTALL)

    # 8. Update Why IndiaMetrix with Clickable Links
    new_why = """  <!-- WHY INDIAMETRIX -->
  <section class="section why" id="about">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow" data-en="Why IndiaMetrix" data-hi="IndiaMetrix क्यों">Why IndiaMetrix</p>
        <h2 data-en="Built to Be Trusted" data-hi="भरोसे के लिए बनाया गया">Built to Be Trusted</h2>
      </header>

      <div class="why-grid">
        <a href="sources.html" class="why-card">
          <h3 data-en="Verified Data" data-hi="सत्यापित डेटा">Verified Data</h3>
          <p data-en="Built around reliable public data sources, cited at every indicator." data-hi="विश्वसनीय सार्वजनिक डेटा स्रोतों पर आधारित, हर संकेतक पर उद्धृत।">Built around reliable public data sources, cited at every indicator.</p>
        </a>
        <a href="explorer.html" class="why-card">
          <h3 data-en="Clear Visuals" data-hi="स्पष्ट विज़ुअल्स">Clear Visuals</h3>
          <p data-en="Charts and rankings make complex statistics easier to understand." data-hi="चार्ट और रैंकिंग जटिल आंकड़ों को समझना आसान बनाते हैं।">Charts and rankings make complex statistics easier to understand.</p>
        </a>
        <a href="compare.html" class="why-card">
          <h3 data-en="Compare India" data-hi="भारत की तुलना">Compare India</h3>
          <p data-en="Compare states, districts and countries side by side." data-hi="राज्यों, ज़िलों और देशों की साथ-साथ तुलना करें।">Compare states, districts and countries side by side.</p>
        </a>
        <a href="methodology.html" class="why-card">
          <h3 data-en="Always Improving" data-hi="निरंतर सुधार">Always Improving</h3>
          <p data-en="Data sources can be checked and updated as automation is built out." data-hi="जैसे-जैसे स्वचालन विकसित होगा, डेटा स्रोतों की जांच और अपडेट होते रहेंगे।">Data sources can be checked and updated as automation is built out.</p>
        </a>
      </div>
    </div>
  </section>"""
    html = re.sub(r'<!-- WHY INDIAMETRIX -->.*?<!-- TRUST / SOURCES -->', new_why + '\n\n  <!-- TRUST / SOURCES -->', html, flags=re.DOTALL)

    # 9. Add assets/js/home.js script tag before assets/js/search.js
    if 'src="assets/js/home.js"' not in html:
        html = html.replace('<script src="assets/js/search.js"></script>', '<script src="assets/js/home.js"></script>\n<script src="assets/js/search.js"></script>')

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Upgraded index.html successfully.")

if __name__ == "__main__":
    build()

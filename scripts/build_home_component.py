import json
import os

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    explorer_path = os.path.join(root, "data", "explorer.json")
    with open(explorer_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    states = data.get("states", [])
    
    country_equivalents = {
        "maharashtra": {"country": "Switzerland", "flag": "🇨🇭", "gdp_usd": 467},
        "tamil-nadu": {"country": "Portugal", "flag": "🇵🇹", "gdp_usd": 285},
        "gujarat": {"country": "Greece", "flag": "🇬🇷", "gdp_usd": 272},
        "karnataka": {"country": "Peru", "flag": "🇵🇪", "gdp_usd": 270},
        "uttar-pradesh": {"country": "Qatar", "flag": "🇶🇦", "gdp_usd": 268},
        "west-bengal": {"country": "Hungary", "flag": "🇭🇺", "gdp_usd": 204},
        "rajasthan": {"country": "Kuwait", "flag": "🇰🇼", "gdp_usd": 169},
        "andhra-pradesh": {"country": "Morocco", "flag": "🇲🇦", "gdp_usd": 157},
        "telangana": {"country": "Slovakia", "flag": "🇸🇰", "gdp_usd": 155},
        "madhya-pradesh": {"country": "Ecuador", "flag": "🇪🇨", "gdp_usd": 150},
        "kerala": {"country": "Bulgaria", "flag": "🇧🇬", "gdp_usd": 120},
        "delhi": {"country": "Oman", "flag": "🇴🇲", "gdp_usd": 118},
        "haryana": {"country": "Guatemala", "flag": "🇬🇹", "gdp_usd": 115},
        "bihar": {"country": "Panama", "flag": "🇵🇦", "gdp_usd": 85},
        "odisha": {"country": "Costa Rica", "flag": "🇨🇷", "gdp_usd": 88},
        "punjab": {"country": "Uruguay", "flag": "🇺🇾", "gdp_usd": 78},
        "assam": {"country": "Jordan", "flag": "🇯🇴", "gdp_usd": 54},
        "chhattisgarh": {"country": "Slovenia", "flag": "🇸🇮", "gdp_usd": 53},
        "jharkhand": {"country": "Lithuania", "flag": "🇱🇹", "gdp_usd": 48},
        "uttarakhand": {"country": "Latvia", "flag": "🇱🇻", "gdp_usd": 38},
        "himachal-pradesh": {"country": "Cyprus", "flag": "🇨🇾", "gdp_usd": 24},
        "jammu-kashmir": {"country": "Iceland", "flag": "🇮🇸", "gdp_usd": 24},
        "goa": {"country": "Malta", "flag": "🇲🇹", "gdp_usd": 11},
        "tripura": {"country": "Montenegro", "flag": "🇲🇪", "gdp_usd": 8.5},
        "chandigarh": {"country": "Mauritius", "flag": "🇲🇺", "gdp_usd": 6.5},
        "puducherry": {"country": "Bahamas", "flag": "🇧🇸", "gdp_usd": 5.2},
        "meghalaya": {"country": "Fiji", "flag": "🇫🇯", "gdp_usd": 5.0},
        "sikkim": {"country": "Maldives", "flag": "🇲🇻", "gdp_usd": 4.8},
        "manipur": {"country": "Barbados", "flag": "🇧🇧", "gdp_usd": 4.6},
        "nagaland": {"country": "Guyana", "flag": "🇬🇾", "gdp_usd": 4.2},
        "arunachal-pradesh": {"country": "Suriname", "flag": "🇸🇷", "gdp_usd": 4.1},
        "mizoram": {"country": "Andorra", "flag": "🇦🇩", "gdp_usd": 3.7},
        "dadra-nagar-haveli-daman-diu": {"country": "Bhutan", "flag": "🇧🇹", "gdp_usd": 3.0},
        "ladakh": {"country": "Belize", "flag": "🇧🇿", "gdp_usd": 1.2},
        "andaman-nicobar": {"country": "Saint Lucia", "flag": "🇱🇨", "gdp_usd": 1.2},
        "lakshadweep": {"country": "Seychelles", "flag": "🇸🇨", "gdp_usd": 0.2}
    }
    
    clean_states = {}
    for s in states:
        sid = s["id"]
        inds = {i["id"]: i["value"] for i in s.get("indicators", [])}
        equiv = country_equivalents.get(sid, {"country": "Sovereign Nation", "flag": "🌐", "gdp_usd": 10})
        clean_states[sid] = {
            "id": sid,
            "name": s["name"]["en"],
            "nameHi": s["name"]["hi"],
            "pop": inds.get("population", 0),
            "gdp": inds.get("gdp", 0),
            "gdp_usd": equiv["gdp_usd"],
            "equiv_country": equiv["country"],
            "equiv_flag": equiv["flag"],
            "lit": inds.get("literacy-rate", 0),
            "unemp": inds.get("unemployment", 0),
            "sex": inds.get("sex-ratio", 0),
            "area": inds.get("area", 0)
        }

    js_code = f"""/**
 * IndiaMetrix Homepage Interactive Engine
 * Embedded dataset for 100% offline & file:/// zero-CORS reliability.
 * Powers:
 * 1. Interactive State-to-State Comparison Engine with Live Bar Charts
 * 2. Interactive SVG India Map with Hover HUD & Metric Choropleth
 * 3. Quick Economic Power Calculator with Sovereign Country Equivalents
 * 4. Region Matrix Filter
 */

(function() {{
  'use strict';

  const STATES_DATA = {json.dumps(clean_states, ensure_ascii=False, indent=2)};
  window.IM_STATES_DATA = STATES_DATA;

  // National Totals / Benchmarks
  const NATIONAL_DATA = {{
    gdpCr: 27241000,
    pop: 1463865525,
    lit: 74.04,
    unemp: 3.1,
    sex: 943
  }};

  /* =========================================================
     1. Interactive Compare Engine on Homepage
     ========================================================= */
  function initCompareEngine() {{
    const s1Select = document.getElementById('home-cmp-state1');
    const s2Select = document.getElementById('home-cmp-state2');
    const resultsContainer = document.getElementById('home-cmp-results');
    const launchBtn = document.getElementById('home-cmp-launch-btn');

    if (!s1Select || !s2Select || !resultsContainer) return;

    // Populate dropdowns
    const sortedStates = Object.values(STATES_DATA).sort((a, b) => a.name.localeCompare(b.name));
    
    s1Select.innerHTML = '';
    s2Select.innerHTML = '';

    sortedStates.forEach(st => {{
      const opt1 = document.createElement('option');
      opt1.value = st.id;
      opt1.textContent = st.name;
      if (st.id === 'maharashtra') opt1.selected = true;
      s1Select.appendChild(opt1);

      const opt2 = document.createElement('option');
      opt2.value = st.id;
      opt2.textContent = st.name;
      if (st.id === 'gujarat') opt2.selected = true;
      s2Select.appendChild(opt2);
    }});

    function formatCr(crores) {{
      if (crores >= 100000) {{
        return '₹' + (crores / 100000).toFixed(2) + 'L Cr';
      }}
      return '₹' + Number(crores).toLocaleString('en-IN') + ' Cr';
    }}

    function formatPop(p) {{
      if (p >= 10000000) {{
        return (p / 10000000).toFixed(2) + ' Cr';
      }}
      if (p >= 100000) {{
        return (p / 100000).toFixed(2) + ' Lakh';
      }}
      return Number(p).toLocaleString('en-IN');
    }}

    function renderComparison() {{
      const id1 = s1Select.value;
      const id2 = s2Select.value;
      const d1 = STATES_DATA[id1];
      const d2 = STATES_DATA[id2];

      if (!d1 || !d2) return;

      if (launchBtn) {{
        launchBtn.href = 'compare.html?s1=' + encodeURIComponent(id1) + '&s2=' + encodeURIComponent(id2);
        launchBtn.setAttribute('data-en', 'Launch Full Deep Comparison (' + d1.name + ' vs ' + d2.name + ') →');
        launchBtn.textContent = 'Launch Full Deep Comparison (' + d1.name + ' vs ' + d2.name + ') →';
      }}

      const metrics = [
        {{
          label: 'GSDP Economy',
          v1: d1.gdp,
          v2: d2.gdp,
          fmt1: formatCr(d1.gdp) + ' ($' + d1.gdp_usd + 'B)',
          fmt2: formatCr(d2.gdp) + ' ($' + d2.gdp_usd + 'B)',
          higherBetter: true,
          unit: 'Cr'
        }},
        {{
          label: 'Literacy Rate',
          v1: d1.lit,
          v2: d2.lit,
          fmt1: d1.lit.toFixed(1) + '%',
          fmt2: d2.lit.toFixed(1) + '%',
          higherBetter: true,
          unit: '%'
        }},
        {{
          label: 'Population',
          v1: d1.pop,
          v2: d2.pop,
          fmt1: formatPop(d1.pop),
          fmt2: formatPop(d2.pop),
          higherBetter: false,
          unit: 'count'
        }},
        {{
          label: 'Unemployment Rate',
          v1: d1.unemp,
          v2: d2.unemp,
          fmt1: d1.unemp.toFixed(1) + '%',
          fmt2: d2.unemp.toFixed(1) + '%',
          higherBetter: false,
          unit: '%'
        }},
        {{
          label: 'Sex Ratio (F/1000 M)',
          v1: d1.sex,
          v2: d2.sex,
          fmt1: d1.sex.toString(),
          fmt2: d2.sex.toString(),
          higherBetter: true,
          unit: 'ratio'
        }}
      ];

      let html = '';
      metrics.forEach(m => {{
        const maxVal = Math.max(m.v1, m.v2, 0.001);
        const bar1Pct = Math.max(10, Math.min(100, (m.v1 / maxVal) * 100));
        const bar2Pct = Math.max(10, Math.min(100, (m.v2 / maxVal) * 100));

        let deltaTxt = '';
        let deltaClass = '';
        if (m.v1 !== m.v2) {{
          const pctDiff = Math.abs(((m.v1 - m.v2) / (m.v2 || 1)) * 100).toFixed(1);
          if (m.higherBetter) {{
            if (m.v1 > m.v2) {{
              deltaTxt = d1.name + ' +' + pctDiff + '%';
              deltaClass = 'im-diff-pos';
            }} else {{
              deltaTxt = d2.name + ' +' + pctDiff + '%';
              deltaClass = 'im-diff-neg';
            }}
          }} else {{
            if (m.v1 < m.v2) {{
              deltaTxt = d1.name + ' is ' + Math.abs(m.v1 - m.v2).toFixed(1) + '% lower';
              deltaClass = 'im-diff-pos';
            }} else {{
              deltaTxt = d2.name + ' is ' + Math.abs(m.v1 - m.v2).toFixed(1) + '% lower';
              deltaClass = 'im-diff-neg';
            }}
          }}
        }} else {{
          deltaTxt = 'Equal';
          deltaClass = 'im-diff-neutral';
        }}

        html += `
          <div class="home-cmp-row">
            <div class="home-cmp-row-header">
              <span class="home-cmp-label">${{m.label}}</span>
              <span class="home-cmp-delta ${{deltaClass}}">${{deltaTxt}}</span>
            </div>
            <div class="home-cmp-bars-container">
              <div class="home-cmp-side">
                <div class="home-cmp-val">${{m.fmt1}}</div>
                <div class="home-cmp-bar-track">
                  <div class="home-cmp-bar home-cmp-bar--1" style="width: ${{bar1Pct}}%;"></div>
                </div>
              </div>
              <div class="home-cmp-side">
                <div class="home-cmp-val">${{m.fmt2}}</div>
                <div class="home-cmp-bar-track">
                  <div class="home-cmp-bar home-cmp-bar--2" style="width: ${{bar2Pct}}%;"></div>
                </div>
              </div>
            </div>
          </div>
        `;
      }});

      resultsContainer.innerHTML = html;
    }}

    s1Select.addEventListener('change', renderComparison);
    s2Select.addEventListener('change', renderComparison);
    renderComparison();
  }}

  /* =========================================================
     2. Interactive SVG India Map & State Visualizer
     ========================================================= */
  function initIndiaMap() {{
    const mapContainer = document.getElementById('home-map-container');
    const hudBox = document.getElementById('home-map-hud');
    const metricBtns = document.querySelectorAll('[data-map-metric]');
    const statesGrid = document.getElementById('home-states-quickgrid');

    if (!mapContainer) return;

    let currentMetric = 'gdp'; // 'gdp' | 'lit' | 'pop'

    const allGdp = Object.values(STATES_DATA).map(s => s.gdp);
    const maxGdp = Math.max(...allGdp);
    const maxPop = Math.max(...Object.values(STATES_DATA).map(s => s.pop));

    function getMetricColor(state, metric) {{
      if (metric === 'gdp') {{
        const r = state.gdp / maxGdp;
        if (r > 0.6) return '#F2A93B';
        if (r > 0.3) return '#D97706';
        if (r > 0.15) return '#0D9488';
        if (r > 0.05) return '#1B2745';
        return '#141E33';
      }} else if (metric === 'lit') {{
        const l = state.lit;
        if (l >= 90) return '#2BB7A0';
        if (l >= 80) return '#0D9488';
        if (l >= 70) return '#213955';
        return '#1B2745';
      }} else {{
        const p = state.pop / maxPop;
        if (p > 0.5) return '#E67E22';
        if (p > 0.25) return '#D97706';
        if (p > 0.1) return '#0D9488';
        return '#1B2745';
      }}
    }}

    function updateMapColors() {{
      const statePaths = mapContainer.querySelectorAll('[data-state-id]');
      statePaths.forEach(el => {{
        const sid = el.getAttribute('data-state-id');
        const st = STATES_DATA[sid];
        if (st) {{
          const col = getMetricColor(st, currentMetric);
          el.style.fill = col;
        }}
      }});
    }}

    function showStateHUD(sid) {{
      const st = STATES_DATA[sid];
      if (!st || !hudBox) return;

      const gdpStr = (st.gdp >= 100000) ? '₹' + (st.gdp / 100000).toFixed(2) + 'L Cr ($' + st.gdp_usd + 'B)' : '₹' + Number(st.gdp).toLocaleString('en-IN') + ' Cr';
      const popStr = (st.pop >= 10000000) ? (st.pop / 10000000).toFixed(2) + ' Cr' : Number(st.pop).toLocaleString('en-IN');

      hudBox.innerHTML = `
        <div class="map-hud-inner">
          <div class="map-hud-head">
            <span class="map-hud-flag">${{st.equiv_flag}}</span>
            <div>
              <h4 class="map-hud-title">${{st.name}}</h4>
              <p class="map-hud-equiv">Economy equivalent to <strong>${{st.equiv_country}}</strong></p>
            </div>
          </div>
          <div class="map-hud-metrics">
            <div><span class="m-lbl">GSDP</span><span class="m-val">${{gdpStr}}</span></div>
            <div><span class="m-lbl">Literacy</span><span class="m-val">${{st.lit}}%</span></div>
            <div><span class="m-lbl">Population</span><span class="m-val">${{popStr}}</span></div>
          </div>
          <a href="states/${{st.id}}.html" class="map-hud-link">Explore ${{st.name}} Full Profile →</a>
        </div>
      `;
      hudBox.style.display = 'block';
    }}

    // Bind state paths
    const statePaths = mapContainer.querySelectorAll('[data-state-id]');
    statePaths.forEach(path => {{
      const sid = path.getAttribute('data-state-id');
      path.style.cursor = 'pointer';
      path.style.transition = 'fill 0.25s ease, stroke 0.25s ease, filter 0.25s ease';

      path.addEventListener('mouseenter', () => {{
        path.style.filter = 'brightness(1.4) drop-shadow(0 0 8px var(--teal))';
        path.style.stroke = '#F2A93B';
        path.style.strokeWidth = '2px';
        showStateHUD(sid);
      }});

      path.addEventListener('mouseleave', () => {{
        path.style.filter = '';
        path.style.stroke = 'var(--border-strong)';
        path.style.strokeWidth = '1px';
      }});

      path.addEventListener('click', () => {{
        window.location.href = 'states/' + sid + '.html';
      }});
    }});

    // Metric Toggle Buttons
    metricBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        metricBtns.forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        currentMetric = btn.getAttribute('data-map-metric');
        updateMapColors();
      }});
    }});

    updateMapColors();

    // Default HUD to Maharashtra
    showStateHUD('maharashtra');

    // Render Quick States Grid underneath
    if (statesGrid) {{
      const sorted = Object.values(STATES_DATA).sort((a,b) => b.gdp - a.gdp);
      let gridHtml = '';
      sorted.forEach(st => {{
        const gdpStr = (st.gdp >= 100000) ? '₹' + (st.gdp / 100000).toFixed(1) + 'L Cr' : '₹' + Number(st.gdp).toLocaleString('en-IN') + ' Cr';
        gridHtml += `
          <a href="states/${{st.id}}.html" class="home-state-chip" data-state-id="${{st.id}}">
            <span class="chip-name">${{st.name}}</span>
            <span class="chip-stat">${{gdpStr}}</span>
          </a>
        `;
      }});
      statesGrid.innerHTML = gridHtml;
    }}
  }}

  /* =========================================================
     3. Quick Mini Economic Power Calculator on Homepage
     ========================================================= */
  function initQuickCalc() {{
    const select = document.getElementById('quick-tool-state');
    const usdVal = document.getElementById('quick-tool-usd');
    const equivCountry = document.getElementById('quick-tool-country');
    const shareVal = document.getElementById('quick-tool-share');
    const doublingVal = document.getElementById('quick-tool-doubling');
    const launchLink = document.getElementById('quick-tool-link');

    if (!select || !usdVal) return;

    // Populate
    const sorted = Object.values(STATES_DATA).sort((a,b) => a.name.localeCompare(b.name));
    select.innerHTML = '';
    sorted.forEach(st => {{
      const opt = document.createElement('option');
      opt.value = st.id;
      opt.textContent = st.name;
      if (st.id === 'maharashtra') opt.selected = true;
      select.appendChild(opt);
    }});

    function updateQuickTool() {{
      const st = STATES_DATA[select.value];
      if (!st) return;

      if (usdVal) usdVal.textContent = '$' + st.gdp_usd + ' Billion';
      if (equivCountry) equivCountry.innerHTML = `<span style="font-size:18px;">${{st.equiv_flag}}</span> ${{st.equiv_country}}`;
      
      const share = ((st.gdp / NATIONAL_DATA.gdpCr) * 100).toFixed(2);
      if (shareVal) shareVal.textContent = share + '% of India';

      if (doublingVal) doublingVal.textContent = '7.2 Years (at 10% CAGR)';

      if (launchLink) {{
        launchLink.href = 'tools/economic-comparator.html?state=' + encodeURIComponent(st.id);
      }}
    }}

    select.addEventListener('change', updateQuickTool);
    updateQuickTool();
  }}

  // DOM Ready
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', () => {{
      initCompareEngine();
      initIndiaMap();
      initQuickCalc();
    }});
  }} else {{
    initCompareEngine();
    initIndiaMap();
    initQuickCalc();
  }}
}})();
"""

    out_path = os.path.join(root, "assets", "js", "home.js")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(js_code)
    print(f"Generated {out_path} successfully ({len(clean_states)} states).")

if __name__ == "__main__":
    main()

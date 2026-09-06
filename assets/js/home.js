/**
 * IndiaMetrix Homepage Interactive Engine
 * Embedded dataset for 100% offline & file:/// zero-CORS reliability.
 * Powers:
 * 1. Interactive State-to-State Comparison Engine with Live Bar Charts
 * 2. Interactive SVG India Map with Hover HUD & Metric Choropleth
 * 3. Quick Economic Power Calculator with Sovereign Country Equivalents
 * 4. Region Matrix Filter
 */

(function() {
  'use strict';

  const STATES_DATA = {
  "andaman-nicobar": {
    "id": "andaman-nicobar",
    "name": "Andaman & Nicobar",
    "nameHi": "अंडमान और निकोबार",
    "pop": 380581,
    "gdp": 10300,
    "gdp_usd": 1.2,
    "equiv_country": "Saint Lucia",
    "equiv_flag": "🇱🇨",
    "lit": 86.63,
    "unemp": 4.5,
    "sex": 876,
    "area": 8249
  },
  "andhra-pradesh": {
    "id": "andhra-pradesh",
    "name": "Andhra Pradesh",
    "nameHi": "आंध्र प्रदेश",
    "pop": 49577103,
    "gdp": 1303524,
    "gdp_usd": 157,
    "equiv_country": "Morocco",
    "equiv_flag": "🇲🇦",
    "lit": 67.02,
    "unemp": 4.1,
    "sex": 993,
    "area": 162968
  },
  "arunachal-pradesh": {
    "id": "arunachal-pradesh",
    "name": "Arunachal Pradesh",
    "nameHi": "अरुणाचल प्रदेश",
    "pop": 1383727,
    "gdp": 37845,
    "gdp_usd": 4.1,
    "equiv_country": "Suriname",
    "equiv_flag": "🇸🇷",
    "lit": 65.38,
    "unemp": 3.7,
    "sex": 938,
    "area": 83743
  },
  "assam": {
    "id": "assam",
    "name": "Assam",
    "nameHi": "असम",
    "pop": 31205576,
    "gdp": 493167,
    "gdp_usd": 54,
    "equiv_country": "Jordan",
    "equiv_flag": "🇯🇴",
    "lit": 72.19,
    "unemp": 4.4,
    "sex": 958,
    "area": 78438
  },
  "bihar": {
    "id": "bihar",
    "name": "Bihar",
    "nameHi": "बिहार",
    "pop": 104099452,
    "gdp": 751396,
    "gdp_usd": 85,
    "equiv_country": "Panama",
    "equiv_flag": "🇵🇦",
    "lit": 61.8,
    "unemp": 3.9,
    "sex": 918,
    "area": 94163
  },
  "chandigarh": {
    "id": "chandigarh",
    "name": "Chandigarh",
    "nameHi": "चंडीगढ़",
    "pop": 1055450,
    "gdp": 45635,
    "gdp_usd": 6.5,
    "equiv_country": "Mauritius",
    "equiv_flag": "🇲🇺",
    "lit": 86.05,
    "unemp": 5.6,
    "sex": 818,
    "area": 114
  },
  "chhattisgarh": {
    "id": "chhattisgarh",
    "name": "Chhattisgarh",
    "nameHi": "छत्तीसगढ़",
    "pop": 25545198,
    "gdp": 457608,
    "gdp_usd": 53,
    "equiv_country": "Slovenia",
    "equiv_flag": "🇸🇮",
    "lit": 70.28,
    "unemp": 2.4,
    "sex": 991,
    "area": 135191
  },
  "dadra-nagar-haveli-daman-diu": {
    "id": "dadra-nagar-haveli-daman-diu",
    "name": "Dadra & Nagar Haveli and Daman & Diu",
    "nameHi": "दादरा और नगर हवेली तथा दमन और दीव",
    "pop": 585764,
    "gdp": 40500,
    "gdp_usd": 3.0,
    "equiv_country": "Bhutan",
    "equiv_flag": "🇧🇹",
    "lit": 76.24,
    "unemp": 3.1,
    "sex": 774,
    "area": 603
  },
  "delhi": {
    "id": "delhi",
    "name": "Delhi",
    "nameHi": "दिल्ली",
    "pop": 16787941,
    "gdp": 1043759,
    "gdp_usd": 118,
    "equiv_country": "Oman",
    "equiv_flag": "🇴🇲",
    "lit": 86.21,
    "unemp": 1.9,
    "sex": 868,
    "area": 1483
  },
  "goa": {
    "id": "goa",
    "name": "Goa",
    "nameHi": "गोवा",
    "pop": 1458545,
    "gdp": 91416,
    "gdp_usd": 11,
    "equiv_country": "Malta",
    "equiv_flag": "🇲🇹",
    "lit": 88.7,
    "unemp": 9.7,
    "sex": 973,
    "area": 3702
  },
  "gujarat": {
    "id": "gujarat",
    "name": "Gujarat",
    "nameHi": "गुजरात",
    "pop": 60439692,
    "gdp": 2262000,
    "gdp_usd": 272,
    "equiv_country": "Greece",
    "equiv_flag": "🇬🇷",
    "lit": 78.03,
    "unemp": 2.2,
    "sex": 919,
    "area": 196024
  },
  "haryana": {
    "id": "haryana",
    "name": "Haryana",
    "nameHi": "हरियाणा",
    "pop": 25351462,
    "gdp": 994116,
    "gdp_usd": 115,
    "equiv_country": "Guatemala",
    "equiv_flag": "🇬🇹",
    "lit": 75.55,
    "unemp": 6.1,
    "sex": 879,
    "area": 44212
  },
  "himachal-pradesh": {
    "id": "himachal-pradesh",
    "name": "Himachal Pradesh",
    "nameHi": "हिमाचल प्रदेश",
    "pop": 6864602,
    "gdp": 191728,
    "gdp_usd": 24,
    "equiv_country": "Cyprus",
    "equiv_flag": "🇨🇾",
    "lit": 82.8,
    "unemp": 4.4,
    "sex": 972,
    "area": 55673
  },
  "jammu-kashmir": {
    "id": "jammu-kashmir",
    "name": "Jammu & Kashmir",
    "nameHi": "जम्मू और कश्मीर",
    "pop": 12267032,
    "gdp": 224102,
    "gdp_usd": 24,
    "equiv_country": "Iceland",
    "equiv_flag": "🇮🇸",
    "lit": 67.16,
    "unemp": 4.4,
    "sex": 889,
    "area": 42241
  },
  "jharkhand": {
    "id": "jharkhand",
    "name": "Jharkhand",
    "nameHi": "झारखंड",
    "pop": 32988134,
    "gdp": 393722,
    "gdp_usd": 48,
    "equiv_country": "Lithuania",
    "equiv_flag": "🇱🇹",
    "lit": 66.41,
    "unemp": 2.0,
    "sex": 948,
    "area": 79714
  },
  "karnataka": {
    "id": "karnataka",
    "name": "Karnataka",
    "nameHi": "कर्नाटक",
    "pop": 61095297,
    "gdp": 2241368,
    "gdp_usd": 270,
    "equiv_country": "Peru",
    "equiv_flag": "🇵🇪",
    "lit": 75.36,
    "unemp": 2.4,
    "sex": 973,
    "area": 191791
  },
  "kerala": {
    "id": "kerala",
    "name": "Kerala",
    "nameHi": "केरल",
    "pop": 33406061,
    "gdp": 1046188,
    "gdp_usd": 120,
    "equiv_country": "Bulgaria",
    "equiv_flag": "🇧🇬",
    "lit": 94.0,
    "unemp": 7.0,
    "sex": 1084,
    "area": 38863
  },
  "ladakh": {
    "id": "ladakh",
    "name": "Ladakh",
    "nameHi": "लद्दाख",
    "pop": 274000,
    "gdp": 4200,
    "gdp_usd": 1.2,
    "equiv_country": "Belize",
    "equiv_flag": "🇧🇿",
    "lit": 74.27,
    "unemp": 3.5,
    "sex": 853,
    "area": 59146
  },
  "lakshadweep": {
    "id": "lakshadweep",
    "name": "Lakshadweep",
    "nameHi": "लक्षद्वीप",
    "pop": 64473,
    "gdp": 850,
    "gdp_usd": 0.2,
    "equiv_country": "Seychelles",
    "equiv_flag": "🇸🇨",
    "lit": 91.85,
    "unemp": 6.8,
    "sex": 946,
    "area": 32
  },
  "madhya-pradesh": {
    "id": "madhya-pradesh",
    "name": "Madhya Pradesh",
    "nameHi": "मध्य प्रदेश",
    "pop": 72626809,
    "gdp": 1322421,
    "gdp_usd": 150,
    "equiv_country": "Ecuador",
    "equiv_flag": "🇪🇨",
    "lit": 69.32,
    "unemp": 1.6,
    "sex": 931,
    "area": 308245
  },
  "maharashtra": {
    "id": "maharashtra",
    "name": "Maharashtra",
    "nameHi": "महाराष्ट्र",
    "pop": 112374333,
    "gdp": 3527084,
    "gdp_usd": 467,
    "equiv_country": "Switzerland",
    "equiv_flag": "🇨🇭",
    "lit": 82.34,
    "unemp": 3.1,
    "sex": 929,
    "area": 307713
  },
  "manipur": {
    "id": "manipur",
    "name": "Manipur",
    "nameHi": "मणिपुर",
    "pop": 2855794,
    "gdp": 39340,
    "gdp_usd": 4.6,
    "equiv_country": "Barbados",
    "equiv_flag": "🇧🇧",
    "lit": 76.94,
    "unemp": 4.0,
    "sex": 985,
    "area": 22327
  },
  "meghalaya": {
    "id": "meghalaya",
    "name": "Meghalaya",
    "nameHi": "मेघालय",
    "pop": 2966889,
    "gdp": 42697,
    "gdp_usd": 5.0,
    "equiv_country": "Fiji",
    "equiv_flag": "🇫🇯",
    "lit": 74.43,
    "unemp": 2.7,
    "sex": 989,
    "area": 22429
  },
  "mizoram": {
    "id": "mizoram",
    "name": "Mizoram",
    "nameHi": "मिज़ोरम",
    "pop": 1097206,
    "gdp": 30500,
    "gdp_usd": 3.7,
    "equiv_country": "Andorra",
    "equiv_flag": "🇦🇩",
    "lit": 91.33,
    "unemp": 3.2,
    "sex": 976,
    "area": 21081
  },
  "nagaland": {
    "id": "nagaland",
    "name": "Nagaland",
    "nameHi": "नागालैंड",
    "pop": 1978502,
    "gdp": 35680,
    "gdp_usd": 4.2,
    "equiv_country": "Guyana",
    "equiv_flag": "🇬🇾",
    "lit": 79.55,
    "unemp": 5.4,
    "sex": 931,
    "area": 16579
  },
  "odisha": {
    "id": "odisha",
    "name": "Odisha",
    "nameHi": "ओडिशा",
    "pop": 41974218,
    "gdp": 774869,
    "gdp_usd": 88,
    "equiv_country": "Costa Rica",
    "equiv_flag": "🇨🇷",
    "lit": 72.87,
    "unemp": 3.9,
    "sex": 979,
    "area": 155707
  },
  "puducherry": {
    "id": "puducherry",
    "name": "Puducherry",
    "nameHi": "पुडुचेरी",
    "pop": 1247953,
    "gdp": 39019,
    "gdp_usd": 5.2,
    "equiv_country": "Bahamas",
    "equiv_flag": "🇧🇸",
    "lit": 85.85,
    "unemp": 4.2,
    "sex": 1037,
    "area": 479
  },
  "punjab": {
    "id": "punjab",
    "name": "Punjab",
    "nameHi": "पंजाब",
    "pop": 27743338,
    "gdp": 637000,
    "gdp_usd": 78,
    "equiv_country": "Uruguay",
    "equiv_flag": "🇺🇾",
    "lit": 75.84,
    "unemp": 6.4,
    "sex": 895,
    "area": 50362
  },
  "rajasthan": {
    "id": "rajasthan",
    "name": "Rajasthan",
    "nameHi": "राजस्थान",
    "pop": 68548437,
    "gdp": 1414000,
    "gdp_usd": 169,
    "equiv_country": "Kuwait",
    "equiv_flag": "🇰🇼",
    "lit": 66.11,
    "unemp": 4.4,
    "sex": 928,
    "area": 342239
  },
  "sikkim": {
    "id": "sikkim",
    "name": "Sikkim",
    "nameHi": "सिक्किम",
    "pop": 610577,
    "gdp": 42754,
    "gdp_usd": 4.8,
    "equiv_country": "Maldives",
    "equiv_flag": "🇲🇻",
    "lit": 81.42,
    "unemp": 3.0,
    "sex": 890,
    "area": 7096
  },
  "tamil-nadu": {
    "id": "tamil-nadu",
    "name": "Tamil Nadu",
    "nameHi": "तमिलनाडु",
    "pop": 72147030,
    "gdp": 2364514,
    "gdp_usd": 285,
    "equiv_country": "Portugal",
    "equiv_flag": "🇵🇹",
    "lit": 80.09,
    "unemp": 3.8,
    "sex": 996,
    "area": 130058
  },
  "telangana": {
    "id": "telangana",
    "name": "Telangana",
    "nameHi": "तेलंगाना",
    "pop": 35003674,
    "gdp": 1302371,
    "gdp_usd": 155,
    "equiv_country": "Slovakia",
    "equiv_flag": "🇸🇰",
    "lit": 66.54,
    "unemp": 4.4,
    "sex": 988,
    "area": 112077
  },
  "tripura": {
    "id": "tripura",
    "name": "Tripura",
    "nameHi": "त्रिपुरा",
    "pop": 3673917,
    "gdp": 64000,
    "gdp_usd": 8.5,
    "equiv_country": "Montenegro",
    "equiv_flag": "🇲🇪",
    "lit": 87.22,
    "unemp": 1.4,
    "sex": 960,
    "area": 10486
  },
  "uttar-pradesh": {
    "id": "uttar-pradesh",
    "name": "Uttar Pradesh",
    "nameHi": "उत्तर प्रदेश",
    "pop": 199812341,
    "gdp": 2258040,
    "gdp_usd": 268,
    "equiv_country": "Qatar",
    "equiv_flag": "🇶🇦",
    "lit": 67.68,
    "unemp": 2.4,
    "sex": 912,
    "area": 240928
  },
  "uttarakhand": {
    "id": "uttarakhand",
    "name": "Uttarakhand",
    "nameHi": "उत्तराखंड",
    "pop": 10086292,
    "gdp": 302621,
    "gdp_usd": 38,
    "equiv_country": "Latvia",
    "equiv_flag": "🇱🇻",
    "lit": 78.82,
    "unemp": 4.5,
    "sex": 963,
    "area": 53483
  },
  "west-bengal": {
    "id": "west-bengal",
    "name": "West Bengal",
    "nameHi": "पश्चिम बंगाल",
    "pop": 91276115,
    "gdp": 1530000,
    "gdp_usd": 204,
    "equiv_country": "Hungary",
    "equiv_flag": "🇭🇺",
    "lit": 76.26,
    "unemp": 4.1,
    "sex": 950,
    "area": 88752
  }
};
  window.IM_STATES_DATA = STATES_DATA;

  // National Totals / Benchmarks
  const NATIONAL_DATA = {
    gdpCr: 27241000,
    pop: 1463865525,
    lit: 74.04,
    unemp: 3.1,
    sex: 943
  };

  /* =========================================================
     1. Interactive Compare Engine on Homepage
     ========================================================= */
  function initCompareEngine() {
    const s1Select = document.getElementById('home-cmp-state1');
    const s2Select = document.getElementById('home-cmp-state2');
    const resultsContainer = document.getElementById('home-cmp-results');
    const launchBtn = document.getElementById('home-cmp-launch-btn');

    if (!s1Select || !s2Select || !resultsContainer) return;

    // Populate dropdowns
    const sortedStates = Object.values(STATES_DATA).sort((a, b) => a.name.localeCompare(b.name));
    
    s1Select.innerHTML = '';
    s2Select.innerHTML = '';

    sortedStates.forEach(st => {
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
    });

    function formatCr(crores) {
      if (crores >= 100000) {
        return '₹' + (crores / 100000).toFixed(2) + 'L Cr';
      }
      return '₹' + Number(crores).toLocaleString('en-IN') + ' Cr';
    }

    function formatPop(p) {
      if (p >= 10000000) {
        return (p / 10000000).toFixed(2) + ' Cr';
      }
      if (p >= 100000) {
        return (p / 100000).toFixed(2) + ' Lakh';
      }
      return Number(p).toLocaleString('en-IN');
    }

    function renderComparison() {
      const id1 = s1Select.value;
      const id2 = s2Select.value;
      const d1 = STATES_DATA[id1];
      const d2 = STATES_DATA[id2];

      if (!d1 || !d2) return;

      if (launchBtn) {
        launchBtn.href = 'compare.html?s1=' + encodeURIComponent(id1) + '&s2=' + encodeURIComponent(id2);
        launchBtn.setAttribute('data-en', 'Launch Full Deep Comparison (' + d1.name + ' vs ' + d2.name + ') →');
        launchBtn.textContent = 'Launch Full Deep Comparison (' + d1.name + ' vs ' + d2.name + ') →';
      }

      const metrics = [
        {
          label: 'GSDP Economy',
          v1: d1.gdp,
          v2: d2.gdp,
          fmt1: formatCr(d1.gdp) + ' ($' + d1.gdp_usd + 'B)',
          fmt2: formatCr(d2.gdp) + ' ($' + d2.gdp_usd + 'B)',
          higherBetter: true,
          unit: 'Cr'
        },
        {
          label: 'Literacy Rate',
          v1: d1.lit,
          v2: d2.lit,
          fmt1: d1.lit.toFixed(1) + '%',
          fmt2: d2.lit.toFixed(1) + '%',
          higherBetter: true,
          unit: '%'
        },
        {
          label: 'Population',
          v1: d1.pop,
          v2: d2.pop,
          fmt1: formatPop(d1.pop),
          fmt2: formatPop(d2.pop),
          higherBetter: false,
          unit: 'count'
        },
        {
          label: 'Unemployment Rate',
          v1: d1.unemp,
          v2: d2.unemp,
          fmt1: d1.unemp.toFixed(1) + '%',
          fmt2: d2.unemp.toFixed(1) + '%',
          higherBetter: false,
          unit: '%'
        },
        {
          label: 'Sex Ratio (F/1000 M)',
          v1: d1.sex,
          v2: d2.sex,
          fmt1: d1.sex.toString(),
          fmt2: d2.sex.toString(),
          higherBetter: true,
          unit: 'ratio'
        }
      ];

      let html = '';
      metrics.forEach(m => {
        const maxVal = Math.max(m.v1, m.v2, 0.001);
        const bar1Pct = Math.max(10, Math.min(100, (m.v1 / maxVal) * 100));
        const bar2Pct = Math.max(10, Math.min(100, (m.v2 / maxVal) * 100));

        let deltaTxt = '';
        let deltaClass = '';
        if (m.v1 !== m.v2) {
          const pctDiff = Math.abs(((m.v1 - m.v2) / (m.v2 || 1)) * 100).toFixed(1);
          if (m.higherBetter) {
            if (m.v1 > m.v2) {
              deltaTxt = d1.name + ' +' + pctDiff + '%';
              deltaClass = 'im-diff-pos';
            } else {
              deltaTxt = d2.name + ' +' + pctDiff + '%';
              deltaClass = 'im-diff-neg';
            }
          } else {
            if (m.v1 < m.v2) {
              deltaTxt = d1.name + ' is ' + Math.abs(m.v1 - m.v2).toFixed(1) + '% lower';
              deltaClass = 'im-diff-pos';
            } else {
              deltaTxt = d2.name + ' is ' + Math.abs(m.v1 - m.v2).toFixed(1) + '% lower';
              deltaClass = 'im-diff-neg';
            }
          }
        } else {
          deltaTxt = 'Equal';
          deltaClass = 'im-diff-neutral';
        }

        html += `
          <div class="home-cmp-row">
            <div class="home-cmp-row-header">
              <span class="home-cmp-label">${m.label}</span>
              <span class="home-cmp-delta ${deltaClass}">${deltaTxt}</span>
            </div>
            <div class="home-cmp-bars-container">
              <div class="home-cmp-side">
                <div class="home-cmp-val">${m.fmt1}</div>
                <div class="home-cmp-bar-track">
                  <div class="home-cmp-bar home-cmp-bar--1" style="width: ${bar1Pct}%;"></div>
                </div>
              </div>
              <div class="home-cmp-side">
                <div class="home-cmp-val">${m.fmt2}</div>
                <div class="home-cmp-bar-track">
                  <div class="home-cmp-bar home-cmp-bar--2" style="width: ${bar2Pct}%;"></div>
                </div>
              </div>
            </div>
          </div>
        `;
      });

      resultsContainer.innerHTML = html;
    }

    s1Select.addEventListener('change', renderComparison);
    s2Select.addEventListener('change', renderComparison);
    renderComparison();
  }

  /* =========================================================
     2. Interactive SVG India Map & State Visualizer
     ========================================================= */
  function initIndiaMap() {
    const mapContainer = document.getElementById('home-map-container');
    const hudBox = document.getElementById('home-map-hud');
    const metricBtns = document.querySelectorAll('[data-map-metric]');
    const statesGrid = document.getElementById('home-states-quickgrid');

    if (!mapContainer) return;

    let currentMetric = 'gdp'; // 'gdp' | 'lit' | 'pop'

    const allGdp = Object.values(STATES_DATA).map(s => s.gdp);
    const maxGdp = Math.max(...allGdp);
    const maxPop = Math.max(...Object.values(STATES_DATA).map(s => s.pop));

    function getMetricColor(state, metric) {
      if (metric === 'gdp') {
        const r = state.gdp / maxGdp;
        if (r > 0.6) return '#F2A93B';
        if (r > 0.3) return '#D97706';
        if (r > 0.15) return '#0D9488';
        if (r > 0.05) return '#1B2745';
        return '#141E33';
      } else if (metric === 'lit') {
        const l = state.lit;
        if (l >= 90) return '#2BB7A0';
        if (l >= 80) return '#0D9488';
        if (l >= 70) return '#213955';
        return '#1B2745';
      } else {
        const p = state.pop / maxPop;
        if (p > 0.5) return '#E67E22';
        if (p > 0.25) return '#D97706';
        if (p > 0.1) return '#0D9488';
        return '#1B2745';
      }
    }

    function updateMapColors() {
      const statePaths = mapContainer.querySelectorAll('[data-state-id]');
      statePaths.forEach(el => {
        const sid = el.getAttribute('data-state-id');
        const st = STATES_DATA[sid];
        if (st) {
          const col = getMetricColor(st, currentMetric);
          el.style.fill = col;
        }
      });
    }

    function showStateHUD(sid) {
      const st = STATES_DATA[sid];
      if (!st || !hudBox) return;

      const gdpStr = (st.gdp >= 100000) ? '₹' + (st.gdp / 100000).toFixed(2) + 'L Cr ($' + st.gdp_usd + 'B)' : '₹' + Number(st.gdp).toLocaleString('en-IN') + ' Cr';
      const popStr = (st.pop >= 10000000) ? (st.pop / 10000000).toFixed(2) + ' Cr' : Number(st.pop).toLocaleString('en-IN');

      hudBox.innerHTML = `
        <div class="map-hud-inner">
          <div class="map-hud-head">
            <span class="map-hud-flag">${st.equiv_flag}</span>
            <div>
              <h4 class="map-hud-title">${st.name}</h4>
              <p class="map-hud-equiv">Economy equivalent to <strong>${st.equiv_country}</strong></p>
            </div>
          </div>
          <div class="map-hud-metrics">
            <div><span class="m-lbl">GSDP</span><span class="m-val">${gdpStr}</span></div>
            <div><span class="m-lbl">Literacy</span><span class="m-val">${st.lit}%</span></div>
            <div><span class="m-lbl">Population</span><span class="m-val">${popStr}</span></div>
          </div>
          <a href="states/${st.id}.html" class="map-hud-link">Explore ${st.name} Full Profile →</a>
        </div>
      `;
      hudBox.style.display = 'block';
    }

    // Bind state paths
    const statePaths = mapContainer.querySelectorAll('[data-state-id]');
    statePaths.forEach(path => {
      const sid = path.getAttribute('data-state-id');
      path.style.cursor = 'pointer';
      path.style.transition = 'fill 0.25s ease, stroke 0.25s ease, filter 0.25s ease';

      path.addEventListener('mouseenter', () => {
        path.style.filter = 'brightness(1.4) drop-shadow(0 0 8px var(--teal))';
        path.style.stroke = '#F2A93B';
        path.style.strokeWidth = '2px';
        showStateHUD(sid);
      });

      path.addEventListener('mouseleave', () => {
        path.style.filter = '';
        path.style.stroke = 'var(--border-strong)';
        path.style.strokeWidth = '1px';
      });

      path.addEventListener('click', () => {
        window.location.href = 'states/' + sid + '.html';
      });
    });

    // Metric Toggle Buttons
    metricBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        metricBtns.forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        currentMetric = btn.getAttribute('data-map-metric');
        updateMapColors();
      });
    });

    updateMapColors();

    // Default HUD to Maharashtra
    showStateHUD('maharashtra');

    // Render Quick States Grid underneath
    if (statesGrid) {
      const sorted = Object.values(STATES_DATA).sort((a,b) => b.gdp - a.gdp);
      let gridHtml = '';
      sorted.forEach(st => {
        const gdpStr = (st.gdp >= 100000) ? '₹' + (st.gdp / 100000).toFixed(1) + 'L Cr' : '₹' + Number(st.gdp).toLocaleString('en-IN') + ' Cr';
        gridHtml += `
          <a href="states/${st.id}.html" class="home-state-chip" data-state-id="${st.id}">
            <span class="chip-name">${st.name}</span>
            <span class="chip-stat">${gdpStr}</span>
          </a>
        `;
      });
      statesGrid.innerHTML = gridHtml;
    }
  }

  /* =========================================================
     3. Quick Mini Economic Power Calculator on Homepage
     ========================================================= */
  function initQuickCalc() {
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
    sorted.forEach(st => {
      const opt = document.createElement('option');
      opt.value = st.id;
      opt.textContent = st.name;
      if (st.id === 'maharashtra') opt.selected = true;
      select.appendChild(opt);
    });

    function updateQuickTool() {
      const st = STATES_DATA[select.value];
      if (!st) return;

      if (usdVal) usdVal.textContent = '$' + st.gdp_usd + ' Billion';
      if (equivCountry) equivCountry.innerHTML = `<span style="font-size:18px;">${st.equiv_flag}</span> ${st.equiv_country}`;
      
      const share = ((st.gdp / NATIONAL_DATA.gdpCr) * 100).toFixed(2);
      if (shareVal) shareVal.textContent = share + '% of India';

      if (doublingVal) doublingVal.textContent = '7.2 Years (at 10% CAGR)';

      if (launchLink) {
        launchLink.href = 'tools/economic-comparator.html?state=' + encodeURIComponent(st.id);
      }
    }

    select.addEventListener('change', updateQuickTool);
    updateQuickTool();
  }

  // DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initCompareEngine();
      initIndiaMap();
      initQuickCalc();
    });
  } else {
    initCompareEngine();
    initIndiaMap();
    initQuickCalc();
  }
})();

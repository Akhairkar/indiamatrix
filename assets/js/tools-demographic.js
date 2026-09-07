/**
 * IndiaMetrix Demographic & Universal Literacy Projector
 * Built on Census of India decadal records and SRS data.
 */

document.addEventListener('DOMContentLoaded', () => {
  const stateSelect = document.getElementById('state-select');
  const benchmarkSelect = document.getElementById('benchmark-select');
  const paceInput = document.getElementById('pace-rate');
  const paceSlider = document.getElementById('pace-slider');
  const paceDisplay = document.getElementById('pace-display');

  let statesData = [];

  const FALLBACK_EXPLORER_STATES = [{"id": "andaman-nicobar", "name": {"en": "Andaman & Nicobar", "hi": "\u0905\u0902\u0921\u092e\u093e\u0928 \u0914\u0930 \u0928\u093f\u0915\u094b\u092c\u093e\u0930"}, "indicators": [{"id": "population", "value": 380581}, {"id": "literacy-rate", "value": 86.63}, {"id": "gdp", "value": 10300}, {"id": "sex-ratio", "value": 876}]}, {"id": "andhra-pradesh", "name": {"en": "Andhra Pradesh", "hi": "\u0906\u0902\u0927\u094d\u0930 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 49577103}, {"id": "literacy-rate", "value": 67.02}, {"id": "gdp", "value": 1303524}, {"id": "sex-ratio", "value": 993}]}, {"id": "arunachal-pradesh", "name": {"en": "Arunachal Pradesh", "hi": "\u0905\u0930\u0941\u0923\u093e\u091a\u0932 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 1383727}, {"id": "literacy-rate", "value": 65.38}, {"id": "gdp", "value": 37845}, {"id": "sex-ratio", "value": 938}]}, {"id": "assam", "name": {"en": "Assam", "hi": "\u0905\u0938\u092e"}, "indicators": [{"id": "population", "value": 31205576}, {"id": "literacy-rate", "value": 72.19}, {"id": "gdp", "value": 493167}, {"id": "sex-ratio", "value": 958}]}, {"id": "bihar", "name": {"en": "Bihar", "hi": "\u092c\u093f\u0939\u093e\u0930"}, "indicators": [{"id": "population", "value": 104099452}, {"id": "literacy-rate", "value": 61.8}, {"id": "gdp", "value": 751396}, {"id": "sex-ratio", "value": 918}]}, {"id": "chandigarh", "name": {"en": "Chandigarh", "hi": "\u091a\u0902\u0921\u0940\u0917\u0922\u093c"}, "indicators": [{"id": "population", "value": 1055450}, {"id": "literacy-rate", "value": 86.05}, {"id": "gdp", "value": 45635}, {"id": "sex-ratio", "value": 818}]}, {"id": "chhattisgarh", "name": {"en": "Chhattisgarh", "hi": "\u091b\u0924\u094d\u0924\u0940\u0938\u0917\u0922\u093c"}, "indicators": [{"id": "population", "value": 25545198}, {"id": "literacy-rate", "value": 70.28}, {"id": "gdp", "value": 457608}, {"id": "sex-ratio", "value": 991}]}, {"id": "dadra-nagar-haveli-daman-diu", "name": {"en": "Dadra & Nagar Haveli and Daman & Diu", "hi": "\u0926\u093e\u0926\u0930\u093e \u0914\u0930 \u0928\u0917\u0930 \u0939\u0935\u0947\u0932\u0940 \u0924\u0925\u093e \u0926\u092e\u0928 \u0914\u0930 \u0926\u0940\u0935"}, "indicators": [{"id": "population", "value": 585764}, {"id": "literacy-rate", "value": 76.24}, {"id": "gdp", "value": 40500}, {"id": "sex-ratio", "value": 774}]}, {"id": "delhi", "name": {"en": "Delhi", "hi": "\u0926\u093f\u0932\u094d\u0932\u0940"}, "indicators": [{"id": "population", "value": 16787941}, {"id": "literacy-rate", "value": 86.21}, {"id": "gdp", "value": 1043759}, {"id": "sex-ratio", "value": 868}]}, {"id": "goa", "name": {"en": "Goa", "hi": "\u0917\u094b\u0935\u093e"}, "indicators": [{"id": "population", "value": 1458545}, {"id": "literacy-rate", "value": 88.7}, {"id": "gdp", "value": 91416}, {"id": "sex-ratio", "value": 973}]}, {"id": "gujarat", "name": {"en": "Gujarat", "hi": "\u0917\u0941\u091c\u0930\u093e\u0924"}, "indicators": [{"id": "population", "value": 60439692}, {"id": "literacy-rate", "value": 78.03}, {"id": "gdp", "value": 2262000}, {"id": "sex-ratio", "value": 919}]}, {"id": "haryana", "name": {"en": "Haryana", "hi": "\u0939\u0930\u093f\u092f\u093e\u0923\u093e"}, "indicators": [{"id": "population", "value": 25351462}, {"id": "literacy-rate", "value": 75.55}, {"id": "gdp", "value": 994116}, {"id": "sex-ratio", "value": 879}]}, {"id": "himachal-pradesh", "name": {"en": "Himachal Pradesh", "hi": "\u0939\u093f\u092e\u093e\u091a\u0932 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 6864602}, {"id": "literacy-rate", "value": 82.8}, {"id": "gdp", "value": 191728}, {"id": "sex-ratio", "value": 972}]}, {"id": "jammu-kashmir", "name": {"en": "Jammu & Kashmir", "hi": "\u091c\u092e\u094d\u092e\u0942 \u0914\u0930 \u0915\u0936\u094d\u092e\u0940\u0930"}, "indicators": [{"id": "population", "value": 12267032}, {"id": "literacy-rate", "value": 67.16}, {"id": "gdp", "value": 224102}, {"id": "sex-ratio", "value": 889}]}, {"id": "jharkhand", "name": {"en": "Jharkhand", "hi": "\u091d\u093e\u0930\u0916\u0902\u0921"}, "indicators": [{"id": "population", "value": 32988134}, {"id": "literacy-rate", "value": 66.41}, {"id": "gdp", "value": 393722}, {"id": "sex-ratio", "value": 948}]}, {"id": "karnataka", "name": {"en": "Karnataka", "hi": "\u0915\u0930\u094d\u0928\u093e\u091f\u0915"}, "indicators": [{"id": "population", "value": 61095297}, {"id": "literacy-rate", "value": 75.36}, {"id": "gdp", "value": 2241368}, {"id": "sex-ratio", "value": 973}]}, {"id": "kerala", "name": {"en": "Kerala", "hi": "\u0915\u0947\u0930\u0932"}, "indicators": [{"id": "population", "value": 33406061}, {"id": "literacy-rate", "value": 94.0}, {"id": "gdp", "value": 1046188}, {"id": "sex-ratio", "value": 1084}]}, {"id": "ladakh", "name": {"en": "Ladakh", "hi": "\u0932\u0926\u094d\u0926\u093e\u0916"}, "indicators": [{"id": "population", "value": 274000}, {"id": "literacy-rate", "value": 74.27}, {"id": "gdp", "value": 4200}, {"id": "sex-ratio", "value": 853}]}, {"id": "lakshadweep", "name": {"en": "Lakshadweep", "hi": "\u0932\u0915\u094d\u0937\u0926\u094d\u0935\u0940\u092a"}, "indicators": [{"id": "population", "value": 64473}, {"id": "literacy-rate", "value": 91.85}, {"id": "gdp", "value": 850}, {"id": "sex-ratio", "value": 946}]}, {"id": "madhya-pradesh", "name": {"en": "Madhya Pradesh", "hi": "\u092e\u0927\u094d\u092f \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 72626809}, {"id": "literacy-rate", "value": 69.32}, {"id": "gdp", "value": 1322421}, {"id": "sex-ratio", "value": 931}]}, {"id": "maharashtra", "name": {"en": "Maharashtra", "hi": "\u092e\u0939\u093e\u0930\u093e\u0937\u094d\u091f\u094d\u0930"}, "indicators": [{"id": "population", "value": 112374333}, {"id": "literacy-rate", "value": 82.34}, {"id": "gdp", "value": 3527084}, {"id": "sex-ratio", "value": 929}]}, {"id": "manipur", "name": {"en": "Manipur", "hi": "\u092e\u0923\u093f\u092a\u0941\u0930"}, "indicators": [{"id": "population", "value": 2855794}, {"id": "literacy-rate", "value": 76.94}, {"id": "gdp", "value": 39340}, {"id": "sex-ratio", "value": 985}]}, {"id": "meghalaya", "name": {"en": "Meghalaya", "hi": "\u092e\u0947\u0918\u093e\u0932\u092f"}, "indicators": [{"id": "population", "value": 2966889}, {"id": "literacy-rate", "value": 74.43}, {"id": "gdp", "value": 42697}, {"id": "sex-ratio", "value": 989}]}, {"id": "mizoram", "name": {"en": "Mizoram", "hi": "\u092e\u093f\u091c\u093c\u094b\u0930\u092e"}, "indicators": [{"id": "population", "value": 1097206}, {"id": "literacy-rate", "value": 91.33}, {"id": "gdp", "value": 30500}, {"id": "sex-ratio", "value": 976}]}, {"id": "nagaland", "name": {"en": "Nagaland", "hi": "\u0928\u093e\u0917\u093e\u0932\u0948\u0902\u0921"}, "indicators": [{"id": "population", "value": 1978502}, {"id": "literacy-rate", "value": 79.55}, {"id": "gdp", "value": 35680}, {"id": "sex-ratio", "value": 931}]}, {"id": "odisha", "name": {"en": "Odisha", "hi": "\u0913\u0921\u093f\u0936\u093e"}, "indicators": [{"id": "population", "value": 41974218}, {"id": "literacy-rate", "value": 72.87}, {"id": "gdp", "value": 774869}, {"id": "sex-ratio", "value": 979}]}, {"id": "puducherry", "name": {"en": "Puducherry", "hi": "\u092a\u0941\u0921\u0941\u091a\u0947\u0930\u0940"}, "indicators": [{"id": "population", "value": 1247953}, {"id": "literacy-rate", "value": 85.85}, {"id": "gdp", "value": 39019}, {"id": "sex-ratio", "value": 1037}]}, {"id": "punjab", "name": {"en": "Punjab", "hi": "\u092a\u0902\u091c\u093e\u092c"}, "indicators": [{"id": "population", "value": 27743338}, {"id": "literacy-rate", "value": 75.84}, {"id": "gdp", "value": 637000}, {"id": "sex-ratio", "value": 895}]}, {"id": "rajasthan", "name": {"en": "Rajasthan", "hi": "\u0930\u093e\u091c\u0938\u094d\u0925\u093e\u0928"}, "indicators": [{"id": "population", "value": 68548437}, {"id": "literacy-rate", "value": 66.11}, {"id": "gdp", "value": 1414000}, {"id": "sex-ratio", "value": 928}]}, {"id": "sikkim", "name": {"en": "Sikkim", "hi": "\u0938\u093f\u0915\u094d\u0915\u093f\u092e"}, "indicators": [{"id": "population", "value": 610577}, {"id": "literacy-rate", "value": 81.42}, {"id": "gdp", "value": 42754}, {"id": "sex-ratio", "value": 890}]}, {"id": "tamil-nadu", "name": {"en": "Tamil Nadu", "hi": "\u0924\u092e\u093f\u0932\u0928\u093e\u0921\u0941"}, "indicators": [{"id": "population", "value": 72147030}, {"id": "literacy-rate", "value": 80.09}, {"id": "gdp", "value": 2364514}, {"id": "sex-ratio", "value": 996}]}, {"id": "telangana", "name": {"en": "Telangana", "hi": "\u0924\u0947\u0932\u0902\u0917\u093e\u0928\u093e"}, "indicators": [{"id": "population", "value": 35003674}, {"id": "literacy-rate", "value": 66.54}, {"id": "gdp", "value": 1302371}, {"id": "sex-ratio", "value": 988}]}, {"id": "tripura", "name": {"en": "Tripura", "hi": "\u0924\u094d\u0930\u093f\u092a\u0941\u0930\u093e"}, "indicators": [{"id": "population", "value": 3673917}, {"id": "literacy-rate", "value": 87.22}, {"id": "gdp", "value": 64000}, {"id": "sex-ratio", "value": 960}]}, {"id": "uttar-pradesh", "name": {"en": "Uttar Pradesh", "hi": "\u0909\u0924\u094d\u0924\u0930 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 199812341}, {"id": "literacy-rate", "value": 67.68}, {"id": "gdp", "value": 2258040}, {"id": "sex-ratio", "value": 912}]}, {"id": "uttarakhand", "name": {"en": "Uttarakhand", "hi": "\u0909\u0924\u094d\u0924\u0930\u093e\u0916\u0902\u0921"}, "indicators": [{"id": "population", "value": 10086292}, {"id": "literacy-rate", "value": 78.82}, {"id": "gdp", "value": 302621}, {"id": "sex-ratio", "value": 963}]}, {"id": "west-bengal", "name": {"en": "West Bengal", "hi": "\u092a\u0936\u094d\u091a\u093f\u092e \u092c\u0902\u0917\u093e\u0932"}, "indicators": [{"id": "population", "value": 91276115}, {"id": "literacy-rate", "value": 76.26}, {"id": "gdp", "value": 1530000}, {"id": "sex-ratio", "value": 950}]}];

  function loadStates(data) {
    statesData = data || [];
    initDropdowns();
    readUrlParams();
    calculate();
  }

  fetch('../data/explorer.json')
    .then(res => {
      if (!res.ok) throw new Error("HTTP error " + res.status);
      return res.json();
    })
    .then(data => {
      loadStates(data.states);
    })
    .catch(err => {
      console.warn("Using offline fallback data for demographic tool:", err);
      loadStates(FALLBACK_EXPLORER_STATES);
    });

  function initDropdowns() {
    stateSelect.innerHTML = '';
    benchmarkSelect.innerHTML = '';

    statesData.forEach(state => {
      const opt1 = document.createElement('option');
      opt1.value = state.id;
      opt1.textContent = `${state.name.en} (${state.name.hi})`;
      stateSelect.appendChild(opt1);

      const opt2 = document.createElement('option');
      opt2.value = state.id;
      opt2.textContent = `${state.name.en} (${state.name.hi})`;
      benchmarkSelect.appendChild(opt2);
    });

    // Defaults
    if (statesData.some(s => s.id === 'bihar')) stateSelect.value = 'bihar';
    if (statesData.some(s => s.id === 'kerala')) benchmarkSelect.value = 'kerala';
  }

  function readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const s1 = params.get('s1');
    const s2 = params.get('s2');
    const p = params.get('pace');

    if (s1 && statesData.some(s => s.id === s1)) stateSelect.value = s1;
    if (s2 && statesData.some(s => s.id === s2)) benchmarkSelect.value = s2;
    if (p && !isNaN(parseFloat(p))) {
      const pVal = Math.min(5.0, Math.max(0.5, parseFloat(p)));
      paceInput.value = pVal;
      paceSlider.value = pVal;
      paceDisplay.textContent = `+${pVal}%/yr`;
    }
  }

  function syncPace(val) {
    paceInput.value = val;
    paceSlider.value = val;
    paceDisplay.textContent = `+${val}%/yr`;
    calculate();
  }

  if (paceSlider && paceInput) {
    paceSlider.addEventListener('input', (e) => syncPace(e.target.value));
    paceInput.addEventListener('input', (e) => syncPace(e.target.value));
  }

  if (stateSelect) {
    stateSelect.addEventListener('change', () => {
      calculate();
      updateUrl();
    });
  }

  if (benchmarkSelect) {
    benchmarkSelect.addEventListener('change', () => {
      calculate();
      updateUrl();
    });
  }

  function updateUrl() {
    const s1 = stateSelect.value;
    const s2 = benchmarkSelect.value;
    const p = paceInput.value;
    const newUrl = `${window.location.pathname}?s1=${s1}&s2=${s2}&pace=${p}`;
    window.history.replaceState(null, '', newUrl);
  }

  function calculate() {
    const s1Id = stateSelect.value;
    const s2Id = benchmarkSelect.value;

    const s1 = statesData.find(s => s.id === s1Id);
    const s2 = statesData.find(s => s.id === s2Id);
    if (!s1 || !s2) return;

    const annualGain = parseFloat(paceInput.value) || 1.5;

    // Get s1 indicators
    const lit1 = s1.indicators.find(i => i.id === 'literacy-rate')?.value || 70;
    const sex1 = s1.indicators.find(i => i.id === 'sex-ratio')?.value || 940;
    const pop1 = s1.indicators.find(i => i.id === 'population')?.value || 1000000;

    // Get s2 indicators
    const lit2 = s2.indicators.find(i => i.id === 'literacy-rate')?.value || 90;

    // 1. Universal Literacy Target (100%)
    const gapToUniversal = Math.max(0, (100 - lit1)).toFixed(2);
    const yearsToUniversal = Math.ceil(gapToUniversal / annualGain);
    const currentBaseYear = 2026; // Current simulation horizon
    const targetUniversalYear = currentBaseYear + yearsToUniversal;

    const isHi = document.documentElement.getAttribute('data-lang') === 'hi' || document.documentElement.lang === 'hi';
    const s1Name = isHi ? (s1.name.hi || s1.name.en) : s1.name.en;
    const s2Name = isHi ? (s2.name.hi || s2.name.en) : s2.name.en;

    // 2. State-to-State Catch-up
    const gapBetweenStates = (lit2 - lit1).toFixed(2);
    let catchupText = "";
    if (lit1 >= lit2) {
      catchupText = isHi ? `${s2Name} से ${Math.abs(gapBetweenStates)}% आगे है ✅` : `Already leads ${s2.name.en} by ${Math.abs(gapBetweenStates)}% ✅`;
    } else {
      const yearsCatchup = Math.ceil(Math.abs(gapBetweenStates) / annualGain);
      catchupText = isHi ? `${s2Name} के ${lit2}% के बराबर पहुँचने में ~${yearsCatchup} वर्ष (~${currentBaseYear + yearsCatchup} तक)` : `~${yearsCatchup} years to match ${s2.name.en}'s ${lit2}% (by ~${currentBaseYear + yearsCatchup})`;
    }

    // 3. Gender / Sex Ratio Analysis
    const naturalBenchmark = 950; // Females per 1000 males
    const sexDiff = sex1 - naturalBenchmark;
    let sexStatus = "";
    if (sexDiff >= 0) {
      sexStatus = isHi ? `सकारात्मक (950 मानक से +${sexDiff} अधिक)` : `Favorable (+${sexDiff} above 950 benchmark)`;
    } else {
      sexStatus = isHi ? `कमी (950 मानक से ${Math.abs(sexDiff)} कम)` : `Deficit (${Math.abs(sexDiff)} below 950 benchmark)`;
    }

    // Update DOM
    const s1NameEl = document.getElementById('res-s1-name');
    if (s1NameEl) s1NameEl.textContent = s1Name;

    document.getElementById('res-current-lit').textContent = `${lit1}%`;
    document.getElementById('res-lit-gap').textContent = `${gapToUniversal}%`;
    document.getElementById('res-universal-year').textContent = `~${targetUniversalYear}`;
    document.getElementById('res-years-to-100').textContent = isHi ? `+${annualGain}%/वर्ष पर ${yearsToUniversal} वर्ष आवश्यक` : `${yearsToUniversal} years required at +${annualGain}%/yr`;

    const bNameEl = document.getElementById('res-benchmark-name');
    if (bNameEl) bNameEl.textContent = s2Name;

    document.getElementById('res-benchmark-gap').textContent = `${gapBetweenStates > 0 ? '+' : ''}${gapBetweenStates}%`;
    document.getElementById('res-catchup-pace').textContent = catchupText;

    document.getElementById('res-sex-ratio').textContent = `${sex1}`;
    document.getElementById('res-sex-status').textContent = sexStatus;

    // Progress Bar Visualizer
    const bar = document.getElementById('lit-progress-bar');
    if (bar) {
      bar.style.width = `${Math.min(100, lit1)}%`;
      document.getElementById('bar-label').textContent = `${s1Name}: ${lit1}%`;
    }

    // Quick links
    const linkS1 = document.getElementById('link-s1-profile');
    if (linkS1) linkS1.href = `../states/${s1.id}.html`;
    const linkCompare = document.getElementById('link-compare-states');
    if (linkCompare) linkCompare.href = `../compare.html?s1=${s1.id}&s2=${s2.id}`;
  }

  document.querySelectorAll("[data-set-lang]").forEach(btn => {
    btn.addEventListener("click", () => {
      setTimeout(calculate, 50);
    });
  });
});

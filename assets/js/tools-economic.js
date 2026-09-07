/**
 * IndiaMetrix State Economic Power & Country Equivalence Calculator
 * Built on MoSPI 2022-23 GSDP and World Bank GDP data.
 */

document.addEventListener('DOMContentLoaded', () => {
  const stateSelect = document.getElementById('state-select');
  const growthInput = document.getElementById('growth-rate');
  const growthSlider = document.getElementById('growth-slider');
  const growthDisplay = document.getElementById('growth-display');

  // Country equivalents benchmark table (Nominal GDP in USD Billions)
  const countryEquivalents = [
    { country: "Switzerland", gdp_usd: 885, flag: "🇨🇭" },
    { country: "Poland", gdp_usd: 840, flag: "🇵🇱" },
    { country: "Argentina", gdp_usd: 640, flag: "🇦🇷" },
    { country: "Sweden", gdp_usd: 600, flag: "🇸🇪" },
    { country: "Belgium", gdp_usd: 590, flag: "🇧🇪" },
    { country: "Thailand", gdp_usd: 515, flag: "🇹🇭" },
    { country: "Ireland", gdp_usd: 505, flag: "🇮🇪" },
    { country: "Austria", gdp_usd: 500, flag: "🇦🇹" },
    { country: "Norway", gdp_usd: 485, flag: "🇳🇴" },
    { country: "Israel", gdp_usd: 470, flag: "🇮🇱" },
    { country: "UAE", gdp_usd: 450, flag: "🇦🇪" },
    { country: "Singapore", gdp_usd: 440, flag: "🇸🇬" },
    { country: "Malaysia", gdp_usd: 430, flag: "🇲🇾" },
    { country: "Philippines", gdp_usd: 425, flag: "🇵🇭" },
    { country: "Vietnam", gdp_usd: 410, flag: "🇻🇳" },
    { country: "Denmark", gdp_usd: 400, flag: "🇩🇰" },
    { country: "South Africa", gdp_usd: 380, flag: "🇿🇦" },
    { country: "Egypt", gdp_usd: 360, flag: "🇪🇬" },
    { country: "Colombia", gdp_usd: 350, flag: "🇨🇴" },
    { country: "Hong Kong", gdp_usd: 345, flag: "🇭🇰" },
    { country: "Romania", gdp_usd: 320, flag: "🇷🇴" },
    { country: "Chile", gdp_usd: 310, flag: "🇨🇱" },
    { country: "Czech Republic", gdp_usd: 290, flag: "🇨🇿" },
    { country: "Finland", gdp_usd: 280, flag: "🇫🇮" },
    { country: "Portugal", gdp_usd: 270, flag: "🇵🇹" },
    { country: "New Zealand", gdp_usd: 250, flag: "🇳🇿" },
    { country: "Peru", gdp_usd: 240, flag: "🇵🇪" },
    { country: "Greece", gdp_usd: 220, flag: "🇬🇷" },
    { country: "Qatar", gdp_usd: 215, flag: "🇶🇦" },
    { country: "Kazakhstan", gdp_usd: 210, flag: "🇰🇿" },
    { country: "Algeria", gdp_usd: 195, flag: "🇩🇿" },
    { country: "Hungary", gdp_usd: 190, flag: "🇭🇺" },
    { country: "Kuwait", gdp_usd: 180, flag: "🇰🇼" },
    { country: "Morocco", gdp_usd: 140, flag: "🇲🇦" },
    { country: "Slovakia", gdp_usd: 120, flag: "🇸🇰" },
    { country: "Ecuador", gdp_usd: 115, flag: "🇪🇨" },
    { country: "Kenya", gdp_usd: 110, flag: "🇰🇪" },
    { country: "Dominican Republic", gdp_usd: 105, flag: "🇩🇴" },
    { country: "Oman", gdp_usd: 100, flag: "🇴🇲" },
    { country: "Guatemala", gdp_usd: 95, flag: "🇬🇹" },
    { country: "Bulgaria", gdp_usd: 90, flag: "🇧🇬" },
    { country: "Uzbekistan", gdp_usd: 85, flag: "🇺🇿" },
    { country: "Croatia", gdp_usd: 80, flag: "🇭🇷" },
    { country: "Sri Lanka", gdp_usd: 75, flag: "🇱🇰" },
    { country: "Lithuania", gdp_usd: 70, flag: "🇱🇹" },
    { country: "Ghana", gdp_usd: 68, flag: "🇬🇭" },
    { country: "Serbia", gdp_usd: 65, flag: "🇷🇸" },
    { country: "Slovenia", gdp_usd: 62, flag: "🇸🇮" },
    { country: "Uruguay", gdp_usd: 60, flag: "🇺🇾" },
    { country: "Jordan", gdp_usd: 48, flag: "🇯🇴" },
    { country: "Tunisia", gdp_usd: 46, flag: "🇹🇳" },
    { country: "Uganda", gdp_usd: 45, flag: "🇺🇬" },
    { country: "Bolivia", gdp_usd: 43, flag: "🇧🇴" },
    { country: "Cameroon", gdp_usd: 42, flag: "🇨🇲" },
    { country: "Nepal", gdp_usd: 40, flag: "🇳🇵" },
    { country: "Estonia", gdp_usd: 38, flag: "🇪🇪" },
    { country: "Paraguay", gdp_usd: 37, flag: "🇵🇾" },
    { country: "Latvia", gdp_usd: 36, flag: "🇱🇻" },
    { country: "Cyprus", gdp_usd: 30, flag: "🇨🇾" },
    { country: "Iceland", gdp_usd: 28, flag: "🇮🇸" },
    { country: "Georgia", gdp_usd: 25, flag: "🇬🇪" },
    { country: "Armenia", gdp_usd: 20, flag: "🇦🇲" },
    { country: "Malta", gdp_usd: 18, flag: "🇲🇹" },
    { country: "Albania", gdp_usd: 18, flag: "🇦🇱" },
    { country: "Cyprus", gdp_usd: 17, flag: "🇨🇾" },
    { country: "Namibia", gdp_usd: 12, flag: "🇳🇦" },
    { country: "Mauritius", gdp_usd: 12, flag: "🇲🇺" },
    { country: "Moldova", gdp_usd: 14, flag: "🇲🇩" },
    { country: "Maldives", gdp_usd: 6, flag: "🇲🇻" },
    { country: "Fiji", gdp_usd: 5, flag: "🇫🇯" },
    { country: "Bhutan", gdp_usd: 3, flag: "🇧🇹" }
  ];

  let statesData = [];
  const USD_INR_RATE = 83.5;
  const INDIA_TOTAL_GDP_CR = 27241000; // ~₹272.4 Lakh Cr nominal base

  const FALLBACK_EXPLORER_STATES = [{"id": "andaman-nicobar", "name": {"en": "Andaman & Nicobar", "hi": "\u0905\u0902\u0921\u092e\u093e\u0928 \u0914\u0930 \u0928\u093f\u0915\u094b\u092c\u093e\u0930"}, "indicators": [{"id": "population", "value": 380581}, {"id": "literacy-rate", "value": 86.63}, {"id": "gdp", "value": 10300}, {"id": "sex-ratio", "value": 876}]}, {"id": "andhra-pradesh", "name": {"en": "Andhra Pradesh", "hi": "\u0906\u0902\u0927\u094d\u0930 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 49577103}, {"id": "literacy-rate", "value": 67.02}, {"id": "gdp", "value": 1303524}, {"id": "sex-ratio", "value": 993}]}, {"id": "arunachal-pradesh", "name": {"en": "Arunachal Pradesh", "hi": "\u0905\u0930\u0941\u0923\u093e\u091a\u0932 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 1383727}, {"id": "literacy-rate", "value": 65.38}, {"id": "gdp", "value": 37845}, {"id": "sex-ratio", "value": 938}]}, {"id": "assam", "name": {"en": "Assam", "hi": "\u0905\u0938\u092e"}, "indicators": [{"id": "population", "value": 31205576}, {"id": "literacy-rate", "value": 72.19}, {"id": "gdp", "value": 493167}, {"id": "sex-ratio", "value": 958}]}, {"id": "bihar", "name": {"en": "Bihar", "hi": "\u092c\u093f\u0939\u093e\u0930"}, "indicators": [{"id": "population", "value": 104099452}, {"id": "literacy-rate", "value": 61.8}, {"id": "gdp", "value": 751396}, {"id": "sex-ratio", "value": 918}]}, {"id": "chandigarh", "name": {"en": "Chandigarh", "hi": "\u091a\u0902\u0921\u0940\u0917\u0922\u093c"}, "indicators": [{"id": "population", "value": 1055450}, {"id": "literacy-rate", "value": 86.05}, {"id": "gdp", "value": 45635}, {"id": "sex-ratio", "value": 818}]}, {"id": "chhattisgarh", "name": {"en": "Chhattisgarh", "hi": "\u091b\u0924\u094d\u0924\u0940\u0938\u0917\u0922\u093c"}, "indicators": [{"id": "population", "value": 25545198}, {"id": "literacy-rate", "value": 70.28}, {"id": "gdp", "value": 457608}, {"id": "sex-ratio", "value": 991}]}, {"id": "dadra-nagar-haveli-daman-diu", "name": {"en": "Dadra & Nagar Haveli and Daman & Diu", "hi": "\u0926\u093e\u0926\u0930\u093e \u0914\u0930 \u0928\u0917\u0930 \u0939\u0935\u0947\u0932\u0940 \u0924\u0925\u093e \u0926\u092e\u0928 \u0914\u0930 \u0926\u0940\u0935"}, "indicators": [{"id": "population", "value": 585764}, {"id": "literacy-rate", "value": 76.24}, {"id": "gdp", "value": 40500}, {"id": "sex-ratio", "value": 774}]}, {"id": "delhi", "name": {"en": "Delhi", "hi": "\u0926\u093f\u0932\u094d\u0932\u0940"}, "indicators": [{"id": "population", "value": 16787941}, {"id": "literacy-rate", "value": 86.21}, {"id": "gdp", "value": 1043759}, {"id": "sex-ratio", "value": 868}]}, {"id": "goa", "name": {"en": "Goa", "hi": "\u0917\u094b\u0935\u093e"}, "indicators": [{"id": "population", "value": 1458545}, {"id": "literacy-rate", "value": 88.7}, {"id": "gdp", "value": 91416}, {"id": "sex-ratio", "value": 973}]}, {"id": "gujarat", "name": {"en": "Gujarat", "hi": "\u0917\u0941\u091c\u0930\u093e\u0924"}, "indicators": [{"id": "population", "value": 60439692}, {"id": "literacy-rate", "value": 78.03}, {"id": "gdp", "value": 2262000}, {"id": "sex-ratio", "value": 919}]}, {"id": "haryana", "name": {"en": "Haryana", "hi": "\u0939\u0930\u093f\u092f\u093e\u0923\u093e"}, "indicators": [{"id": "population", "value": 25351462}, {"id": "literacy-rate", "value": 75.55}, {"id": "gdp", "value": 994116}, {"id": "sex-ratio", "value": 879}]}, {"id": "himachal-pradesh", "name": {"en": "Himachal Pradesh", "hi": "\u0939\u093f\u092e\u093e\u091a\u0932 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 6864602}, {"id": "literacy-rate", "value": 82.8}, {"id": "gdp", "value": 191728}, {"id": "sex-ratio", "value": 972}]}, {"id": "jammu-kashmir", "name": {"en": "Jammu & Kashmir", "hi": "\u091c\u092e\u094d\u092e\u0942 \u0914\u0930 \u0915\u0936\u094d\u092e\u0940\u0930"}, "indicators": [{"id": "population", "value": 12267032}, {"id": "literacy-rate", "value": 67.16}, {"id": "gdp", "value": 224102}, {"id": "sex-ratio", "value": 889}]}, {"id": "jharkhand", "name": {"en": "Jharkhand", "hi": "\u091d\u093e\u0930\u0916\u0902\u0921"}, "indicators": [{"id": "population", "value": 32988134}, {"id": "literacy-rate", "value": 66.41}, {"id": "gdp", "value": 393722}, {"id": "sex-ratio", "value": 948}]}, {"id": "karnataka", "name": {"en": "Karnataka", "hi": "\u0915\u0930\u094d\u0928\u093e\u091f\u0915"}, "indicators": [{"id": "population", "value": 61095297}, {"id": "literacy-rate", "value": 75.36}, {"id": "gdp", "value": 2241368}, {"id": "sex-ratio", "value": 973}]}, {"id": "kerala", "name": {"en": "Kerala", "hi": "\u0915\u0947\u0930\u0932"}, "indicators": [{"id": "population", "value": 33406061}, {"id": "literacy-rate", "value": 94.0}, {"id": "gdp", "value": 1046188}, {"id": "sex-ratio", "value": 1084}]}, {"id": "ladakh", "name": {"en": "Ladakh", "hi": "\u0932\u0926\u094d\u0926\u093e\u0916"}, "indicators": [{"id": "population", "value": 274000}, {"id": "literacy-rate", "value": 74.27}, {"id": "gdp", "value": 4200}, {"id": "sex-ratio", "value": 853}]}, {"id": "lakshadweep", "name": {"en": "Lakshadweep", "hi": "\u0932\u0915\u094d\u0937\u0926\u094d\u0935\u0940\u092a"}, "indicators": [{"id": "population", "value": 64473}, {"id": "literacy-rate", "value": 91.85}, {"id": "gdp", "value": 850}, {"id": "sex-ratio", "value": 946}]}, {"id": "madhya-pradesh", "name": {"en": "Madhya Pradesh", "hi": "\u092e\u0927\u094d\u092f \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 72626809}, {"id": "literacy-rate", "value": 69.32}, {"id": "gdp", "value": 1322421}, {"id": "sex-ratio", "value": 931}]}, {"id": "maharashtra", "name": {"en": "Maharashtra", "hi": "\u092e\u0939\u093e\u0930\u093e\u0937\u094d\u091f\u094d\u0930"}, "indicators": [{"id": "population", "value": 112374333}, {"id": "literacy-rate", "value": 82.34}, {"id": "gdp", "value": 3527084}, {"id": "sex-ratio", "value": 929}]}, {"id": "manipur", "name": {"en": "Manipur", "hi": "\u092e\u0923\u093f\u092a\u0941\u0930"}, "indicators": [{"id": "population", "value": 2855794}, {"id": "literacy-rate", "value": 76.94}, {"id": "gdp", "value": 39340}, {"id": "sex-ratio", "value": 985}]}, {"id": "meghalaya", "name": {"en": "Meghalaya", "hi": "\u092e\u0947\u0918\u093e\u0932\u092f"}, "indicators": [{"id": "population", "value": 2966889}, {"id": "literacy-rate", "value": 74.43}, {"id": "gdp", "value": 42697}, {"id": "sex-ratio", "value": 989}]}, {"id": "mizoram", "name": {"en": "Mizoram", "hi": "\u092e\u093f\u091c\u093c\u094b\u0930\u092e"}, "indicators": [{"id": "population", "value": 1097206}, {"id": "literacy-rate", "value": 91.33}, {"id": "gdp", "value": 30500}, {"id": "sex-ratio", "value": 976}]}, {"id": "nagaland", "name": {"en": "Nagaland", "hi": "\u0928\u093e\u0917\u093e\u0932\u0948\u0902\u0921"}, "indicators": [{"id": "population", "value": 1978502}, {"id": "literacy-rate", "value": 79.55}, {"id": "gdp", "value": 35680}, {"id": "sex-ratio", "value": 931}]}, {"id": "odisha", "name": {"en": "Odisha", "hi": "\u0913\u0921\u093f\u0936\u093e"}, "indicators": [{"id": "population", "value": 41974218}, {"id": "literacy-rate", "value": 72.87}, {"id": "gdp", "value": 774869}, {"id": "sex-ratio", "value": 979}]}, {"id": "puducherry", "name": {"en": "Puducherry", "hi": "\u092a\u0941\u0921\u0941\u091a\u0947\u0930\u0940"}, "indicators": [{"id": "population", "value": 1247953}, {"id": "literacy-rate", "value": 85.85}, {"id": "gdp", "value": 39019}, {"id": "sex-ratio", "value": 1037}]}, {"id": "punjab", "name": {"en": "Punjab", "hi": "\u092a\u0902\u091c\u093e\u092c"}, "indicators": [{"id": "population", "value": 27743338}, {"id": "literacy-rate", "value": 75.84}, {"id": "gdp", "value": 637000}, {"id": "sex-ratio", "value": 895}]}, {"id": "rajasthan", "name": {"en": "Rajasthan", "hi": "\u0930\u093e\u091c\u0938\u094d\u0925\u093e\u0928"}, "indicators": [{"id": "population", "value": 68548437}, {"id": "literacy-rate", "value": 66.11}, {"id": "gdp", "value": 1414000}, {"id": "sex-ratio", "value": 928}]}, {"id": "sikkim", "name": {"en": "Sikkim", "hi": "\u0938\u093f\u0915\u094d\u0915\u093f\u092e"}, "indicators": [{"id": "population", "value": 610577}, {"id": "literacy-rate", "value": 81.42}, {"id": "gdp", "value": 42754}, {"id": "sex-ratio", "value": 890}]}, {"id": "tamil-nadu", "name": {"en": "Tamil Nadu", "hi": "\u0924\u092e\u093f\u0932\u0928\u093e\u0921\u0941"}, "indicators": [{"id": "population", "value": 72147030}, {"id": "literacy-rate", "value": 80.09}, {"id": "gdp", "value": 2364514}, {"id": "sex-ratio", "value": 996}]}, {"id": "telangana", "name": {"en": "Telangana", "hi": "\u0924\u0947\u0932\u0902\u0917\u093e\u0928\u093e"}, "indicators": [{"id": "population", "value": 35003674}, {"id": "literacy-rate", "value": 66.54}, {"id": "gdp", "value": 1302371}, {"id": "sex-ratio", "value": 988}]}, {"id": "tripura", "name": {"en": "Tripura", "hi": "\u0924\u094d\u0930\u093f\u092a\u0941\u0930\u093e"}, "indicators": [{"id": "population", "value": 3673917}, {"id": "literacy-rate", "value": 87.22}, {"id": "gdp", "value": 64000}, {"id": "sex-ratio", "value": 960}]}, {"id": "uttar-pradesh", "name": {"en": "Uttar Pradesh", "hi": "\u0909\u0924\u094d\u0924\u0930 \u092a\u094d\u0930\u0926\u0947\u0936"}, "indicators": [{"id": "population", "value": 199812341}, {"id": "literacy-rate", "value": 67.68}, {"id": "gdp", "value": 2258040}, {"id": "sex-ratio", "value": 912}]}, {"id": "uttarakhand", "name": {"en": "Uttarakhand", "hi": "\u0909\u0924\u094d\u0924\u0930\u093e\u0916\u0902\u0921"}, "indicators": [{"id": "population", "value": 10086292}, {"id": "literacy-rate", "value": 78.82}, {"id": "gdp", "value": 302621}, {"id": "sex-ratio", "value": 963}]}, {"id": "west-bengal", "name": {"en": "West Bengal", "hi": "\u092a\u0936\u094d\u091a\u093f\u092e \u092c\u0902\u0917\u093e\u0932"}, "indicators": [{"id": "population", "value": 91276115}, {"id": "literacy-rate", "value": 76.26}, {"id": "gdp", "value": 1530000}, {"id": "sex-ratio", "value": 950}]}];

  function loadStates(data) {
    statesData = data || [];
    initDropdown();
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
      console.warn("Using offline fallback data for economic tool:", err);
      loadStates(FALLBACK_EXPLORER_STATES);
    });

  function initDropdown() {
    stateSelect.innerHTML = '';
    statesData.forEach(state => {
      const opt = document.createElement('option');
      opt.value = state.id;
      opt.textContent = `${state.name.en} (${state.name.hi})`;
      stateSelect.appendChild(opt);
    });
  }

  function readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const sParam = params.get('state');
    const gParam = params.get('growth');

    if (sParam && statesData.some(s => s.id === sParam)) {
      stateSelect.value = sParam;
    } else if (statesData.some(s => s.id === 'maharashtra')) {
      stateSelect.value = 'maharashtra';
    }

    if (gParam && !isNaN(parseFloat(gParam))) {
      const gVal = Math.min(15, Math.max(3, parseFloat(gParam)));
      growthInput.value = gVal;
      growthSlider.value = gVal;
      growthDisplay.textContent = `${gVal}%`;
    }
  }

  function syncGrowth(val) {
    growthInput.value = val;
    growthSlider.value = val;
    growthDisplay.textContent = `${val}%`;
    calculate();
  }

  if (growthSlider && growthInput) {
    growthSlider.addEventListener('input', (e) => syncGrowth(e.target.value));
    growthInput.addEventListener('input', (e) => syncGrowth(e.target.value));
  }

  if (stateSelect) {
    stateSelect.addEventListener('change', () => {
      calculate();
      updateUrl();
    });
  }

  function updateUrl() {
    const sVal = stateSelect.value;
    const gVal = growthInput.value;
    const newUrl = `${window.location.pathname}?state=${sVal}&growth=${gVal}`;
    window.history.replaceState(null, '', newUrl);
  }

  function findClosestCountry(gdpUsd) {
    let closest = countryEquivalents[0];
    let minDiff = Math.abs(closest.gdp_usd - gdpUsd);

    for (const c of countryEquivalents) {
      const diff = Math.abs(c.gdp_usd - gdpUsd);
      if (diff < minDiff) {
        minDiff = diff;
        closest = c;
      }
    }
    return closest;
  }

  function calculate() {
    const stateId = stateSelect.value;
    const state = statesData.find(s => s.id === stateId);
    if (!state) return;

    const growthRate = parseFloat(growthInput.value) || 8.0;

    // Get indicators
    const gdpInd = state.indicators.find(i => i.id === 'gdp');
    const popInd = state.indicators.find(i => i.id === 'population');
    const litInd = state.indicators.find(i => i.id === 'literacy-rate');

    const gsdpCr = gdpInd ? gdpInd.value : 0;
    const population = popInd ? popInd.value : 1;
    const gsdpUsdBillion = (gsdpCr * 1e7) / (USD_INR_RATE * 1e9);

    const perCapitaInr = Math.round((gsdpCr * 1e7) / population);
    const perCapitaUsd = Math.round(perCapitaInr / USD_INR_RATE);
    const nationalShare = ((gsdpCr / INDIA_TOTAL_GDP_CR) * 100).toFixed(2);

    // Closest Country
    const country = findClosestCountry(gsdpUsdBillion);

    // Rule of 72 Doubling Time
    const doublingYears = (72 / growthRate).toFixed(1);

    const isHi = document.documentElement.getAttribute('data-lang') === 'hi' || document.documentElement.lang === 'hi';
    const stateName = isHi ? (state.name.hi || state.name.en) : state.name.en;

    // Update DOM
    const stateNameEl = document.getElementById('res-state-name');
    if (stateNameEl) stateNameEl.textContent = stateName;

    document.getElementById('res-gsdp-inr').textContent = isHi ? (gdpInd?.display?.hi || `₹${(gsdpCr/100000).toFixed(2)} लाख करोड़`) : (gdpInd?.display?.en || `₹${(gsdpCr/100000).toFixed(2)} Lakh Cr`);
    document.getElementById('res-gsdp-usd').textContent = isHi ? `$${gsdpUsdBillion.toFixed(1)} बिलियन` : `$${gsdpUsdBillion.toFixed(1)} Billion`;
    
    document.getElementById('res-country-name').textContent = `${country.flag} ${country.country}`;
    document.getElementById('res-country-gdp').textContent = isHi ? `$${country.gdp_usd} बिलियन (नॉमिनल GDP)` : `$${country.gdp_usd} Billion (Nominal GDP)`;
    
    document.getElementById('res-per-capita').textContent = `₹${perCapitaInr.toLocaleString('en-IN')} ($${perCapitaUsd.toLocaleString()})`;
    document.getElementById('res-national-share').textContent = `${nationalShare}%`;
    document.getElementById('res-doubling-time').textContent = isHi ? `${doublingYears} वर्ष` : `${doublingYears} years`;

    // Target Projections ($250B, $500B, $1 Trillion)
    const baseYear = 2023;
    const targets = [
      { label: "$250 Billion", labelHi: "$250 बिलियन", val: 250 },
      { label: "$500 Billion", labelHi: "$500 बिलियन", val: 500 },
      { label: "$1 Trillion ($1,000B)", labelHi: "$1 ट्रिलियन ($1,000B)", val: 1000 }
    ];

    const projContainer = document.getElementById('milestone-projections');
    if (projContainer) {
      projContainer.innerHTML = targets.map(t => {
        const curTargetLabel = isHi ? t.labelHi : t.label;
        if (gsdpUsdBillion >= t.val) {
          return `
            <div style="background:rgba(45, 212, 191, 0.08); border:1px solid rgba(45, 212, 191, 0.3); border-radius:8px; padding:12px; text-align:center;">
              <div style="font-size:12px; color:var(--teal); font-weight:600;">${curTargetLabel}</div>
              <div style="font-family:var(--font-mono); font-size:18px; font-weight:700; color:var(--teal); margin-top:4px;">${isHi ? "प्राप्त ✅" : "ACHIEVED ✅"}</div>
              <div style="font-size:11px; color:var(--text-faint); margin-top:2px;">${isHi ? `वर्तमान में $${gsdpUsdBillion.toFixed(1)}B` : `Currently $${gsdpUsdBillion.toFixed(1)}B`}</div>
            </div>
          `;
        }
        // t.val = gsdpUsdBillion * (1 + r)^n => n = ln(t.val / gsdpUsdBillion) / ln(1 + r)
        const r = growthRate / 100;
        const yearsNeeded = Math.log(t.val / gsdpUsdBillion) / Math.log(1 + r);
        const targetYear = Math.round(baseYear + yearsNeeded);
        return `
          <div style="background:var(--surface-2); border:1px solid var(--border); border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:12px; color:var(--text-muted); font-weight:600;">${curTargetLabel}</div>
            <div style="font-family:var(--font-mono); font-size:20px; font-weight:700; color:var(--text); margin-top:4px;">~${targetYear}</div>
            <div style="font-size:11px; color:var(--text-faint); margin-top:2px;">${isHi ? `${growthRate}%/वर्ष पर ~${Math.ceil(yearsNeeded)} वर्षों में` : `In ~${Math.ceil(yearsNeeded)} years at ${growthRate}%/yr`}</div>
          </div>
        `;
      }).join('');
    }

    // Update Quick Links
    const stateLink = document.getElementById('view-state-link');
    if (stateLink) stateLink.href = `../states/${state.id}.html`;
    const compareLink = document.getElementById('compare-state-link');
    if (compareLink) compareLink.href = `../compare.html?s1=${state.id}`;
  }

  document.querySelectorAll("[data-set-lang]").forEach(btn => {
    btn.addEventListener("click", () => {
      setTimeout(calculate, 50);
    });
  });
});

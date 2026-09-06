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

  fetch('../data/explorer.json')
    .then(res => res.json())
    .then(data => {
      statesData = data.states || [];
      initDropdown();
      readUrlParams();
      calculate();
    })
    .catch(err => console.error("Error loading explorer data:", err));

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

    // Update DOM
    document.getElementById('res-state-name').textContent = state.name.en;
    document.getElementById('res-gsdp-inr').textContent = gdpInd?.display?.en || `₹${(gsdpCr/100000).toFixed(2)} Lakh Cr`;
    document.getElementById('res-gsdp-usd').textContent = `$${gsdpUsdBillion.toFixed(1)} Billion`;
    
    document.getElementById('res-country-name').textContent = `${country.flag} ${country.country}`;
    document.getElementById('res-country-gdp').textContent = `$${country.gdp_usd} Billion (Nominal GDP)`;
    
    document.getElementById('res-per-capita').textContent = `₹${perCapitaInr.toLocaleString('en-IN')} ($${perCapitaUsd.toLocaleString()})`;
    document.getElementById('res-national-share').textContent = `${nationalShare}%`;
    document.getElementById('res-doubling-time').textContent = `${doublingYears} years`;

    // Target Projections ($250B, $500B, $1 Trillion)
    const baseYear = 2023;
    const targets = [
      { label: "$250 Billion", val: 250 },
      { label: "$500 Billion", val: 500 },
      { label: "$1 Trillion ($1,000B)", val: 1000 }
    ];

    const projContainer = document.getElementById('milestone-projections');
    if (projContainer) {
      projContainer.innerHTML = targets.map(t => {
        if (gsdpUsdBillion >= t.val) {
          return `
            <div style="background:rgba(45, 212, 191, 0.08); border:1px solid rgba(45, 212, 191, 0.3); border-radius:8px; padding:12px; text-align:center;">
              <div style="font-size:12px; color:var(--teal); font-weight:600;">${t.label}</div>
              <div style="font-family:var(--font-mono); font-size:18px; font-weight:700; color:var(--teal); margin-top:4px;">ACHIEVED ✅</div>
              <div style="font-size:11px; color:var(--text-faint); margin-top:2px;">Currently $${gsdpUsdBillion.toFixed(1)}B</div>
            </div>
          `;
        }
        // t.val = gsdpUsdBillion * (1 + r)^n => n = ln(t.val / gsdpUsdBillion) / ln(1 + r)
        const r = growthRate / 100;
        const yearsNeeded = Math.log(t.val / gsdpUsdBillion) / Math.log(1 + r);
        const targetYear = Math.round(baseYear + yearsNeeded);
        return `
          <div style="background:var(--surface-2); border:1px solid var(--border); border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:12px; color:var(--text-muted); font-weight:600;">${t.label}</div>
            <div style="font-family:var(--font-mono); font-size:20px; font-weight:700; color:var(--text); margin-top:4px;">~${targetYear}</div>
            <div style="font-size:11px; color:var(--text-faint); margin-top:2px;">In ~${Math.ceil(yearsNeeded)} years at ${growthRate}%/yr</div>
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
});

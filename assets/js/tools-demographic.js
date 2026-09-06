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

  fetch('../data/explorer.json')
    .then(res => res.json())
    .then(data => {
      statesData = data.states || [];
      initDropdowns();
      readUrlParams();
      calculate();
    })
    .catch(err => console.error("Error loading explorer data for demographic tool:", err));

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

    // 2. State-to-State Catch-up
    const gapBetweenStates = (lit2 - lit1).toFixed(2);
    let catchupText = "";
    if (lit1 >= lit2) {
      catchupText = `Already leads ${s2.name.en} by ${Math.abs(gapBetweenStates)}% ✅`;
    } else {
      const yearsCatchup = Math.ceil(Math.abs(gapBetweenStates) / annualGain);
      catchupText = `~${yearsCatchup} years to match ${s2.name.en}'s ${lit2}% (by ~${currentBaseYear + yearsCatchup})`;
    }

    // 3. Gender / Sex Ratio Analysis
    const naturalBenchmark = 950; // Females per 1000 males
    const sexDiff = sex1 - naturalBenchmark;
    let sexStatus = "";
    if (sexDiff >= 0) {
      sexStatus = `Favorable (+${sexDiff} above 950 benchmark)`;
    } else {
      sexStatus = `Deficit (${Math.abs(sexDiff)} below 950 benchmark)`;
    }

    // Update DOM
    document.getElementById('res-s1-name').textContent = s1.name.en;
    document.getElementById('res-current-lit').textContent = `${lit1}%`;
    document.getElementById('res-lit-gap').textContent = `${gapToUniversal}%`;
    document.getElementById('res-universal-year').textContent = `~${targetUniversalYear}`;
    document.getElementById('res-years-to-100').textContent = `${yearsToUniversal} years required at +${annualGain}%/yr`;

    document.getElementById('res-benchmark-name').textContent = s2.name.en;
    document.getElementById('res-benchmark-gap').textContent = `${gapBetweenStates > 0 ? '+' : ''}${gapBetweenStates}%`;
    document.getElementById('res-catchup-pace').textContent = catchupText;

    document.getElementById('res-sex-ratio').textContent = `${sex1}`;
    document.getElementById('res-sex-status').textContent = sexStatus;

    // Progress Bar Visualizer
    const bar = document.getElementById('lit-progress-bar');
    if (bar) {
      bar.style.width = `${Math.min(100, lit1)}%`;
      document.getElementById('bar-label').textContent = `${s1.name.en}: ${lit1}%`;
    }

    // Quick links
    const linkS1 = document.getElementById('link-s1-profile');
    if (linkS1) linkS1.href = `../states/${s1.id}.html`;
    const linkCompare = document.getElementById('link-compare-states');
    if (linkCompare) linkCompare.href = `../compare.html?s1=${s1.id}&s2=${s2.id}`;
  }
});

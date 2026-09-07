(function () {
  "use strict";

  var grid = document.getElementById("overview-grid");
  var errorEl = document.getElementById("overview-error");
  if (!grid) return;

  function currentLang() {
    return document.documentElement.getAttribute("data-lang") === "hi" ? "hi" : "en";
  }

  // Note: Overview cards are now pre-rendered into HTML by scripts/build.py for SEO.
  // Language switching for the cards is handled automatically by main.js via data-en and data-hi attributes.
  
  // Re-render chart on language switch
  document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (window.__indiaHistoryData) renderChart(window.__indiaHistoryData);
    });
  });

  // Load and render history chart
  var trendChartInstance = null;
  function renderChart(historyData) {
    var lang = currentLang();
    var ctx = document.getElementById('trendChart');
    if (!ctx) return;
    
    var titleEl = document.getElementById('chart-title');
    var sourceEl = document.getElementById('chart-source');
    if (titleEl) titleEl.innerText = historyData.name[lang] || historyData.name.en;
    if (sourceEl) {
      var sourceLabel = lang === "hi" ? "स्रोत" : "Source";
      sourceEl.innerHTML = '<a href="' + historyData.source_url + '" target="_blank" rel="noopener" style="color:var(--teal);">' + sourceLabel + ': ' + sourceName(historyData.source_id) + ' →</a>';
    }

    var labels = historyData.history.map(function(item) { return item.year; });
    var dataPoints = historyData.history.map(function(item) { return item.value; });

    if (trendChartInstance) {
      trendChartInstance.destroy();
    }

    trendChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: lang === 'hi' ? 'जनसंख्या' : 'Population',
          data: dataPoints,
          borderColor: '#E68332', // saffron
          backgroundColor: 'rgba(230, 131, 50, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { color: document.documentElement.getAttribute('data-theme') === 'light' ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)' },
            ticks: { color: document.documentElement.getAttribute('data-theme') === 'light' ? '#334155' : '#94a3b8' }
          },
          y: {
            beginAtZero: false,
            grid: { color: document.documentElement.getAttribute('data-theme') === 'light' ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)' },
            ticks: {
              color: document.documentElement.getAttribute('data-theme') === 'light' ? '#334155' : '#94a3b8',
              callback: function(value) {
                return (value / 1000000000).toFixed(2) + 'B';
              }
            }
          }
        }
      }
    });
  }

  var FALLBACK_INDIA_HISTORY = {
  "_readme": "Historical trend for India's Population. Data from World Bank.",
  "indicator_id": "population",
  "name": { "en": "Population Trend", "hi": "जनसंख्या का रुझान" },
  "source_id": "world-bank",
  "source_url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=IN",
  "history": [
    { "year": 2014, "value": 1307246509, "display": { "en": "1.31 billion", "hi": "1.31 अरब" } },
    { "year": 2015, "value": 1322866505, "display": { "en": "1.32 billion", "hi": "1.32 अरब" } },
    { "year": 2016, "value": 1338636340, "display": { "en": "1.34 billion", "hi": "1.34 अरब" } },
    { "year": 2017, "value": 1354195680, "display": { "en": "1.35 billion", "hi": "1.35 अरब" } },
    { "year": 2018, "value": 1369003306, "display": { "en": "1.37 billion", "hi": "1.37 अरब" } },
    { "year": 2019, "value": 1383112050, "display": { "en": "1.38 billion", "hi": "1.38 अरब" } },
    { "year": 2020, "value": 1396814904, "display": { "en": "1.40 billion", "hi": "1.40 अरब" } },
    { "year": 2021, "value": 1407563842, "display": { "en": "1.41 billion", "hi": "1.41 अरब" } },
    { "year": 2022, "value": 1417173173, "display": { "en": "1.42 billion", "hi": "1.42 अरब" } },
    { "year": 2023, "value": 1428627663, "display": { "en": "1.43 billion", "hi": "1.43 अरब" } },
    { "year": 2024, "value": 1450935791, "display": { "en": "1.45 billion", "hi": "1.45 अरब" } }
  ]
};

  function loadHistory(data) {
    window.__indiaHistoryData = data;
    renderChart(data);
  }

  fetch("data/indicators/india-population-history.json")
    .then(function (res) {
      if (res.ok) return res.json();
      throw new Error("Could not load history");
    })
    .then(function (data) {
      loadHistory(data);
    })
    .catch(function (e) {
      console.warn("Using offline fallback for India population history:", e);
      loadHistory(FALLBACK_INDIA_HISTORY);
    });
})
  document.querySelectorAll('.theme-toggle-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      setTimeout(function() {
        if (window.__indiaHistoryData) renderChart(window.__indiaHistoryData);
      }, 60);
    });
  });
})();

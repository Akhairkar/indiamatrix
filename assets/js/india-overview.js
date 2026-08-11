(function () {
  "use strict";

  var grid = document.getElementById("overview-grid");
  var errorEl = document.getElementById("overview-error");
  if (!grid) return;

  function currentLang() {
    return document.documentElement.getAttribute("data-lang") === "hi" ? "hi" : "en";
  }

  function renderCards(indicators) {
    var lang = currentLang();
    grid.innerHTML = indicators.map(function (ind) {
      var name = ind.name[lang] || ind.name.en;
      var display = ind.display[lang] || ind.display.en;
      var yearLabel = lang === "hi" ? "डेटा वर्ष" : "Data year";
      var sourceLabel = lang === "hi" ? "स्रोत" : "Source";
      return (
        '<article class="glance-card" data-indicator-id="' + ind.id + '">' +
          '<h3>' + name + '</h3>' +
          '<p class="glance-value" style="color:var(--text); font-size:22px; font-family:var(--font-mono); font-weight:600; margin-bottom:10px;">' + display + '</p>' +
          '<p style="font-size:12px; color:var(--text-faint); margin:0 0 4px; font-family:var(--font-mono);">' + yearLabel + ': ' + ind.year + '</p>' +
          '<a href="' + ind.source_url + '" target="_blank" rel="noopener" style="font-size:12px; color:var(--teal); font-family:var(--font-mono);">' + sourceLabel + ': ' + sourceName(ind.source_id) + ' →</a>' +
        '</article>'
      );
    }).join("");
  }

  var sourceNames = {
    "world-bank": "World Bank",
    "census-india": "Census of India",
    "mospi": "MoSPI (PLFS)",
    "rbi": "RBI",
    "niti-aayog": "NITI Aayog",
    "data-gov-in": "data.gov.in",
    "moh-family-welfare": "MoHFW",
    "ncrb": "NCRB",
    "moef-cc": "MoEFCC",
    "meity": "MeitY",
    "un-data": "UN Data"
  };
  function sourceName(id) { return sourceNames[id] || id; }

  fetch("data/indicators/india-overview.json")
    .then(function (res) {
      if (!res.ok) throw new Error("Network response was not ok");
      return res.json();
    })
    .then(function (data) {
      window.__indiaOverviewData = data.indicators;
      renderCards(data.indicators);

      // Re-render on language switch
      document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          if (window.__indiaOverviewData) renderCards(window.__indiaOverviewData);
          if (window.__indiaHistoryData) renderChart(window.__indiaHistoryData);
        });
      });
    })
    .catch(function () {
      if (errorEl) errorEl.style.display = "block";
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
          y: {
            beginAtZero: false,
            ticks: {
              callback: function(value) {
                return (value / 1000000000).toFixed(2) + 'B';
              }
            }
          }
        }
      }
    });
  }

  fetch("data/indicators/india-population-history.json")
    .then(function (res) {
      if (res.ok) return res.json();
      throw new Error("Could not load history");
    })
    .then(function (data) {
      window.__indiaHistoryData = data;
      renderChart(data);
    })
    .catch(function (e) {
      console.error(e);
    });
})();

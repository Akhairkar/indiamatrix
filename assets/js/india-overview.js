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

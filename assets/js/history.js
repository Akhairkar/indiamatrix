document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("history-charts-container");
  if (!container) return;

  const FALLBACK_HISTORY = {
    "population": {
      "title": "Population (in billions)",
      "source": "World Bank",
      "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2023"],
      "values": [0.45, 0.55, 0.7, 0.87, 1.05, 1.23, 1.39, 1.43]
    },
    "gdp": {
      "title": "GDP (Current USD, Billions)",
      "source": "World Bank",
      "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2023"],
      "values": [37, 62, 186, 320, 468, 1675, 2667, 3549]
    },
    "life_expectancy": {
      "title": "Life Expectancy at Birth (Years)",
      "source": "World Bank",
      "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2022"],
      "values": [45.2, 48.7, 53.8, 58.6, 62.5, 66.8, 70.1, 72.0]
    },
    "literacy_rate": {
      "title": "Literacy Rate (%)",
      "source": "Census of India",
      "labels": ["1951", "1961", "1971", "1981", "1991", "2001", "2011"],
      "values": [18.33, 28.3, 34.45, 43.57, 52.21, 64.83, 74.04]
    },
    "internet_penetration": {
      "title": "Internet Penetration (% of Population)",
      "source": "TRAI / ITU / World Bank",
      "labels": ["2010", "2014", "2016", "2018", "2020", "2022", "2024"],
      "values": [7.5, 13.5, 22.0, 34.4, 43.0, 48.7, 55.2]
    }
  };

  function renderCharts(data) {
    container.innerHTML = "";
    const isLight = document.documentElement.getAttribute("data-theme") === "light" ||
      (!document.documentElement.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: light)").matches);

    const gridColor = isLight ? "rgba(16, 24, 43, 0.08)" : "rgba(255, 255, 255, 0.08)";
    const tickColor = isLight ? "#475569" : "#94a3b8";

    Object.keys(data).forEach((key) => {
      const item = data[key];
      const vals = item.values || [];
      const firstVal = vals[0] || 1;
      const latestVal = vals[vals.length - 1] || 0;
      const totalGrowthPct = (((latestVal - firstVal) / firstVal) * 100).toFixed(1);

      // Create wrapper
      const wrapper = document.createElement("div");
      wrapper.style.background = "var(--panel-bg)";
      wrapper.style.border = "1px solid var(--border)";
      wrapper.style.borderRadius = "14px";
      wrapper.style.padding = "26px";
      wrapper.style.boxShadow = "var(--shadow-card)";

      // Header row with Title and Growth Pill
      const headRow = document.createElement("div");
      headRow.style.display = "flex";
      headRow.style.justifyContent = "space-between";
      headRow.style.alignItems = "flex-start";
      headRow.style.flexWrap = "wrap";
      headRow.style.gap = "12px";
      headRow.style.marginBottom = "14px";

      const titleWrap = document.createElement("div");
      const title = document.createElement("h3");
      title.style.margin = "0 0 4px";
      title.style.color = "var(--text)";
      title.style.fontSize = "19px";
      title.textContent = item.title;
      titleWrap.appendChild(title);

      const source = document.createElement("p");
      source.style.fontSize = "12px";
      source.style.color = "var(--text-faint)";
      source.style.margin = "0";
      source.style.fontFamily = "var(--font-mono)";
      source.textContent = `Accredited Source: ${item.source}`;
      titleWrap.appendChild(source);

      headRow.appendChild(titleWrap);

      // Stat Badge
      const badge = document.createElement("div");
      badge.style.background = isLight ? "rgba(13, 148, 136, 0.1)" : "rgba(43, 183, 160, 0.15)";
      badge.style.border = "1px solid var(--teal)";
      badge.style.borderRadius = "6px";
      badge.style.padding = "6px 12px";
      badge.style.textAlign = "right";
      badge.innerHTML = `
        <span style="font-size:11px; font-family:var(--font-mono); color:var(--text-faint); display:block; text-transform:uppercase;">Historical Growth</span>
        <span style="font-size:15px; font-weight:700; font-family:var(--font-mono); color:var(--teal);">${totalGrowthPct >= 0 ? '+' : ''}${totalGrowthPct}%</span>
      `;
      headRow.appendChild(badge);
      wrapper.appendChild(headRow);

      // Canvas container
      const canvasContainer = document.createElement("div");
      canvasContainer.style.position = "relative";
      canvasContainer.style.height = "320px";
      canvasContainer.style.width = "100%";

      const canvas = document.createElement("canvas");
      canvasContainer.appendChild(canvas);
      wrapper.appendChild(canvasContainer);
      container.appendChild(wrapper);

      function formatHistoryVal(v) {
        if (key === 'population') return `${v} Billion citizens`;
        if (key === 'gdp') return `$${v.toLocaleString()} Billion (${(v/1000).toFixed(2)}T USD)`;
        if (key === 'life_expectancy') return `${v} Years at birth`;
        if (key === 'literacy_rate') return `${v}% Literacy`;
        if (key === 'internet_penetration') return `${v}% Internet Users`;
        return v.toLocaleString();
      }

      if (typeof Chart !== "undefined") {
        new Chart(canvas, {
          type: "line",
          data: {
            labels: item.labels,
            datasets: [
              {
                label: item.title,
                data: item.values,
                borderColor: "#FF9933", // Saffron
                backgroundColor: "rgba(255, 153, 51, 0.12)",
                borderWidth: 3,
                pointBackgroundColor: "#138808", // Green
                pointBorderColor: "#FFFFFF",
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 9,
                fill: true,
                tension: 0.35,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: isLight ? "#FFFFFF" : "#10182B",
                titleColor: isLight ? "#10182B" : "#E8ECF8",
                bodyColor: isLight ? "#10182B" : "#E8ECF8",
                borderColor: isLight ? "rgba(16, 24, 43, 0.18)" : "rgba(43, 183, 160, 0.35)",
                borderWidth: 1.5,
                padding: 14,
                cornerRadius: 8,
                titleFont: { family: "Inter", size: 14, weight: "700" },
                bodyFont: { family: "JetBrains Mono", size: 12.5 },
                callbacks: {
                  title: function(items) {
                    return `Year ${items[0].label} • National Benchmark`;
                  },
                  label: function(ctx) {
                    const val = ctx.raw;
                    const lines = [`• Recorded: ${formatHistoryVal(val)}`];
                    if (ctx.dataIndex > 0) {
                      const prev = item.values[ctx.dataIndex - 1];
                      const diff = val - prev;
                      const pct = (((diff) / prev) * 100).toFixed(1);
                      lines.push(`• Period Growth: ${diff >= 0 ? '+' : ''}${pct}% since previous milestone`);
                    }
                    return lines;
                  }
                }
              },
            },
            scales: {
              x: {
                grid: { color: gridColor },
                ticks: { color: tickColor, font: { family: "JetBrains Mono", size: 11.5 } },
              },
              y: {
                grid: { color: gridColor },
                ticks: {
                  color: tickColor,
                  font: { family: "JetBrains Mono", size: 11 },
                  callback: function(v) {
                    if (key === 'gdp') {
                      if (v >= 1000) return '$' + (v/1000).toFixed(1) + 'T';
                      return '$' + v + 'B';
                    }
                    if (key === 'population') return v + 'B';
                    if (key === 'literacy_rate' || key === 'internet_penetration') return v + '%';
                    return v;
                  }
                },
              },
            },
          },
        });
      }
    });
  }

  // Try fetch first, fall back to embedded data immediately if fetch fails (e.g. file:/// or offline)
  fetch("data/history.json")
    .then((response) => {
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return response.json();
    })
    .then((data) => {
      renderCharts(data);
    })
    .catch((error) => {
      console.warn("Using offline fallback history data:", error);
      renderCharts(FALLBACK_HISTORY);
    });
});

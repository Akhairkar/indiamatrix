document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("world-charts-container");
  if (!container) return;

  const FALLBACK_WORLD = {
    "comparisons": [
      {
        "id": "gdp",
        "name": "GDP (Trillion USD)",
        "source": "World Bank, 2025",
        "india": 3.96,
        "china": 17.7,
        "usa": 27.3,
        "world": 105.4
      },
      {
        "id": "population",
        "name": "Population (Billions)",
        "source": "World Bank, 2023",
        "india": 1.43,
        "china": 1.41,
        "usa": 0.33,
        "world": 8.02
      },
      {
        "id": "life_expectancy",
        "name": "Life Expectancy (Years)",
        "source": "World Bank, 2022",
        "india": 72.0,
        "china": 78.2,
        "usa": 76.3,
        "world": 71.3
      },
      {
        "id": "gdp_per_capita",
        "name": "GDP per Capita (USD)",
        "source": "World Bank, 2023",
        "india": 2500,
        "china": 12500,
        "usa": 80000,
        "world": 13000
      },
      {
        "id": "literacy_rate",
        "name": "Literacy Rate (%)",
        "source": "World Bank / UNESCO",
        "india": 76.3,
        "china": 99.8,
        "usa": 99.0,
        "world": 86.3
      },
      {
        "id": "internet_penetration",
        "name": "Internet Penetration (%)",
        "source": "ITU, 2023",
        "india": 52.0,
        "china": 74.4,
        "usa": 91.8,
        "world": 67.0
      },
      {
        "id": "poverty_headcount",
        "name": "Poverty Headcount Ratio at $2.15 a day (%)",
        "source": "World Bank, 2021",
        "india": 12.9,
        "china": 0.1,
        "usa": 1.2,
        "world": 8.5
      },
      {
        "id": "health_expenditure",
        "name": "Current Health Expenditure (% of GDP)",
        "source": "World Bank, 2021",
        "india": 3.3,
        "china": 5.4,
        "usa": 17.4,
        "world": 9.8
      }
    ]
  };

  function renderWorldCharts(data) {
    container.innerHTML = "";
    const isLight = document.documentElement.getAttribute("data-theme") === "light" ||
      (!document.documentElement.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: light)").matches);

    const gridColor = isLight ? "rgba(16, 24, 43, 0.08)" : "rgba(255, 255, 255, 0.08)";
    const tickColor = isLight ? "#475569" : "#94a3b8";

    (data.comparisons || []).forEach((item) => {
      // Create wrapper
      const wrapper = document.createElement("div");
      wrapper.style.background = "var(--panel-bg)";
      wrapper.style.border = "1px solid var(--border)";
      wrapper.style.borderRadius = "14px";
      wrapper.style.padding = "26px";
      wrapper.style.boxShadow = "var(--shadow-card)";

      // Header row
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
      title.textContent = item.name;
      titleWrap.appendChild(title);

      const source = document.createElement("p");
      source.style.fontSize = "12px";
      source.style.color = "var(--text-faint)";
      source.style.margin = "0";
      source.style.fontFamily = "var(--font-mono)";
      source.textContent = `Accredited Source: ${item.source}`;
      titleWrap.appendChild(source);

      headRow.appendChild(titleWrap);

      // India Metric Pill
      const pill = document.createElement("div");
      pill.style.background = isLight ? "rgba(217, 119, 6, 0.1)" : "rgba(242, 169, 59, 0.15)";
      pill.style.border = "1px solid var(--saffron)";
      pill.style.borderRadius = "6px";
      pill.style.padding = "6px 12px";
      pill.style.textAlign = "right";
      pill.innerHTML = `
        <span style="font-size:11px; font-family:var(--font-mono); color:var(--text-faint); display:block; text-transform:uppercase;">India Benchmark</span>
        <span style="font-size:15px; font-weight:700; font-family:var(--font-mono); color:var(--saffron);">${item.india.toLocaleString()}</span>
      `;
      headRow.appendChild(pill);
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

      // Render bar chart
      if (typeof Chart !== "undefined") {
        new Chart(canvas, {
          type: "bar",
          data: {
            labels: ["India 🇮🇳", "China 🇨🇳", "USA 🇺🇸", "World Avg 🌐"],
            datasets: [
              {
                label: item.name,
                data: [item.india, item.china, item.usa, item.world],
                backgroundColor: [
                  "#F2A93B", // India (Saffron)
                  "#E3000F", // China (Red)
                  "#2563EB", // USA (Blue)
                  "#64748B", // World (Gray)
                ],
                borderRadius: 6,
                maxBarThickness: 48
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
                    return items[0].label;
                  },
                  label: function(ctx) {
                    const val = ctx.raw;
                    return `• ${item.name}: ${val.toLocaleString()}`;
                  },
                  afterLabel: function(ctx) {
                    const idx = ctx.dataIndex;
                    if (idx === 0) { // India
                      const diffChina = (((item.india - item.china) / (item.china || 1)) * 100).toFixed(1);
                      const diffWorld = (((item.india - item.world) / (item.world || 1)) * 100).toFixed(1);
                      return `• vs China: ${diffChina >= 0 ? '+' : ''}${diffChina}%\n• vs World Avg: ${diffWorld >= 0 ? '+' : ''}${diffWorld}%`;
                    } else if (idx === 1) { // China
                      const diff = (((item.china - item.india) / (item.india || 1)) * 100).toFixed(1);
                      return `• vs India: ${diff >= 0 ? '+' : ''}${diff}%`;
                    } else if (idx === 2) { // USA
                      const diff = (((item.usa - item.india) / (item.india || 1)) * 100).toFixed(1);
                      return `• vs India: ${diff >= 0 ? '+' : ''}${diff}%`;
                    }
                    return '';
                  }
                }
              },
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: tickColor, font: { family: "Inter", weight: "600", size: 13 } },
              },
              y: {
                grid: { color: gridColor },
                ticks: { color: tickColor, font: { family: "JetBrains Mono", size: 11 } },
              },
            },
          },
        });
      }
    });
  }

  fetch("data/world.json")
    .then((response) => {
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return response.json();
    })
    .then((data) => {
      renderWorldCharts(data);
    })
    .catch((error) => {
      console.warn("Using offline fallback world data:", error);
      renderWorldCharts(FALLBACK_WORLD);
    });
});

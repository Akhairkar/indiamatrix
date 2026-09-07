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
      wrapper.style.borderRadius = "12px";
      wrapper.style.padding = "24px";
      wrapper.style.boxShadow = "var(--shadow-card)";

      // Title
      const title = document.createElement("h3");
      title.style.marginBottom = "8px";
      title.style.color = "var(--text)";
      title.textContent = item.name;
      wrapper.appendChild(title);

      // Source
      const source = document.createElement("p");
      source.style.fontSize = "12px";
      source.style.color = "var(--text-faint)";
      source.style.marginBottom = "24px";
      source.style.fontFamily = "var(--font-mono)";
      source.textContent = `Source: ${item.source}`;
      wrapper.appendChild(source);

      // Canvas container
      const canvasContainer = document.createElement("div");
      canvasContainer.style.position = "relative";
      canvasContainer.style.height = "300px";
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
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: isLight ? "#FFFFFF" : "#1a2332",
                titleColor: isLight ? "#10182B" : "#e2e8f0",
                bodyColor: isLight ? "#10182B" : "#e2e8f0",
                borderColor: isLight ? "rgba(16, 24, 43, 0.15)" : "#334155",
                borderWidth: 1,
              },
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: tickColor, font: { weight: "600" } },
              },
              y: {
                grid: { color: gridColor },
                ticks: { color: tickColor, font: { family: "JetBrains Mono" } },
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

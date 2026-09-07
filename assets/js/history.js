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
      title.textContent = item.title;
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
                borderWidth: 2.5,
                pointBackgroundColor: "#138808", // Green
                pointBorderColor: "#FFFFFF",
                pointBorderWidth: 1.5,
                pointRadius: 5,
                pointHoverRadius: 7,
                fill: true,
                tension: 0.3,
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
                grid: { color: gridColor },
                ticks: { color: tickColor, font: { family: "JetBrains Mono" } },
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

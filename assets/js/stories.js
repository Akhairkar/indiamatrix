document.addEventListener("DOMContentLoaded", function () {
  const FALLBACK_HISTORY = {
    "population": {
      "title": "Population (in billions)",
      "source": "World Bank",
      "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2023"],
      "values": [0.45, 0.55, 0.7, 0.87, 1.05, 1.23, 1.39, 1.43]
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

  function renderStoryCharts(data) {
    if (typeof Chart === "undefined") return;

    const isLight = document.documentElement.getAttribute("data-theme") === "light" ||
      (!document.documentElement.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: light)").matches);

    const gridColor = isLight ? "rgba(16, 24, 43, 0.08)" : "rgba(255, 255, 255, 0.08)";
    const tickColor = isLight ? "#475569" : "#94a3b8";

    // Render Population Chart if present
    const popCanvas = document.getElementById("populationChart");
    if (popCanvas && data["population"]) {
      const item = data["population"];
      new Chart(popCanvas, {
        type: "line",
        data: {
          labels: item.labels,
          datasets: [
            {
              label: "Population (Billions)",
              data: item.values,
              borderColor: "#FF9933", // Saffron
              backgroundColor: "rgba(255, 153, 51, 0.14)",
              borderWidth: 2.5,
              pointBackgroundColor: "#138808", // Green
              pointBorderColor: "#FFFFFF",
              pointBorderWidth: 1.5,
              pointRadius: 5,
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
              callbacks: {
                label: function (ctx) {
                  return " " + ctx.parsed.y + " Billion";
                }
              }
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

    // Render Literacy Chart if present
    const litCanvas = document.getElementById("literacyChart");
    if (litCanvas && data["literacy_rate"]) {
      const item = data["literacy_rate"];
      new Chart(litCanvas, {
        type: "line",
        data: {
          labels: item.labels,
          datasets: [
            {
              label: "Literacy Rate (%)",
              data: item.values,
              borderColor: "#2563EB", // Blue
              backgroundColor: "rgba(37, 99, 235, 0.12)",
              borderWidth: 2.5,
              pointBackgroundColor: "#138808", // Green
              pointBorderColor: "#FFFFFF",
              pointBorderWidth: 1.5,
              pointRadius: 5,
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
              callbacks: {
                label: function (context) {
                  return " " + context.parsed.y + "%";
                }
              }
            },
          },
          scales: {
            x: {
              grid: { color: gridColor },
              ticks: { color: tickColor, font: { family: "JetBrains Mono" } },
            },
            y: {
              grid: { color: gridColor },
              ticks: { color: tickColor, font: { family: "JetBrains Mono" }, callback: function (v) { return v + "%"; } },
            },
          },
        },
      });
    }

    // Render Digital Internet Penetration Chart if present
    const digCanvas = document.getElementById("digitalChart");
    if (digCanvas && data["internet_penetration"]) {
      const item = data["internet_penetration"];
      new Chart(digCanvas, {
        type: "line",
        data: {
          labels: item.labels,
          datasets: [
            {
              label: "Internet Penetration (%)",
              data: item.values,
              borderColor: "#2BB7A0", // Teal
              backgroundColor: "rgba(43, 183, 160, 0.14)",
              borderWidth: 2.5,
              pointBackgroundColor: "#F2A93B", // Saffron
              pointBorderColor: "#FFFFFF",
              pointBorderWidth: 1.5,
              pointRadius: 5,
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
              callbacks: {
                label: function (context) {
                  return " " + context.parsed.y + "%";
                },
              },
            },
          },
          scales: {
            x: {
              grid: { color: gridColor },
              ticks: { color: tickColor, font: { family: "JetBrains Mono" } },
            },
            y: {
              grid: { color: gridColor },
              ticks: { color: tickColor, font: { family: "JetBrains Mono" }, callback: function (v) { return v + "%"; } },
            },
          },
        },
      });
    }
  }

  fetch("../data/history.json")
    .then((response) => {
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return response.json();
    })
    .then((data) => {
      renderStoryCharts(data);
    })
    .catch((error) => {
      console.warn("Using offline fallback story data:", error);
      renderStoryCharts(FALLBACK_HISTORY);
    });
});

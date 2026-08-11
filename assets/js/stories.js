document.addEventListener("DOMContentLoaded", function () {
  fetch("../data/history.json")
    .then((response) => response.json())
    .then((data) => {
      
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
                label: "Population",
                data: item.values,
                borderColor: "#FF9933", // Saffron
                backgroundColor: "rgba(255, 153, 51, 0.1)",
                borderWidth: 2,
                pointBackgroundColor: "#138808", // Green
                pointRadius: 4,
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
                backgroundColor: "#1a2332",
                titleColor: "#e2e8f0",
                bodyColor: "#e2e8f0",
                borderColor: "#334155",
                borderWidth: 1,
              },
            },
            scales: {
              x: {
                grid: { color: "rgba(255,255,255,0.05)" },
                ticks: { color: "#94a3b8" },
              },
              y: {
                grid: { color: "rgba(255,255,255,0.05)" },
                ticks: { color: "#94a3b8" },
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
                borderColor: "#005A9C", // Blue
                backgroundColor: "rgba(0, 90, 156, 0.1)",
                borderWidth: 2,
                pointBackgroundColor: "#138808",
                pointRadius: 4,
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
                backgroundColor: "#1a2332",
                titleColor: "#e2e8f0",
                bodyColor: "#e2e8f0",
                borderColor: "#334155",
                borderWidth: 1,
                callbacks: {
                    label: function(context) {
                        return context.parsed.y + '%';
                    }
                }
              },
            },
            scales: {
              x: {
                grid: { color: "rgba(255,255,255,0.05)" },
                ticks: { color: "#94a3b8" },
              },
              y: {
                grid: { color: "rgba(255,255,255,0.05)" },
                ticks: { color: "#94a3b8", callback: function(value) { return value + "%" } },
              },
            },
          },
        });
      }

    })
    .catch((error) => {
      console.error("Error loading stories chart data:", error);
    });
});

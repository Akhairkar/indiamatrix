document.addEventListener("DOMContentLoaded", function () {
  fetch("data/history.json")
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("history-charts-container");
      if (!container) return;

      Object.keys(data).forEach((key) => {
        const item = data[key];

        // Create wrapper
        const wrapper = document.createElement("div");
        wrapper.style.background = "var(--panel-bg)";
        wrapper.style.border = "1px solid var(--border)";
        wrapper.style.borderRadius = "12px";
        wrapper.style.padding = "24px";

        // Title
        const title = document.createElement("h3");
        title.style.marginBottom = "8px";
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

        // Render chart
        new Chart(canvas, {
          type: "line",
          data: {
            labels: item.labels,
            datasets: [
              {
                label: item.title,
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
      });
    })
    .catch((error) => {
      console.error("Error loading history data:", error);
    });
});

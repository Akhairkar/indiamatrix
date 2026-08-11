document.addEventListener("DOMContentLoaded", function () {
  fetch("data/world.json")
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("world-charts-container");
      if (!container) return;

      data.comparisons.forEach((item) => {
        // Create wrapper
        const wrapper = document.createElement("div");
        wrapper.style.background = "var(--panel-bg)";
        wrapper.style.border = "1px solid var(--border)";
        wrapper.style.borderRadius = "12px";
        wrapper.style.padding = "24px";

        // Title
        const title = document.createElement("h3");
        title.style.marginBottom = "8px";
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
        new Chart(canvas, {
          type: "bar",
          data: {
            labels: ["India", "China", "USA", "World Avg/Total"],
            datasets: [
              {
                label: item.name,
                data: [item.india, item.china, item.usa, item.world],
                backgroundColor: [
                  "#FF9933", // India (Saffron)
                  "#E3000F", // China (Red)
                  "#005A9C", // USA (Blue)
                  "#94a3b8", // World (Gray)
                ],
                borderRadius: 4,
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
                grid: { display: false },
                ticks: { color: "#94a3b8", font: { weight: "600" } },
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
      console.error("Error loading world data:", error);
    });
});

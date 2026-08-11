document.addEventListener("DOMContentLoaded", function () {
  let explorerData = [];
  let currentLang = document.documentElement.getAttribute("data-lang") || "en";
  let chartInstance = null;

  const stateSelect = document.getElementById("state-select");
  const indicatorSelect = document.getElementById("indicator-select");
  const downloadBtn = document.getElementById("download-btn");
  const vizTitle = document.getElementById("viz-title");
  const vizSource = document.getElementById("viz-source");
  const tableBody = document.getElementById("viz-table-body");
  const canvas = document.getElementById("explorerChart");

  // Fetch compiled explorer data
  fetch("data/explorer.json")
    .then((res) => res.json())
    .then((data) => {
      explorerData = data.states;
      populateStateSelect();
      render();
    })
    .catch((err) => console.error("Error loading explorer data:", err));

  function populateStateSelect() {
    // Keep 'all' option, clear others
    stateSelect.innerHTML = `<option value="all" selected data-en="All States / UTs" data-hi="सभी राज्य / केंद्र शासित प्रदेश">All States / UTs</option>`;
    
    explorerData.forEach(state => {
      const opt = document.createElement("option");
      opt.value = state.id;
      opt.textContent = state.name[currentLang];
      // Store translations for dynamic switching
      opt.setAttribute("data-en", state.name.en);
      opt.setAttribute("data-hi", state.name.hi);
      stateSelect.appendChild(opt);
    });
  }

  function getSelectedStates() {
    const selectedOptions = Array.from(stateSelect.selectedOptions).map(opt => opt.value);
    if (selectedOptions.includes("all")) {
      return explorerData;
    }
    return explorerData.filter(state => selectedOptions.includes(state.id));
  }

  function render() {
    const indicatorId = indicatorSelect.value;
    const statesToRender = getSelectedStates();
    
    // Extract indicator name
    const selectedIndicatorOption = indicatorSelect.options[indicatorSelect.selectedIndex];
    vizTitle.textContent = selectedIndicatorOption.getAttribute(`data-${currentLang}`) || selectedIndicatorOption.textContent;

    // Build dataset
    const chartLabels = [];
    const chartData = [];
    let sourceText = "";
    
    tableBody.innerHTML = "";

    // We sort states by value descending for better visualization
    const sortedStates = [...statesToRender].map(state => {
        const ind = state.indicators.find(i => i.id === indicatorId);
        return {
            stateName: state.name[currentLang],
            value: ind ? ind.value : 0,
            formattedValue: ind ? ind.formatted_value[currentLang] : "-",
            year: ind ? ind.year : "-",
            source: ind ? ind.source_name[currentLang] : ""
        };
    }).sort((a, b) => b.value - a.value);

    sortedStates.forEach(item => {
        chartLabels.push(item.stateName);
        chartData.push(item.value);
        if (!sourceText && item.source) {
            sourceText = item.source; // Grab the first available source
        }

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.stateName}</td>
            <td style="font-family:var(--font-mono); font-weight:600;">${item.formattedValue}</td>
            <td style="font-family:var(--font-mono); color:var(--text-faint);">${item.year}</td>
        `;
        tableBody.appendChild(tr);
    });

    vizSource.textContent = `Source: ${sourceText || 'Unknown'}`;

    // Render Chart
    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(canvas, {
        type: "bar",
        data: {
          labels: chartLabels,
          datasets: [
            {
              label: vizTitle.textContent,
              data: chartData,
              backgroundColor: "#005A9C", // Blue
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
              ticks: { color: "#94a3b8", maxRotation: 45, minRotation: 45 },
            },
            y: {
              grid: { color: "rgba(255,255,255,0.05)" },
              ticks: { color: "#94a3b8" },
            },
          },
        },
    });
  }

  function downloadCSV() {
    const indicatorId = indicatorSelect.value;
    const statesToRender = getSelectedStates();
    
    let csvContent = "State/UT,Indicator ID,Value,Data Year,Source\n";

    statesToRender.forEach(state => {
        const ind = state.indicators.find(i => i.id === indicatorId);
        if (ind) {
            const stateName = state.name.en.replace(/,/g, ""); // escape commas
            const val = ind.value;
            const year = ind.year;
            const src = ind.source_name.en.replace(/,/g, "");
            csvContent += `${stateName},${indicatorId},${val},${year},${src}\n`;
        }
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `indiametrix_${indicatorId}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Event Listeners
  stateSelect.addEventListener("change", render);
  indicatorSelect.addEventListener("change", render);
  downloadBtn.addEventListener("click", downloadCSV);

  // Listen for language change events from main.js (which updates data-lang on html)
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === "data-lang") {
        currentLang = document.documentElement.getAttribute("data-lang") || "en";
        // Re-populate state dropdown options text
        Array.from(stateSelect.options).forEach(opt => {
            const translatedText = opt.getAttribute(`data-${currentLang}`);
            if (translatedText) opt.textContent = translatedText;
        });
        render();
      }
    });
  });
  
  observer.observe(document.documentElement, { attributes: true });

});

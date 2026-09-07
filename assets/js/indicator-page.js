/**
 * IndiaMetrix Master Indicator Page Interactive Engine
 * Powers:
 * 1. Dual-mode Visualization (State-by-State Leaderboard & Decadal Historical Trend)
 * 2. High-contrast, theme-aware Chart.js rendering with detailed rich tooltips
 * 3. Interactive Searchable & Sortable State Leaderboard Table
 * 4. Real-time Mini State Simulator & Calculator
 * 5. Theme toggle synchronization
 */

(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    const data = window.INDICATOR_DATA;
    if (!data) return;

    let currentView = data.states && data.states.length > 0 ? 'states' : 'history';
    let chartInstance = null;
    const canvas = document.getElementById('indChartCanvas');
    const tableBody = document.getElementById('indTableBody');
    const searchInput = document.getElementById('indTableSearch');
    const toggleStatesBtn = document.getElementById('btnViewStates');
    const toggleHistoryBtn = document.getElementById('btnViewHistory');
    const calcSelect = document.getElementById('indCalcState');
    const calcResultVal = document.getElementById('indCalcVal');
    const calcResultEquiv = document.getElementById('indCalcEquiv');
    const calcResultShare = document.getElementById('indCalcShare');
    const calcDeepLink = document.getElementById('indCalcLink');

    function isLightMode() {
      return document.documentElement.getAttribute('data-theme') === 'light' ||
        (!document.documentElement.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: light)').matches);
    }

    function getThemeColors() {
      const isLight = isLightMode();
      return {
        isLight: isLight,
        text: isLight ? '#10182B' : '#E8ECF8',
        muted: isLight ? '#475569' : '#94A3B8',
        grid: isLight ? 'rgba(16, 24, 43, 0.08)' : 'rgba(255, 255, 255, 0.06)',
        tooltipBg: isLight ? '#FFFFFF' : '#10182B',
        tooltipBorder: isLight ? 'rgba(16, 24, 43, 0.18)' : 'rgba(43, 183, 160, 0.35)',
        barPrimary: isLight ? '#D97706' : '#F2A93B',
        barSecondary: isLight ? '#0D9488' : '#2BB7A0',
        linePrimary: isLight ? '#D97706' : '#F2A93B',
        lineArea: isLight ? 'rgba(217, 119, 6, 0.12)' : 'rgba(242, 169, 59, 0.15)'
      };
    }

    // 1. Render Master Chart
    function renderChart() {
      if (!canvas) return;
      if (chartInstance) {
        chartInstance.destroy();
      }

      const colors = getThemeColors();
      const ctx = canvas.getContext('2d');

      if (currentView === 'states' && data.states && data.states.length > 0) {
        // State Breakdown Bar Chart
        const labels = data.states.map(s => s.name.en);
        const values = data.states.map(s => s.value);
        
        // Color top 3 states distinctly
        const barColors = data.states.map((s, idx) => {
          if (idx === 0) return colors.barPrimary; // #1 Gold/Saffron
          if (idx < 3) return colors.barSecondary; // Top 3 Teal
          return colors.isLight ? '#94A3B8' : '#28385A';
        });

        chartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: data.name.en,
              data: values,
              backgroundColor: barColors,
              borderRadius: 4,
              borderWidth: 0,
              maxBarThickness: 28
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: colors.tooltipBg,
                titleColor: colors.text,
                bodyColor: colors.text,
                borderColor: colors.tooltipBorder,
                borderWidth: 1.5,
                padding: 14,
                cornerRadius: 8,
                titleFont: { family: 'Inter', size: 14, weight: '700' },
                bodyFont: { family: 'JetBrains Mono', size: 12.5 },
                callbacks: {
                  title: function(items) {
                    const idx = items[0].dataIndex;
                    const st = data.states[idx];
                    return `#${idx + 1} ${st.name.en} ${st.equiv_flag || ''}`;
                  },
                  label: function(item) {
                    const idx = item.dataIndex;
                    const st = data.states[idx];
                    const lines = [];
                    lines.push(`• Value: ${st.formatted.en}`);
                    if (st.share_pct) {
                      lines.push(`• National Share: ${st.share_pct}% of India`);
                    }
                    if (st.equiv_country) {
                      lines.push(`• Equivalent Nation: ${st.equiv_country}`);
                    }
                    return lines;
                  }
                }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: {
                  color: colors.muted,
                  font: { family: 'Inter', size: 11 },
                  maxRotation: 45,
                  minRotation: 45
                }
              },
              y: {
                grid: { color: colors.grid },
                ticks: {
                  color: colors.muted,
                  font: { family: 'JetBrains Mono', size: 11 },
                  callback: function(val) {
                    if (data.id.includes('gdp')) {
                      if (val >= 100000) return '₹' + (val / 100000).toFixed(1) + 'L Cr';
                      return '₹' + val.toLocaleString('en-IN') + ' Cr';
                    }
                    if (data.id.includes('population')) {
                      if (val >= 10000000) return (val / 10000000).toFixed(1) + ' Cr';
                      return val.toLocaleString('en-IN');
                    }
                    if (data.id.includes('literacy') || data.id.includes('unemployment')) {
                      return val + '%';
                    }
                    return val.toLocaleString('en-IN');
                  }
                }
              }
            }
          }
        });
      } else if (data.history && data.history.labels && data.history.labels.length > 0) {
        // Multi-Decade Historical Trend Line Chart
        chartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.history.labels,
            datasets: [{
              label: data.name.en,
              data: data.history.values,
              borderColor: colors.linePrimary,
              backgroundColor: colors.lineArea,
              borderWidth: 3,
              pointBackgroundColor: colors.barSecondary,
              pointBorderColor: '#FFFFFF',
              pointBorderWidth: 2,
              pointRadius: 5,
              pointHoverRadius: 8,
              fill: true,
              tension: 0.35
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: colors.tooltipBg,
                titleColor: colors.text,
                bodyColor: colors.text,
                borderColor: colors.tooltipBorder,
                borderWidth: 1.5,
                padding: 14,
                cornerRadius: 8,
                titleFont: { family: 'Inter', size: 14, weight: '700' },
                bodyFont: { family: 'JetBrains Mono', size: 12.5 },
                callbacks: {
                  title: function(items) {
                    return `Year ${items[0].label} • National Benchmark`;
                  },
                  label: function(item) {
                    const idx = item.dataIndex;
                    const fmtVal = data.history.formatted ? data.history.formatted[idx] : item.raw;
                    const lines = [`• India Recorded: ${fmtVal}`];
                    if (idx > 0) {
                      const prev = data.history.values[idx - 1];
                      const curr = item.raw;
                      const diff = curr - prev;
                      const pct = ((diff / prev) * 100).toFixed(1);
                      lines.push(`• Period Growth: ${diff >= 0 ? '+' : ''}${pct}%`);
                    }
                    return lines;
                  }
                }
              }
            },
            scales: {
              x: {
                grid: { color: colors.grid },
                ticks: { color: colors.muted, font: { family: 'JetBrains Mono', size: 12 } }
              },
              y: {
                grid: { color: colors.grid },
                ticks: {
                  color: colors.muted,
                  font: { family: 'JetBrains Mono', size: 11 },
                  callback: function(val) {
                    return val.toLocaleString('en-IN');
                  }
                }
              }
            }
          }
        });
      }
    }

    // 2. View Toggle Handler
    if (toggleStatesBtn && toggleHistoryBtn) {
      toggleStatesBtn.addEventListener('click', function() {
        toggleStatesBtn.classList.add('is-active');
        toggleHistoryBtn.classList.remove('is-active');
        currentView = 'states';
        renderChart();
      });

      toggleHistoryBtn.addEventListener('click', function() {
        toggleHistoryBtn.classList.add('is-active');
        toggleStatesBtn.classList.remove('is-active');
        currentView = 'history';
        renderChart();
      });
    }

    // 3. Searchable State Leaderboard Table
    function renderTable(filterText) {
      if (!tableBody || !data.states) return;
      const q = (filterText || '').toLowerCase().trim();
      const filtered = data.states.filter(s => {
        return s.name.en.toLowerCase().includes(q) ||
               (s.name.hi && s.name.hi.includes(q)) ||
               (s.equiv_country && s.equiv_country.toLowerCase().includes(q));
      });

      if (filtered.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:24px; color:var(--text-muted);">No matching states or territories found.</td></tr>`;
        return;
      }

      let html = '';
      filtered.forEach((st, idx) => {
        const rank = st.rank || (idx + 1);
        const rankBadge = rank <= 3 
          ? `<span class="ind-rank-badge ind-rank-badge--top">#${rank}</span>`
          : `<span class="ind-rank-badge">#${rank}</span>`;
        
        const equivCell = st.equiv_country 
          ? `<span style="font-size:13px; font-family:var(--font-mono); color:var(--text);">${st.equiv_flag || '🌍'} ${st.equiv_country}</span>` 
          : `<span style="color:var(--text-faint);">-</span>`;

        const shareCell = st.share_pct 
          ? `<div style="display:flex; align-items:center; gap:8px;">
               <span style="font-family:var(--font-mono); font-size:13px; font-weight:600; min-width:44px;">${st.share_pct}%</span>
               <div style="flex:1; max-width:80px; height:6px; background:var(--surface-2); border-radius:3px; overflow:hidden;">
                 <div style="width:${Math.min(100, st.share_pct * 5)}%; height:100%; background:var(--teal);"></div>
               </div>
             </div>`
          : `<span style="color:var(--text-faint);">-</span>`;

        html += `
          <tr>
            <td style="width: 60px;">${rankBadge}</td>
            <td>
              <a href="../states/${st.id}.html" class="ind-state-link">
                <strong>${st.name.en}</strong>
                <span style="font-size:12px; color:var(--text-faint); margin-left:4px;">${st.name.hi || ''}</span>
              </a>
            </td>
            <td style="font-family:var(--font-mono); font-weight:700; color:var(--text); font-size:14px;">
              ${st.formatted.en}
            </td>
            <td>${equivCell}</td>
            <td>${shareCell}</td>
          </tr>
        `;
      });
      tableBody.innerHTML = html;
    }

    if (searchInput) {
      searchInput.addEventListener('input', function(e) {
        renderTable(e.target.value);
      });
    }

    // 4. Interactive Mini State Calculator / Simulator
    if (calcSelect && data.states && data.states.length > 0) {
      calcSelect.innerHTML = '';
      data.states.forEach(st => {
        const opt = document.createElement('option');
        opt.value = st.id;
        opt.textContent = `${st.name.en} (#${st.rank || ''})`;
        if (st.id === 'maharashtra') opt.selected = true;
        calcSelect.appendChild(opt);
      });

      function updateCalculator() {
        const sid = calcSelect.value;
        const st = data.states.find(s => s.id === sid);
        if (!st) return;

        if (calcResultVal) calcResultVal.textContent = st.formatted.en;
        if (calcResultEquiv) {
          calcResultEquiv.innerHTML = st.equiv_country 
            ? `<span style="font-size:18px;">${st.equiv_flag || ''}</span> ${st.equiv_country}`
            : 'National Leader';
        }
        if (calcResultShare) {
          calcResultShare.textContent = st.share_pct ? `${st.share_pct}% of India's Total` : `Rank #${st.rank}`;
        }
        if (calcDeepLink) {
          if (data.id.includes('gdp')) {
            calcDeepLink.href = `../tools/economic-comparator.html?state=${encodeURIComponent(st.id)}`;
          } else if (data.id.includes('lit') || data.id.includes('pop')) {
            calcDeepLink.href = `../tools/demographic-calculator.html?s1=${encodeURIComponent(st.id)}`;
          } else {
            calcDeepLink.href = `../compare.html?s1=${encodeURIComponent(st.id)}&s2=gujarat`;
          }
        }
      }

      calcSelect.addEventListener('change', updateCalculator);
      updateCalculator();
    }

    // Initial table & chart rendering
    renderChart();
    renderTable();

    // 5. Theme Toggle Listener
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        setTimeout(renderChart, 60);
      });
    });
  });
})();

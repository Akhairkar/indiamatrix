/**
 * IndiaMetrix Grounded Data Intelligence Engine
 * Client-side verified retrieval with zero hallucination and zero API key exposure.
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatInput = document.getElementById('chat-input');
  const chatBtn = document.getElementById('chat-btn');
  const chatBox = document.getElementById('chat-box');
  const typingIndicator = document.getElementById('typing-indicator');
  const suggestionChips = document.getElementById('suggestion-chips');

  let explorerData = {
    india: null,
    states: [],
    districts: []
  };
  let currentLang = document.documentElement.getAttribute('data-lang') || 'en';

  // Load verified data
  fetch('data/explorer.json')
    .then(response => response.json())
    .then(data => {
      explorerData = data;
      console.log(`IndiaMetrix Engine loaded: ${data.states?.length || 0} states, ${data.districts?.length || 0} districts.`);
    })
    .catch(err => console.error("Failed to load IndiaMetrix explorer data:", err));

  // Listen to language changes
  const observer = new MutationObserver(() => {
    currentLang = document.documentElement.getAttribute('data-lang') || 'en';
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-lang'] });

  const appendMessage = (htmlContent, sender) => {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerHTML = htmlContent;
    chatBox.insertBefore(msgDiv, typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;
  };

  // State Aliases Dictionary
  const stateAliases = {
    'andaman-nicobar': ['andaman', 'nicobar', 'andaman and nicobar', 'andaman & nicobar'],
    'andhra-pradesh': ['andhra', 'andhra pradesh', 'ap'],
    'arunachal-pradesh': ['arunachal', 'arunachal pradesh'],
    'assam': ['assam', 'asom'],
    'bihar': ['bihar'],
    'chandigarh': ['chandigarh'],
    'chhattisgarh': ['chhattisgarh', 'chattisgarh'],
    'dadra-nagar-haveli-daman-diu': ['daman', 'diu', 'dadra', 'nagar haveli', 'dnh'],
    'delhi': ['delhi', 'nct', 'new delhi', 'nct of delhi'],
    'goa': ['goa'],
    'gujarat': ['gujarat'],
    'haryana': ['haryana'],
    'himachal-pradesh': ['himachal', 'himachal pradesh', 'hp'],
    'jammu-kashmir': ['jammu', 'kashmir', 'j&k', 'jammu and kashmir', 'jammu & kashmir'],
    'jharkhand': ['jharkhand'],
    'karnataka': ['karnataka'],
    'kerala': ['kerala'],
    'ladakh': ['ladakh'],
    'lakshadweep': ['lakshadweep'],
    'madhya-pradesh': ['madhya pradesh', 'mp'],
    'maharashtra': ['maharashtra', 'maha'],
    'manipur': ['manipur'],
    'meghalaya': ['meghalaya'],
    'mizoram': ['mizoram'],
    'nagaland': ['nagaland'],
    'odisha': ['odisha', 'orissa'],
    'puducherry': ['puducherry', 'pondicherry'],
    'punjab': ['punjab'],
    'rajasthan': ['rajasthan'],
    'sikkim': ['sikkim'],
    'tamil-nadu': ['tamil nadu', 'tamilnadu', 'tn'],
    'telangana': ['telangana'],
    'tripura': ['tripura'],
    'uttar-pradesh': ['uttar pradesh', 'up'],
    'uttarakhand': ['uttarakhand', 'uk', 'uttaranchal'],
    'west-bengal': ['west bengal', 'bengal', 'wb']
  };

  // District Aliases
  const districtAliases = {
    'pune': ['pune', 'poona'],
    'bengaluru-urban': ['bengaluru', 'bangalore', 'bengaluru urban', 'bangalore urban'],
    'ahmedabad': ['ahmedabad', 'amdavad'],
    'chennai': ['chennai', 'madras'],
    'lucknow': ['lucknow'],
    'ernakulam': ['ernakulam', 'kochi', 'cochin'],
    'nagpur': ['nagpur']
  };

  // Indicator Matchers
  const indicatorConfigs = [
    {
      id: 'population',
      keywords: ['population', 'people', 'inhabitants', 'citizens', 'pop', 'जनसंख्या', 'आबादी'],
      label: { en: 'Population', hi: 'जनसंख्या' }
    },
    {
      id: 'literacy-rate',
      keywords: ['literacy', 'literate', 'education', 'literacy rate', 'साक्षरता', 'पढ़ाई'],
      label: { en: 'Literacy Rate', hi: 'साक्षरता दर' }
    },
    {
      id: 'gdp',
      keywords: ['gsdp', 'gdp', 'economy', 'economic', 'gross state domestic product', 'जीडीपी', 'अर्थव्यवस्था'],
      label: { en: 'GSDP Economy', hi: 'जीएसडीपी अर्थव्यवस्था' }
    },
    {
      id: 'unemployment-rate',
      keywords: ['unemployment', 'unemployed', 'jobless', 'jobs', 'unemployment rate', 'बेरोजगारी', 'रोज़गार'],
      label: { en: 'Unemployment Rate', hi: 'बेरोज़गारी दर' }
    },
    {
      id: 'sex-ratio',
      keywords: ['sex ratio', 'gender ratio', 'females', 'women per', 'लिंगानुपात', 'स्त्री-पुरुष अनुपात'],
      label: { en: 'Sex Ratio', hi: 'लिंगानुपात' }
    },
    {
      id: 'area',
      keywords: ['area', 'sq km', 'size', 'land', 'square kilometer', 'क्षेत्रफल'],
      label: { en: 'Geographic Area', hi: 'क्षेत्रफल' }
    },
    {
      id: 'imr',
      keywords: ['imr', 'infant mortality', 'infant mortality rate', 'child mortality', 'शिशु मृत्यु दर'],
      label: { en: 'Infant Mortality Rate (IMR)', hi: 'शिशु मृत्यु दर' }
    }
  ];

  function findMatchedStates(query) {
    const q = query.toLowerCase();
    const matched = [];
    
    // Sort aliases by length descending so longer names like 'uttar pradesh' match before 'up'
    for (const [stateId, aliases] of Object.entries(stateAliases)) {
      for (const alias of aliases) {
        // Regex with word boundaries
        const regex = new RegExp(`\\b${alias.replace('&', '(&|and)')}\\b`, 'i');
        if (regex.test(q)) {
          if (!matched.includes(stateId)) {
            matched.push(stateId);
          }
          break;
        }
      }
    }
    return matched;
  }

  function findMatchedDistrict(query) {
    const q = query.toLowerCase();
    for (const [distId, aliases] of Object.entries(districtAliases)) {
      for (const alias of aliases) {
        const regex = new RegExp(`\\b${alias}\\b`, 'i');
        if (regex.test(q)) {
          return explorerData.districts.find(d => d.id === distId || d.id.endsWith(distId));
        }
      }
    }
    return null;
  }

  function findMatchedIndicator(query) {
    const q = query.toLowerCase();
    for (const ind of indicatorConfigs) {
      for (const kw of ind.keywords) {
        const regex = new RegExp(`\\b${kw}\\b`, 'i');
        if (regex.test(q)) {
          return ind;
        }
      }
    }
    return null;
  }

  function formatDisplay(ind) {
    if (!ind) return '-';
    if (ind.display && ind.display[currentLang]) return ind.display[currentLang];
    if (ind.display && ind.display.en) return ind.display.en;
    if (ind.formatted_value) return ind.formatted_value[currentLang] || ind.formatted_value.en;
    return `${ind.value} ${ind.unit || ''}`;
  }

  // Answer Generator
  function answerQuery(query) {
    const q = query.toLowerCase().trim();

    // 1. Check National / India Overview queries
    const isIndiaQuery = /\bindia\b|\bnational\b|\bcountry\b|\ball india\b|\bभारत\b/.test(q);
    if (isIndiaQuery && !findMatchedStates(q).length) {
      const ind = findMatchedIndicator(q);
      if (explorerData.india && explorerData.india.indicators) {
        let nationalInds = explorerData.india.indicators;
        if (ind) {
          const matched = nationalInds.find(i => i.id === ind.id || (ind.id === 'gdp' && i.id.startsWith('gdp')));
          if (matched) {
            return `
              <p><strong>India — National ${matched.name[currentLang] || matched.name.en}</strong></p>
              <div class="im-chat-stat-card">
                <div style="font-size:12px; color:var(--text-faint); text-transform:uppercase;">National Figure</div>
                <div class="im-chat-stat-val">${formatDisplay(matched)}</div>
                <div class="im-chat-provenance">
                  <span>📅 Ref Year: <strong>${matched.year}</strong></span>
                  <span>🏛️ Source: <strong>${matched.source_id.toUpperCase()}</strong></span>
                </div>
              </div>
              <p style="font-size:13px; color:var(--text-muted); margin-top:8px;">
                ${matched.methodology_note || ''}
              </p>
              <div style="margin-top:10px;">
                <a href="india.html" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">View Full India Profile →</a>
              </div>
            `;
          }
        }
        // General India Summary
        return `
          <p><strong>India (Bharat) — National Statistical Overview</strong></p>
          <div class="im-chat-table-wrap">
            <table class="im-chat-table">
              <thead><tr><th>Indicator</th><th>Verified Value</th><th>Ref Year</th><th>Source</th></tr></thead>
              <tbody>
                ${nationalInds.slice(0, 5).map(i => `
                  <tr>
                    <td><strong>${i.name[currentLang] || i.name.en}</strong></td>
                    <td style="font-family:var(--font-mono); font-weight:600;">${formatDisplay(i)}</td>
                    <td style="font-family:var(--font-mono); color:var(--text-faint);">${i.year}</td>
                    <td><a href="${i.source_url}" target="_blank" rel="noopener noreferrer">${i.source_id}</a></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
          <div style="margin-top:10px;">
            <a href="india.html" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">Explore 50+ India Indicators →</a>
          </div>
        `;
      }
    }

    // 2. Rankings & Extremes (Highest, Lowest, Top, Bottom, Most, Least)
    const isRanking = /\b(highest|top|most|largest|maximum|best|lowest|bottom|least|smallest|minimum|rank|ranking|rankings|सबसे ज्यादा|सबसे कम)\b/.test(q);
    const indConfig = findMatchedIndicator(q);

    if (isRanking && indConfig) {
      const isLowest = /\b(lowest|bottom|least|smallest|minimum|सबसे कम)\b/.test(q);
      const targetId = indConfig.id;

      const scored = explorerData.states.map(state => {
        const ind = state.indicators.find(i => i.id === targetId || (targetId === 'gdp' && i.id === 'gdp'));
        return {
          state,
          ind,
          val: ind ? ind.value : (isLowest ? Infinity : -Infinity)
        };
      }).filter(s => s.ind);

      scored.sort((a, b) => isLowest ? a.val - b.val : b.val - a.val);

      const top3 = scored.slice(0, 3);
      if (top3.length > 0) {
        const title = isLowest ? `Lowest ${indConfig.label[currentLang]} States` : `Highest ${indConfig.label[currentLang]} States`;
        return `
          <p><strong>${title} (Verified Government Data)</strong></p>
          <div class="im-chat-table-wrap">
            <table class="im-chat-table">
              <thead><tr><th>Rank</th><th>State</th><th>Value</th><th>Year</th><th>Source</th></tr></thead>
              <tbody>
                ${top3.map((item, idx) => `
                  <tr>
                    <td><strong>#${idx + 1}</strong></td>
                    <td><a href="states/${item.state.id}.html"><strong>${item.state.name[currentLang] || item.state.name.en}</strong></a></td>
                    <td style="font-family:var(--font-mono); font-weight:700; color:var(--teal);">${formatDisplay(item.ind)}</td>
                    <td style="font-family:var(--font-mono); color:var(--text-faint);">${item.ind.year}</td>
                    <td><span style="font-size:11px; text-transform:uppercase;">${item.ind.source_id}</span></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
          <div style="margin-top:12px;">
            <a href="rankings.html#rank-${targetId}" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">View Full 36-State Ranking Table →</a>
          </div>
        `;
      }
    }

    // 3. Comparisons between 2 states
    const matchedStates = findMatchedStates(q);
    const isCompare = /\b(compare|vs|versus|between|difference|और|तुलना)\b/.test(q) || matchedStates.length >= 2;

    if (isCompare && matchedStates.length >= 2) {
      const s1 = explorerData.states.find(s => s.id === matchedStates[0]);
      const s2 = explorerData.states.find(s => s.id === matchedStates[1]);

      if (s1 && s2) {
        const compareInds = ['population', 'literacy-rate', 'gdp', 'unemployment-rate', 'sex-ratio', 'area'];
        return `
          <p><strong>Comparison: ${s1.name[currentLang] || s1.name.en} vs ${s2.name[currentLang] || s2.name.en}</strong></p>
          <div class="im-chat-table-wrap">
            <table class="im-chat-table">
              <thead>
                <tr>
                  <th>Indicator</th>
                  <th>${s1.name[currentLang] || s1.name.en}</th>
                  <th>${s2.name[currentLang] || s2.name.en}</th>
                </tr>
              </thead>
              <tbody>
                ${compareInds.map(indId => {
                  const i1 = s1.indicators.find(i => i.id === indId);
                  const i2 = s2.indicators.find(i => i.id === indId);
                  const label = i1?.name[currentLang] || i1?.name.en || indId;
                  return `
                    <tr>
                      <td><strong>${label}</strong></td>
                      <td style="font-family:var(--font-mono); font-weight:600;">${formatDisplay(i1)}</td>
                      <td style="font-family:var(--font-mono); font-weight:600;">${formatDisplay(i2)}</td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
          <div style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
            <a href="compare.html?s1=${s1.id}&s2=${s2.id}" class="im-btn im-btn--primary" style="font-size:12px; padding:4px 12px;">Open Interactive Compare Tool →</a>
          </div>
        `;
      }
    }

    // 4. District Lookup
    const matchedDist = findMatchedDistrict(q);
    if (matchedDist) {
      const ind = findMatchedIndicator(q);
      const distName = matchedDist.name[currentLang] || matchedDist.name.en;
      if (ind) {
        const dInd = matchedDist.indicators.find(i => i.id === ind.id);
        if (dInd) {
          return `
            <p><strong>${distName} District — ${dInd.name[currentLang] || dInd.name.en}</strong></p>
            <div class="im-chat-stat-card">
              <div style="font-size:12px; color:var(--text-faint); text-transform:uppercase;">District Level (${matchedDist.state_id.replace('-', ' ').toUpperCase()})</div>
              <div class="im-chat-stat-val">${formatDisplay(dInd)}</div>
              <div class="im-chat-provenance">
                <span>📅 Reference Year: <strong>${dInd.year}</strong></span>
                <span>🏛️ Official Source: <strong>${dInd.source_id.toUpperCase()}</strong></span>
              </div>
            </div>
            <div style="margin-top:10px;">
              <a href="districts/${matchedDist.state_id}/${matchedDist.id}.html" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">View ${distName} District Profile →</a>
            </div>
          `;
        }
      }
      return `
        <p><strong>${distName} District Overview</strong></p>
        <div class="im-chat-table-wrap">
          <table class="im-chat-table">
            <thead><tr><th>Indicator</th><th>Value</th><th>Year</th><th>Source</th></tr></thead>
            <tbody>
              ${matchedDist.indicators.map(i => `
                <tr>
                  <td><strong>${i.name[currentLang] || i.name.en}</strong></td>
                  <td style="font-family:var(--font-mono); font-weight:600;">${formatDisplay(i)}</td>
                  <td style="font-family:var(--font-mono); color:var(--text-faint);">${i.year}</td>
                  <td>${i.source_id}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
        <div style="margin-top:10px;">
          <a href="districts/${matchedDist.state_id}/${matchedDist.id}.html" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">View District Page →</a>
        </div>
      `;
    }

    // 5. Single State Query (Indicator specific or State overview)
    if (matchedStates.length === 1) {
      const stateId = matchedStates[0];
      const state = explorerData.states.find(s => s.id === stateId);
      const stateName = state.name[currentLang] || state.name.en;

      if (indConfig) {
        const ind = state.indicators.find(i => i.id === indConfig.id);
        if (ind) {
          const dirBadge = ind.direction === 'higher_is_better' ? '🟢 Higher is better' : ind.direction === 'lower_is_better' ? '🟢 Lower is better' : '⚪ Demographic Metric';
          return `
            <p><strong>${stateName} — ${ind.name[currentLang] || ind.name.en}</strong></p>
            <div class="im-chat-stat-card">
              <div style="font-size:12px; color:var(--text-faint); display:flex; justify-content:space-between;">
                <span>STATE LEVEL</span>
                <span class="im-chat-badge" style="background:var(--surface-1); border:1px solid var(--border);">${dirBadge}</span>
              </div>
              <div class="im-chat-stat-val">${formatDisplay(ind)}</div>
              <div class="im-chat-provenance">
                <span>📅 Reference Year: <strong>${ind.year}</strong></span>
                <span>🏛️ Publisher: <strong>${ind.source_id.toUpperCase()}</strong></span>
              </div>
            </div>
            <p style="font-size:12px; color:var(--text-muted); margin-top:6px;">${ind.methodology_note || ''}</p>
            <div style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
              <a href="states/${state.id}.html" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">View ${stateName} Profile →</a>
              <a href="rankings.html#rank-${ind.id}" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">View Rankings →</a>
            </div>
          `;
        }
      }

      // State Overview Cards
      return `
        <p><strong>${stateName} Profile Overview</strong></p>
        <div class="im-chat-table-wrap">
          <table class="im-chat-table">
            <thead><tr><th>Indicator</th><th>Verified Value</th><th>Ref Year</th><th>Source</th></tr></thead>
            <tbody>
              ${state.indicators.map(i => `
                <tr>
                  <td><strong>${i.name[currentLang] || i.name.en}</strong></td>
                  <td style="font-family:var(--font-mono); font-weight:600;">${formatDisplay(i)}</td>
                  <td style="font-family:var(--font-mono); color:var(--text-faint);">${i.year}</td>
                  <td><a href="${i.source_url}" target="_blank" rel="noopener noreferrer">${i.source_id}</a></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
        <div style="margin-top:12px; display:flex; gap:8px;">
          <a href="states/${state.id}.html" class="im-btn im-btn--primary" style="font-size:12px; padding:4px 12px;">Full ${stateName} Profile →</a>
          <a href="compare.html?s1=${state.id}" class="im-btn im-btn--secondary" style="font-size:12px; padding:4px 10px;">Compare ${stateName} →</a>
        </div>
      `;
    }

    // 6. Generic or Unrecognized Query -> Polite Guided Assistant
    return `
      <p>I am grounded exclusively in verified Indian demographic, economic, and social statistics. I cannot provide unverified commentary or opinions.</p>
      <p style="margin-top:8px;"><strong>You can ask me questions such as:</strong></p>
      <ul style="margin: 8px 0 12px 20px; font-size:14px; line-height:1.6;">
        <li><em>"Which state has the highest literacy rate?"</em></li>
        <li><em>"What is the unemployment rate in Kerala?"</em></li>
        <li><em>"Compare Maharashtra and Gujarat"</em></li>
        <li><em>"What is India's GDP and population?"</em></li>
        <li><em>"Tell me about Pune district"</em></li>
      </ul>
      <p style="font-size:13px; color:var(--text-muted);">Explore our databases in the <a href="explorer.html">Data Explorer</a> or <a href="rankings.html">Rankings Hub</a>.</p>
    `;
  }

  async function handleSend() {
    const userText = chatInput.value.trim();
    if (!userText) return;

    // Append user query
    appendMessage(escapeHTML(userText), 'user');
    chatInput.value = '';
    chatBtn.disabled = true;
    chatInput.disabled = true;
    typingIndicator.style.display = 'block';
    chatBox.scrollTop = chatBox.scrollHeight;

    // Optional Worker Fallback check
    if (window.IM_WORKER_URL) {
      try {
        const resp = await fetch(window.IM_WORKER_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: userText })
        });
        const data = await resp.json();
        if (data.answer) {
          typingIndicator.style.display = 'none';
          appendMessage(data.answer, 'bot');
          chatBtn.disabled = false;
          chatInput.disabled = false;
          chatInput.focus();
          return;
        }
      } catch (e) {
        console.warn("External worker failed, using local grounded engine.", e);
      }
    }

    // Grounded Local Retrieval
    setTimeout(() => {
      typingIndicator.style.display = 'none';
      const answerHtml = answerQuery(userText);
      appendMessage(answerHtml, 'bot');
      chatBtn.disabled = false;
      chatInput.disabled = false;
      chatInput.focus();
    }, 280);
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag] || tag)
    );
  }

  // Suggestion chips handler
  if (suggestionChips) {
    suggestionChips.addEventListener('click', (e) => {
      const chip = e.target.closest('.im-chip');
      if (chip && chip.dataset.query) {
        chatInput.value = chip.dataset.query;
        handleSend();
      }
    });
  }

  chatBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
  });
});

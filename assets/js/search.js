/**
 * IndiaMetrix Fast Global Search Engine
 * Instant indexing across States, Districts, Indicators, Rankings, Tools & Stories.
 */

(function() {
  const searchInput = document.querySelector('.search-dialog-input');
  const suggestionsList = document.querySelector('.search-suggestions');
  const searchDialog = document.getElementById('search-dialog');
  const heroSearchInput = document.querySelector('.hero .search-box input');
  const heroSearchBtn = document.querySelector('.hero .search-box button');
  const heroTryLinks = document.querySelectorAll('.hero .search-hint a');
  
  if (!searchInput || !suggestionsList) return;

  // Determine root path offset
  const path = window.location.pathname;
  let rootPrefix = '';
  if (path.includes('/states/') || path.includes('/stories/') || path.includes('/tools/')) {
    rootPrefix = '../';
  } else if (path.includes('/districts/') && path.split('/').length > 3) {
    // e.g. /districts/maharashtra/pune.html
    rootPrefix = '../../';
  } else if (path.includes('/districts/')) {
    rootPrefix = '../';
  }

  const searchIndex = [
    // Core Platform Tools & Hubs
    { title: 'India Overview', subtitle: 'National Demographics & Economy', url: 'india.html', type: 'Hub', keywords: 'india bharat national gdp population statistics' },
    { title: 'Interactive Master Tools Hub', subtitle: 'Calculators, Simulators & Projection Engines', url: 'tools/index.html', type: 'Tool', keywords: 'tools calculator simulator projection gsdp literacy power' },
    { title: 'Economic Power & Country Comparator', subtitle: 'State GSDP vs World Nations & Doubling Clock', url: 'tools/economic-comparator.html', type: 'Tool', keywords: 'economic power calculator gsdp comparator country world sovereign milestone' },
    { title: 'Demographic & Universal Literacy Projector', subtitle: 'Literacy 100% Target Year & Gender Parity Gap', url: 'tools/demographic-calculator.html', type: 'Tool', keywords: 'demographic literacy calculator projector sex ratio milestone target simulation' },
    { title: 'Data Explorer', subtitle: 'Interactive Data Matrix & Charts', url: 'explorer.html', type: 'Tool', keywords: 'explorer chart visualizer download data query' },
    { title: 'Compare States', subtitle: 'Side-by-side State Indicator Comparison', url: 'compare.html', type: 'Tool', keywords: 'compare comparison difference versus vs' },
    { title: 'State Rankings', subtitle: 'Rankings across 6 Verified Indicators', url: 'rankings.html', type: 'Hub', keywords: 'rankings highest lowest leaderboards top states' },
    { title: 'District Discovery Hub', subtitle: 'Profiles & Metrics for Indian Districts', url: 'districts/index.html', type: 'Hub', keywords: 'districts zilla city pune bengaluru lucknow ahmedabad chennai' },
    { title: 'Ask IndiaMetrix AI', subtitle: 'Natural Language Verified Data Queries', url: 'ask.html', type: 'AI', keywords: 'ask ai assistant chat questions bot nlp' },
    { title: 'Historical Trends', subtitle: 'Decadal Statistical Progression (1951-2026)', url: 'history.html', type: 'Story', keywords: 'history past timeline trends decades' },
    { title: 'India vs World', subtitle: 'Global Benchmarking with World Bank Data', url: 'world.html', type: 'Hub', keywords: 'world international china usa comparison global' },
    { title: 'Data Sources Directory', subtitle: 'Official Registry of 11+ Ministries & Agencies', url: 'sources.html', type: 'Legal', keywords: 'sources mospi census rbi niti aayog world bank data.gov.in' },
    { title: 'Methodology & Standards', subtitle: 'Data Verification & Integrity Principles', url: 'methodology.html', type: 'Legal', keywords: 'methodology verification rules transparency data governance' },

    // Rankings Shortcuts
    { title: 'Ranking: State Population', subtitle: 'Census 2011 State Population Leaderboard', url: 'rankings.html#rank-population', type: 'Ranking', keywords: 'population largest states most populated up maharashtra bihar' },
    { title: 'Ranking: Literacy Rate', subtitle: 'Highest to Lowest Literacy across States', url: 'rankings.html#rank-literacy-rate', type: 'Ranking', keywords: 'literacy education literate kerala bihar mizoram' },
    { title: 'Ranking: GSDP Economy', subtitle: 'MoSPI 2022-23 State Economic Output', url: 'rankings.html#rank-gdp', type: 'Ranking', keywords: 'gsdp gdp state economy maharashtra tamil nadu gujarat' },
    { title: 'Ranking: Lowest Unemployment Rate', subtitle: 'PLFS 2023 Employment Rankings', url: 'rankings.html#rank-unemployment-rate', type: 'Ranking', keywords: 'unemployment jobs employment plfs lowest jobless' },
    { title: 'Ranking: Sex Ratio', subtitle: 'Females per 1000 Males (Census 2011)', url: 'rankings.html#rank-sex-ratio', type: 'Ranking', keywords: 'sex ratio gender ratio females women kerala haryana' },
    { title: 'Ranking: Geographic Area', subtitle: 'Survey of India Total Land Area', url: 'rankings.html#rank-area', type: 'Ranking', keywords: 'area sq km land size rajasthan goa largest' },

    // Verified Districts
    { title: 'Pune District', subtitle: 'Maharashtra • Pop: 9.43M • Lit: 86.15%', url: 'districts/maharashtra/pune.html', type: 'District', keywords: 'pune poona maharashtra district it hub' },
    { title: 'Bengaluru Urban', subtitle: 'Karnataka • Pop: 9.62M • Lit: 87.67%', url: 'districts/karnataka/bengaluru-urban.html', type: 'District', keywords: 'bengaluru bangalore karnataka district silicon valley' },
    { title: 'Ahmedabad District', subtitle: 'Gujarat • Pop: 7.21M • Lit: 85.31%', url: 'districts/gujarat/ahmedabad.html', type: 'District', keywords: 'ahmedabad gujarat district amdavad' },
    { title: 'Chennai District', subtitle: 'Tamil Nadu • Pop: 4.65M • Lit: 90.18%', url: 'districts/tamil-nadu/chennai.html', type: 'District', keywords: 'chennai madras tamil nadu district' },
    { title: 'Lucknow District', subtitle: 'Uttar Pradesh • Pop: 4.59M • Lit: 77.29%', url: 'districts/uttar-pradesh/lucknow.html', type: 'District', keywords: 'lucknow up uttar pradesh district capital' },
    { title: 'Ernakulam District', subtitle: 'Kerala • Pop: 3.28M • Lit: 95.89%', url: 'districts/kerala/ernakulam.html', type: 'District', keywords: 'ernakulam kochi cochin kerala district' },
    { title: 'Nagpur District', subtitle: 'Maharashtra • Pop: 4.65M • Lit: 88.39%', url: 'districts/maharashtra/nagpur.html', type: 'District', keywords: 'nagpur maharashtra district' },

    // All 36 States & UTs
    { title: 'Andaman & Nicobar Islands', subtitle: 'Union Territory (अंडमान और निकोबार)', url: 'states/andaman-nicobar.html', type: 'State', keywords: 'andaman nicobar port blair ut' },
    { title: 'Andhra Pradesh', subtitle: 'State (आंध्र प्रदेश)', url: 'states/andhra-pradesh.html', type: 'State', keywords: 'andhra pradesh ap amaravati visakhapatnam' },
    { title: 'Arunachal Pradesh', subtitle: 'State (अरुणाचल प्रदेश)', url: 'states/arunachal-pradesh.html', type: 'State', keywords: 'arunachal pradesh itanagar northeast' },
    { title: 'Assam', subtitle: 'State (असम)', url: 'states/assam.html', type: 'State', keywords: 'assam asom dispur guwahati' },
    { title: 'Bihar', subtitle: 'State (बिहार)', url: 'states/bihar.html', type: 'State', keywords: 'bihar patna' },
    { title: 'Chandigarh', subtitle: 'Union Territory (चंडीगढ़)', url: 'states/chandigarh.html', type: 'State', keywords: 'chandigarh ut capital' },
    { title: 'Chhattisgarh', subtitle: 'State (छत्तीसगढ़)', url: 'states/chhattisgarh.html', type: 'State', keywords: 'chhattisgarh raipur' },
    { title: 'Dadra and Nagar Haveli and Daman and Diu', subtitle: 'Union Territory', url: 'states/dadra-nagar-haveli-daman-diu.html', type: 'State', keywords: 'daman diu dadra nagar haveli ut' },
    { title: 'Delhi (NCT)', subtitle: 'National Capital Territory (दिल्ली)', url: 'states/delhi.html', type: 'State', keywords: 'delhi new delhi nct capital' },
    { title: 'Goa', subtitle: 'State (गोवा)', url: 'states/goa.html', type: 'State', keywords: 'goa panaji panjim' },
    { title: 'Gujarat', subtitle: 'State (गुजरात)', url: 'states/gujarat.html', type: 'State', keywords: 'gujarat gandhinagar ahmedabad surat' },
    { title: 'Haryana', subtitle: 'State (हरियाणा)', url: 'states/haryana.html', type: 'State', keywords: 'haryana chandigarh gurugram' },
    { title: 'Himachal Pradesh', subtitle: 'State (हिमाचल प्रदेश)', url: 'states/himachal-pradesh.html', type: 'State', keywords: 'himachal pradesh shimla hp' },
    { title: 'Jammu & Kashmir', subtitle: 'Union Territory (जम्मू और कश्मीर)', url: 'states/jammu-kashmir.html', type: 'State', keywords: 'jammu kashmir srinagar j&k ut' },
    { title: 'Jharkhand', subtitle: 'State (झारखंड)', url: 'states/jharkhand.html', type: 'State', keywords: 'jharkhand ranchi jamshedpur' },
    { title: 'Karnataka', subtitle: 'State (कर्नाटक)', url: 'states/karnataka.html', type: 'State', keywords: 'karnataka bengaluru bangalore' },
    { title: 'Kerala', subtitle: 'State (केरल)', url: 'states/kerala.html', type: 'State', keywords: 'kerala thiruvananthapuram kochi' },
    { title: 'Ladakh', subtitle: 'Union Territory (लद्दाख)', url: 'states/ladakh.html', type: 'State', keywords: 'ladakh leh kargil ut' },
    { title: 'Lakshadweep', subtitle: 'Union Territory (लक्षद्वीप)', url: 'states/lakshadweep.html', type: 'State', keywords: 'lakshadweep kavaratti island ut' },
    { title: 'Madhya Pradesh', subtitle: 'State (मध्य प्रदेश)', url: 'states/madhya-pradesh.html', type: 'State', keywords: 'madhya pradesh mp bhopal indore' },
    { title: 'Maharashtra', subtitle: 'State (महाराष्ट्र)', url: 'states/maharashtra.html', type: 'State', keywords: 'maharashtra mumbai pune nagpur' },
    { title: 'Manipur', subtitle: 'State (मणिपुर)', url: 'states/manipur.html', type: 'State', keywords: 'manipur imphal' },
    { title: 'Meghalaya', subtitle: 'State (मेघालय)', url: 'states/meghalaya.html', type: 'State', keywords: 'meghalaya shillong' },
    { title: 'Mizoram', subtitle: 'State (मिज़ोरम)', url: 'states/mizoram.html', type: 'State', keywords: 'mizoram aizawl' },
    { title: 'Nagaland', subtitle: 'State (नागालैंड)', url: 'states/nagaland.html', type: 'State', keywords: 'nagaland kohima' },
    { title: 'Odisha', subtitle: 'State (ओडिशा)', url: 'states/odisha.html', type: 'State', keywords: 'odisha orissa bhubaneswar' },
    { title: 'Puducherry', subtitle: 'Union Territory (पुडुचेरी)', url: 'states/puducherry.html', type: 'State', keywords: 'puducherry pondicherry ut' },
    { title: 'Punjab', subtitle: 'State (पंजाब)', url: 'states/punjab.html', type: 'State', keywords: 'punjab chandigarh amritsar' },
    { title: 'Rajasthan', subtitle: 'State (राजस्थान)', url: 'states/rajasthan.html', type: 'State', keywords: 'rajasthan jaipur jodhpur' },
    { title: 'Sikkim', subtitle: 'State (सिक्किम)', url: 'states/sikkim.html', type: 'State', keywords: 'sikkim gangtok' },
    { title: 'Tamil Nadu', subtitle: 'State (तमिलनाडु)', url: 'states/tamil-nadu.html', type: 'State', keywords: 'tamil nadu tn chennai coimbatore' },
    { title: 'Telangana', subtitle: 'State (तेलंगाना)', url: 'states/telangana.html', type: 'State', keywords: 'telangana hyderabad' },
    { title: 'Tripura', subtitle: 'State (त्रिपुरा)', url: 'states/tripura.html', type: 'State', keywords: 'tripura agartala' },
    { title: 'Uttar Pradesh', subtitle: 'State (उत्तर प्रदेश)', url: 'states/uttar-pradesh.html', type: 'State', keywords: 'uttar pradesh up lucknow kanpur varanasi noida' },
    { title: 'Uttarakhand', subtitle: 'State (उत्तराखंड)', url: 'states/uttarakhand.html', type: 'State', keywords: 'uttarakhand uk dehradun' },
    { title: 'West Bengal', subtitle: 'State (पश्चिम बंगाल)', url: 'states/west-bengal.html', type: 'State', keywords: 'west bengal wb kolkata calcutta' },

    // Data Stories
    { title: "India's Changing Population", subtitle: 'Demographic Transition 1951-2026', url: 'stories/population.html', type: 'Story', keywords: 'population fertility growth story' },
    { title: "The Story of India's Literacy", subtitle: 'Educational Journey across 7 Decades', url: 'stories/literacy.html', type: 'Story', keywords: 'literacy education schools story' },
    { title: "How Indian States Compare", subtitle: 'Regional Economic & Health Disparities', url: 'stories/growth.html', type: 'Story', keywords: 'states growth comparison economy story' },
    { title: "Digital India Revolution", subtitle: 'Internet Penetration & Telecom Growth', url: 'stories/digital.html', type: 'Story', keywords: 'digital internet broadband story' }
  ];

  const defaultHTML = `
    <li><a href="${rootPrefix}india.html"><strong>India Overview</strong> <span style="float:right; font-size:11px; color:var(--text-faint);">Hub</span></a></li>
    <li><a href="${rootPrefix}rankings.html"><strong>State Rankings</strong> <span style="float:right; font-size:11px; color:var(--text-faint);">Rankings</span></a></li>
    <li><a href="${rootPrefix}districts/index.html"><strong>District Discovery Hub</strong> <span style="float:right; font-size:11px; color:var(--teal);">Districts</span></a></li>
    <li><a href="${rootPrefix}compare.html"><strong>Compare States</strong> <span style="float:right; font-size:11px; color:var(--text-faint);">Tool</span></a></li>
    <li><a href="${rootPrefix}ask.html"><strong>Ask IndiaMetrix AI</strong> <span style="float:right; font-size:11px; color:var(--teal);">Verified AI</span></a></li>
  `;

  let selectedIndex = -1;

  function getTypeBadge(type) {
    let color = 'var(--text-faint)';
    let bg = 'transparent';
    let border = 'var(--border)';

    if (type === 'District') {
      color = '#38bdf8';
      border = 'rgba(56, 189, 248, 0.3)';
      bg = 'rgba(56, 189, 248, 0.08)';
    } else if (type === 'AI') {
      color = '#34d399';
      border = 'rgba(52, 211, 153, 0.3)';
      bg = 'rgba(52, 211, 153, 0.08)';
    } else if (type === 'Ranking') {
      color = '#f59e0b';
      border = 'rgba(245, 158, 11, 0.3)';
      bg = 'rgba(245, 158, 11, 0.08)';
    } else if (type === 'Story') {
      color = '#a78bfa';
      border = 'rgba(167, 139, 250, 0.3)';
      bg = 'rgba(167, 139, 250, 0.08)';
    }

    return `<span style="float:right; font-size:11px; font-weight:600; color:${color}; background:${bg}; padding:2px 8px; border:1px solid ${border}; border-radius:4px;">${type}</span>`;
  }

  function renderResults(results) {
    selectedIndex = -1;
    const hint = document.querySelector('.search-hint');
    if (hint) {
      hint.textContent = results.length > 0 ? `Results (${results.length})` : 'No verified matches found';
    }

    if (results.length === 0) {
      suggestionsList.innerHTML = `
        <li style="padding:12px; color:var(--text-muted); font-size:14px; text-align:center;">
          No matching records. Try searching for a State, District, or Indicator (e.g. <em>Pune, Maharashtra, Literacy</em>).
        </li>
      `;
      return;
    }

    const html = results.slice(0, 10).map((r, idx) => {
      const badge = getTypeBadge(r.type);
      const targetUrl = rootPrefix + r.url;
      return `
        <li data-index="${idx}">
          <a href="${targetUrl}" style="display:block; padding:10px 14px; text-decoration:none; color:inherit;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:600; color:var(--text);">${r.title}</span>
              ${badge}
            </div>
            ${r.subtitle ? `<div style="font-size:12px; color:var(--text-muted); margin-top:2px;">${r.subtitle}</div>` : ''}
          </a>
        </li>
      `;
    }).join('');

    suggestionsList.innerHTML = html;
  }

  searchInput.addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase().trim();
    if (query.length === 0) {
      const hint = document.querySelector('.search-hint');
      if (hint) hint.textContent = 'Suggested Searches';
      suggestionsList.innerHTML = defaultHTML;
      return;
    }

    const tokens = query.split(/\s+/);
    const results = searchIndex.filter(item => {
      const haystack = `${item.title} ${item.subtitle || ''} ${item.keywords || ''}`.toLowerCase();
      return tokens.every(token => haystack.includes(token));
    });

    renderResults(results);
  });

  // Keyboard Navigation
  searchInput.addEventListener('keydown', function(e) {
    const items = suggestionsList.querySelectorAll('li a');
    if (!items.length) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = (selectedIndex + 1) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = (selectedIndex - 1 + items.length) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && items[selectedIndex]) {
        window.location.href = items[selectedIndex].href;
      } else if (items[0]) {
        window.location.href = items[0].href;
      }
    }
  });

  function updateActiveItem(items) {
    items.forEach((item, idx) => {
      const li = item.closest('li');
      if (idx === selectedIndex) {
        li.style.background = 'var(--surface-2)';
        li.style.outline = '1px solid var(--teal)';
      } else {
        li.style.background = '';
        li.style.outline = '';
      }
    });
  }

  // Dialog close and backdrop handlers
  if (searchDialog) {
    const closeBtn = searchDialog.querySelector('.search-dialog-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => searchDialog.close());
    }
    searchDialog.addEventListener('click', (e) => {
      if (e.target === searchDialog) {
        searchDialog.close();
      }
    });
  }

  // Hero Search integration
  if (heroSearchInput && searchDialog) {
    const openSearchWith = (val) => {
      if (typeof searchDialog.showModal === 'function') {
        searchDialog.showModal();
        searchInput.value = val || '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.focus();
      }
    };

    heroSearchInput.addEventListener('click', () => openSearchWith(heroSearchInput.value));
    heroSearchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        openSearchWith(heroSearchInput.value);
      }
    });

    if (heroSearchBtn) {
      heroSearchBtn.addEventListener('click', () => openSearchWith(heroSearchInput.value));
    }
  }
})();

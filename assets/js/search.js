(function() {
  const searchInput = document.querySelector('.search-dialog-input');
  const suggestionsList = document.querySelector('.search-suggestions');
  
  if (!searchInput || !suggestionsList) return;

  // Pre-defined static search index for a fast static site experience
  const searchIndex = [
    { title: 'India Overview', url: 'india.html', type: 'page' },
    { title: 'Data Explorer', url: 'explorer.html', type: 'page' },
    { title: 'Compare States', url: 'compare.html', type: 'page' },
    { title: 'State Rankings', url: 'rankings.html', type: 'page' },
    
    // States
    { title: 'Andaman and Nicobar Islands', url: 'states/andaman-nicobar.html', type: 'state' },
    { title: 'Andhra Pradesh', url: 'states/andhra-pradesh.html', type: 'state' },
    { title: 'Arunachal Pradesh', url: 'states/arunachal-pradesh.html', type: 'state' },
    { title: 'Assam', url: 'states/assam.html', type: 'state' },
    { title: 'Bihar', url: 'states/bihar.html', type: 'state' },
    { title: 'Chandigarh', url: 'states/chandigarh.html', type: 'state' },
    { title: 'Chhattisgarh', url: 'states/chhattisgarh.html', type: 'state' },
    { title: 'Dadra and Nagar Haveli and Daman and Diu', url: 'states/dadra-nagar-haveli-daman-diu.html', type: 'state' },
    { title: 'Delhi', url: 'states/delhi.html', type: 'state' },
    { title: 'Goa', url: 'states/goa.html', type: 'state' },
    { title: 'Gujarat', url: 'states/gujarat.html', type: 'state' },
    { title: 'Haryana', url: 'states/haryana.html', type: 'state' },
    { title: 'Himachal Pradesh', url: 'states/himachal-pradesh.html', type: 'state' },
    { title: 'Jammu and Kashmir', url: 'states/jammu-kashmir.html', type: 'state' },
    { title: 'Jharkhand', url: 'states/jharkhand.html', type: 'state' },
    { title: 'Karnataka', url: 'states/karnataka.html', type: 'state' },
    { title: 'Kerala', url: 'states/kerala.html', type: 'state' },
    { title: 'Ladakh', url: 'states/ladakh.html', type: 'state' },
    { title: 'Lakshadweep', url: 'states/lakshadweep.html', type: 'state' },
    { title: 'Madhya Pradesh', url: 'states/madhya-pradesh.html', type: 'state' },
    { title: 'Maharashtra', url: 'states/maharashtra.html', type: 'state' },
    { title: 'Manipur', url: 'states/manipur.html', type: 'state' },
    { title: 'Meghalaya', url: 'states/meghalaya.html', type: 'state' },
    { title: 'Mizoram', url: 'states/mizoram.html', type: 'state' },
    { title: 'Nagaland', url: 'states/nagaland.html', type: 'state' },
    { title: 'Odisha', url: 'states/odisha.html', type: 'state' },
    { title: 'Puducherry', url: 'states/puducherry.html', type: 'state' },
    { title: 'Punjab', url: 'states/punjab.html', type: 'state' },
    { title: 'Rajasthan', url: 'states/rajasthan.html', type: 'state' },
    { title: 'Sikkim', url: 'states/sikkim.html', type: 'state' },
    { title: 'Tamil Nadu', url: 'states/tamil-nadu.html', type: 'state' },
    { title: 'Telangana', url: 'states/telangana.html', type: 'state' },
    { title: 'Tripura', url: 'states/tripura.html', type: 'state' },
    { title: 'Uttar Pradesh', url: 'states/uttar-pradesh.html', type: 'state' },
    { title: 'Uttarakhand', url: 'states/uttarakhand.html', type: 'state' },
    { title: 'West Bengal', url: 'states/west-bengal.html', type: 'state' },
    
    // Stories
    { title: "India's Changing Population", url: 'stories/population.html', type: 'story' },
    { title: "The Story of India's Literacy", url: 'stories/literacy.html', type: 'story' },
    { title: "How Indian States Compare", url: 'stories/growth.html', type: 'story' },
    { title: "Digital India", url: 'stories/digital.html', type: 'story' }
  ];

  const defaultHTML = `
      <li><a href="india.html">India Overview</a></li>
      <li><a href="explorer.html">Data Explorer</a></li>
      <li><a href="compare.html">Compare States</a></li>
      <li><a href="rankings.html">State Rankings</a></li>
  `;

  searchInput.addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase().trim();
    
    if (query.length === 0) {
      document.querySelector('.search-hint').textContent = 'Suggested Searches';
      suggestionsList.innerHTML = defaultHTML;
      return;
    }

    const results = searchIndex.filter(item => item.title.toLowerCase().includes(query));
    
    document.querySelector('.search-hint').textContent = results.length > 0 ? 'Search Results' : 'No results found';
    
    if (results.length === 0) {
      suggestionsList.innerHTML = '';
      return;
    }

    const html = results.map(r => {
      // Small badge logic
      let badge = '';
      if (r.type === 'state') badge = '<span style="float:right; font-size:11px; color:var(--text-faint); padding:2px 6px; border:1px solid var(--border); border-radius:4px;">State</span>';
      if (r.type === 'story') badge = '<span style="float:right; font-size:11px; color:var(--teal); padding:2px 6px; border:1px solid var(--teal-soft); background:var(--teal-soft); border-radius:4px;">Story</span>';
      
      return \`<li><a href="\${r.url}">\${r.title} \${badge}</a></li>\`;
    }).join('');
    
    suggestionsList.innerHTML = html;
  });

  // Handle enter key to go to first result
  searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      const firstLink = suggestionsList.querySelector('a');
      if (firstLink) {
        window.location.href = firstLink.href;
      }
    }
  });
})();

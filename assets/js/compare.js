(function () {
  "use strict";

  var statesList = [
    {"id": "andaman-nicobar", "en": "Andaman & Nicobar", "hi": "अंडमान और निकोबार"},
    {"id": "andhra-pradesh", "en": "Andhra Pradesh", "hi": "आंध्र प्रदेश"},
    {"id": "arunachal-pradesh", "en": "Arunachal Pradesh", "hi": "अरुणाचल प्रदेश"},
    {"id": "assam", "en": "Assam", "hi": "असम"},
    {"id": "bihar", "en": "Bihar", "hi": "बिहार"},
    {"id": "chandigarh", "en": "Chandigarh", "hi": "चंडीगढ़"},
    {"id": "chhattisgarh", "en": "Chhattisgarh", "hi": "छत्तीसगढ़"},
    {"id": "dadra-nagar-haveli-daman-diu", "en": "Dadra & Nagar Haveli and Daman & Diu", "hi": "दादरा और नगर हवेली तथा दमन और दीव"},
    {"id": "delhi", "en": "Delhi", "hi": "दिल्ली"},
    {"id": "goa", "en": "Goa", "hi": "गोवा"},
    {"id": "gujarat", "en": "Gujarat", "hi": "गुजरात"},
    {"id": "haryana", "en": "Haryana", "hi": "हरियाणा"},
    {"id": "himachal-pradesh", "en": "Himachal Pradesh", "hi": "हिमाचल प्रदेश"},
    {"id": "jammu-kashmir", "en": "Jammu & Kashmir", "hi": "जम्मू और कश्मीर"},
    {"id": "jharkhand", "en": "Jharkhand", "hi": "झारखंड"},
    {"id": "karnataka", "en": "Karnataka", "hi": "कर्नाटक"},
    {"id": "kerala", "en": "Kerala", "hi": "केरल"},
    {"id": "ladakh", "en": "Ladakh", "hi": "लद्दाख"},
    {"id": "lakshadweep", "en": "Lakshadweep", "hi": "लक्षद्वीप"},
    {"id": "madhya-pradesh", "en": "Madhya Pradesh", "hi": "मध्य प्रदेश"},
    {"id": "maharashtra", "en": "Maharashtra", "hi": "महाराष्ट्र"},
    {"id": "manipur", "en": "Manipur", "hi": "मणिपुर"},
    {"id": "meghalaya", "en": "Meghalaya", "hi": "मेघालय"},
    {"id": "mizoram", "en": "Mizoram", "hi": "मिज़ोरम"},
    {"id": "nagaland", "en": "Nagaland", "hi": "नागालैंड"},
    {"id": "odisha", "en": "Odisha", "hi": "ओडिशा"},
    {"id": "puducherry", "en": "Puducherry", "hi": "पुडुचेरी"},
    {"id": "punjab", "en": "Punjab", "hi": "पंजाब"},
    {"id": "rajasthan", "en": "Rajasthan", "hi": "राजस्थान"},
    {"id": "sikkim", "en": "Sikkim", "hi": "सिक्किम"},
    {"id": "tamil-nadu", "en": "Tamil Nadu", "hi": "तमिलनाडु"},
    {"id": "telangana", "en": "Telangana", "hi": "तेलंगाना"},
    {"id": "tripura", "en": "Tripura", "hi": "त्रिपुरा"},
    {"id": "uttar-pradesh", "en": "Uttar Pradesh", "hi": "उत्तर प्रदेश"},
    {"id": "uttarakhand", "en": "Uttarakhand", "hi": "उत्तराखंड"},
    {"id": "west-bengal", "en": "West Bengal", "hi": "पश्चिम बंगाल"}
  ];

  var select1 = document.getElementById("state1");
  var select2 = document.getElementById("state2");
  var compareBtn = document.getElementById("compareBtn");
  var resultsDiv = document.getElementById("compare-results");
  var errorEl = document.getElementById("compare-error");

  function populateSelect(selectEl) {
    statesList.forEach(function(st) {
      var opt = document.createElement("option");
      opt.value = st.id;
      opt.setAttribute("data-en", st.en);
      opt.setAttribute("data-hi", st.hi);
      var lang = document.documentElement.getAttribute("data-lang") || "en";
      opt.textContent = lang === "hi" ? st.hi : st.en;
      selectEl.appendChild(opt);
    });
  }

  if (select1 && select2) {
    populateSelect(select1);
    populateSelect(select2);
  }

  function getIndicator(stateData, indId) {
    var inds = stateData.indicators || [];
    for (var i = 0; i < inds.length; i++) {
      if (inds[i].id === indId) return inds[i];
    }
    return null;
  }

  function renderStateCard(stateData, otherStateData) {
    var sNameEn = stateData.name.en || "";
    var sNameHi = stateData.name.hi || "";

    var indConfigs = [
      { id: "population", nameEn: "Population", nameHi: "जनसंख्या", dir: "neutral" },
      { id: "literacy-rate", nameEn: "Literacy Rate", nameHi: "साक्षरता दर", dir: "higher_is_better" },
      { id: "gdp", nameEn: "GSDP (Current Prices)", nameHi: "GSDP (वर्तमान मूल्य)", dir: "higher_is_better" },
      { id: "unemployment", nameEn: "Unemployment Rate", nameHi: "बेरोजगारी दर", dir: "lower_is_better" },
      { id: "health", nameEn: "Infant Mortality Rate (IMR)", nameHi: "शिशु मृत्यु दर", dir: "lower_is_better" },
      { id: "sex-ratio", nameEn: "Sex Ratio", nameHi: "लिंगानुपात", dir: "higher_is_better" },
      { id: "area", nameEn: "Geographical Area", nameHi: "भौगोलिक क्षेत्रफल", dir: "neutral" }
    ];
    
    var html = '<div class="compare-card" style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-m); padding:24px; box-shadow:var(--shadow-card);">';
    html += '<h2 class="compare-state-name" style="font-family:var(--font-display); font-size:24px; color:var(--text); margin-bottom:18px; border-bottom:1px solid var(--border); padding-bottom:12px;" data-en="' + sNameEn + '" data-hi="' + sNameHi + '">' + sNameEn + '</h2>';

    indConfigs.forEach(function(cfg) {
      var ind1 = getIndicator(stateData, cfg.id);
      var ind2 = getIndicator(otherStateData, cfg.id);

      if (ind1) {
        var nameEn = ind1.name.en || cfg.nameEn;
        var nameHi = ind1.name.hi || cfg.nameHi;
        var dispEn = ind1.display.en;
        var dispHi = ind1.display.hi;
        var year = ind1.year || "";
        
        var diffHtml = "";
        if (ind2 && ind1.value !== null && ind2.value !== null) {
          var v1 = ind1.value;
          var v2 = ind2.value;
          
          if (v1 !== v2) {
            var isBetter = false;
            if (cfg.dir === "higher_is_better") {
              isBetter = (v1 > v2);
            } else if (cfg.dir === "lower_is_better") {
              isBetter = (v1 < v2);
            }

            if (cfg.dir !== "neutral") {
              var badgeClass = isBetter ? "im-badge--verified" : "im-badge--source";
              var badgeText = isBetter ? "Favorable" : "Lower";
              diffHtml = ' <span class="im-badge ' + badgeClass + '" style="font-size:11px;">' + badgeText + '</span>';
            }
          }
        }

        html += '<div class="ind-row" style="padding:10px 0; border-bottom:1px solid var(--border);">';
        html += '<p class="ind-label" style="font-size:13px; color:var(--text-muted); margin:0 0 4px;" data-en="' + nameEn + '" data-hi="' + nameHi + '">' + nameEn + '</p>';
        html += '<p style="margin:0; display:flex; justify-content:space-between; align-items:center;">';
        html += '<span class="ind-val" style="font-family:var(--font-mono); font-weight:600; font-size:16px; color:var(--text);" data-en="' + dispEn + '" data-hi="' + dispHi + '">' + dispEn + '</span>';
        html += diffHtml;
        html += '</p>';
        html += '<span style="font-size:11px; font-family:var(--font-mono); color:var(--text-faint);">Ref: ' + year + '</span>';
        html += '</div>';
      }
    });

    html += '<div style="margin-top:20px; text-align:center;">';
    html += '<a href="states/' + stateData.id + '.html" class="im-btn im-btn-sm im-btn-outline" style="width:100%;" data-en="View ' + sNameEn + ' Profile →" data-hi="' + sNameHi + ' प्रोफ़ाइल देखें →">View ' + sNameEn + ' Profile →</a>';
    html += '</div>';

    html += '</div>';
    return html;
  }

  function executeCompare(id1, id2) {
    if (!id1 || !id2) return;
    
    errorEl.style.display = "none";
    resultsDiv.style.display = "none";

    Promise.all([
      fetch("data/indicators/states/" + id1 + ".json").then(res => res.json()),
      fetch("data/indicators/states/" + id2 + ".json").then(res => res.json())
    ])
    .then(function(data) {
      var state1Data = data[0];
      var state2Data = data[1];

      var html = renderStateCard(state1Data, state2Data) + renderStateCard(state2Data, state1Data);
      resultsDiv.innerHTML = html;
      resultsDiv.style.display = "grid";

      var rootLang = document.documentElement.getAttribute("data-lang") || "en";
      document.querySelectorAll("#compare-results [data-en]").forEach(function(el) {
         var val = rootLang === "hi" ? el.getAttribute("data-hi") : el.getAttribute("data-en");
         if (val) el.textContent = val;
      });

      // Update URL without page reload
      var newUrl = window.location.pathname + "?s1=" + id1 + "&s2=" + id2;
      window.history.replaceState({path: newUrl}, "", newUrl);
    })
    .catch(function(err) {
      console.error(err);
      errorEl.style.display = "block";
    });
  }

  if (compareBtn) {
    compareBtn.addEventListener("click", function () {
      executeCompare(select1.value, select2.value);
    });
  }

  // Prepopulate from URL parameters if present
  document.addEventListener("DOMContentLoaded", function () {
    var params = new URLSearchParams(window.location.search);
    var s1 = params.get("s1");
    var s2 = params.get("s2");
    if (s1 && s2 && select1 && select2) {
      select1.value = s1;
      select2.value = s2;
      executeCompare(s1, s2);
    }
  });

})();

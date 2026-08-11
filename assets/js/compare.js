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

    var indIds = ["population", "literacy-rate"];
    
    var html = '<div class="compare-card">';
    html += '<h2 class="compare-state-name" data-en="' + sNameEn + '" data-hi="' + sNameHi + '">' + sNameEn + '</h2>';

    indIds.forEach(function(indId) {
      var ind1 = getIndicator(stateData, indId);
      var ind2 = getIndicator(otherStateData, indId);

      if (ind1) {
        var nameEn = ind1.name.en;
        var nameHi = ind1.name.hi;
        var dispEn = ind1.display.en;
        var dispHi = ind1.display.hi;
        
        var diffHtml = "";
        if (ind2) {
          // Compare values
          var v1 = ind1.value;
          var v2 = ind2.value;
          
          if (v1 > v2) {
             var diffClass = (indId === "literacy-rate") ? "diff-better" : "";
             diffHtml = '<span class="diff-val ' + diffClass + '">Higher</span>';
          } else if (v1 < v2) {
             var diffClass2 = (indId === "literacy-rate") ? "diff-worse" : "";
             diffHtml = '<span class="diff-val ' + diffClass2 + '">Lower</span>';
          }
        }

        html += '<div class="ind-row">';
        html += '<p class="ind-label" data-en="' + nameEn + '" data-hi="' + nameHi + '">' + nameEn + '</p>';
        html += '<p><span class="ind-val" data-en="' + dispEn + '" data-hi="' + dispHi + '">' + dispEn + '</span>' + diffHtml + '</p>';
        html += '</div>';
      }
    });

    html += '</div>';
    return html;
  }

  if (compareBtn) {
    compareBtn.addEventListener("click", function () {
      var id1 = select1.value;
      var id2 = select2.value;
      
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

        // trigger lang switch logic on newly injected DOM if needed
        var rootLang = document.documentElement.getAttribute("data-lang") || "en";
        document.querySelectorAll("#compare-results [data-en]").forEach(function(el) {
           var val = rootLang === "hi" ? el.getAttribute("data-hi") : el.getAttribute("data-en");
           if (val) el.textContent = val;
        });

      })
      .catch(function(err) {
        console.error(err);
        errorEl.style.display = "block";
      });
    });
  }

})();

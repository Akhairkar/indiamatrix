(function () {
  "use strict";

  /* ---------- Language switching ---------- */
  var langButtons = document.querySelectorAll("[data-set-lang]");
  var root = document.documentElement;

  function applyLang(lang) {
    root.setAttribute("lang", lang === "hi" ? "hi" : "en");
    root.setAttribute("data-lang", lang);

    document.querySelectorAll("[data-en]").forEach(function (el) {
      var val = lang === "hi" ? el.getAttribute("data-hi") : el.getAttribute("data-en");
      if (val !== null) el.textContent = val;
    });

    document.querySelectorAll("[data-en-placeholder]").forEach(function (el) {
      var val = lang === "hi" ? el.getAttribute("data-hi-placeholder") : el.getAttribute("data-en-placeholder");
      if (val !== null) el.setAttribute("placeholder", val);
    });

    langButtons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-set-lang") === lang);
    });

    try { localStorage.setItem("im-lang", lang); } catch (e) {}
  }

  langButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyLang(btn.getAttribute("data-set-lang"));
    });
  });

  var savedLang = null;
  try { savedLang = localStorage.getItem("im-lang"); } catch (e) {}
  if (savedLang === "hi") applyLang("hi");

  /* ---------- Mobile nav ---------- */
  var hamburger = document.getElementById("hamburger");
  var mainNav = document.getElementById("main-nav");

  if (hamburger && mainNav) {
    hamburger.addEventListener("click", function () {
      var isOpen = mainNav.classList.toggle("is-open");
      hamburger.setAttribute("aria-expanded", String(isOpen));
    });

    mainNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mainNav.classList.remove("is-open");
        hamburger.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---------- Category cards (18 planned categories) ---------- */
  var categories = [
    { icon: "📊", en: "Economy", hi: "अर्थव्यवस्था", enDesc: "GDP, growth, trade and inflation.", hiDesc: "जीडीपी, विकास, व्यापार और महंगाई।" },
    { icon: "👥", en: "Population", hi: "जनसंख्या", enDesc: "Census, density and demographics.", hiDesc: "जनगणना, घनत्व और जनसांख्यिकी।" },
    { icon: "🎓", en: "Education", hi: "शिक्षा", enDesc: "Literacy, enrolment and outcomes.", hiDesc: "साक्षरता, नामांकन और परिणाम।" },
    { icon: "🏥", en: "Healthcare", hi: "स्वास्थ्य", enDesc: "Life expectancy, access and outcomes.", hiDesc: "जीवन प्रत्याशा, पहुंच और परिणाम।" },
    { icon: "💼", en: "Employment", hi: "रोज़गार", enDesc: "Jobs, wages and labour force data.", hiDesc: "रोज़गार, वेतन और श्रम बल डेटा।" },
    { icon: "🌾", en: "Agriculture", hi: "कृषि", enDesc: "Crops, yield and rural livelihoods.", hiDesc: "फसलें, उपज और ग्रामीण आजीविका।" },
    { icon: "🏗️", en: "Infrastructure", hi: "बुनियादी ढांचा", enDesc: "Roads, housing and connectivity.", hiDesc: "सड़कें, आवास और कनेक्टिविटी।" },
    { icon: "⚡", en: "Energy", hi: "ऊर्जा", enDesc: "Power generation, access and mix.", hiDesc: "बिजली उत्पादन, पहुंच और मिश्रण।" },
    { icon: "🌳", en: "Environment", hi: "पर्यावरण", enDesc: "Emissions, forests and air quality.", hiDesc: "उत्सर्जन, वन और वायु गुणवत्ता।" },
    { icon: "🛡️", en: "Crime & Safety", hi: "अपराध व सुरक्षा", enDesc: "Crime rates and public safety.", hiDesc: "अपराध दर और सार्वजनिक सुरक्षा।" },
    { icon: "👶", en: "Women & Children", hi: "महिला व बच्चे", enDesc: "Health, safety and welfare indicators.", hiDesc: "स्वास्थ्य, सुरक्षा और कल्याण संकेतक।" },
    { icon: "🤝", en: "Social Development", hi: "सामाजिक विकास", enDesc: "Human development and welfare.", hiDesc: "मानव विकास और कल्याण।" },
    { icon: "📱", en: "Digital India", hi: "डिजिटल इंडिया", enDesc: "Internet, mobile and digital access.", hiDesc: "इंटरनेट, मोबाइल और डिजिटल पहुंच।" },
    { icon: "🏦", en: "Banking & Finance", hi: "बैंकिंग व वित्त", enDesc: "Credit, inclusion and markets.", hiDesc: "ऋण, समावेशन और बाज़ार।" },
    { icon: "🏛️", en: "Government & Governance", hi: "सरकार व शासन", enDesc: "Budgets, policy and administration.", hiDesc: "बजट, नीति और प्रशासन।" },
    { icon: "🗺️", en: "States & Districts", hi: "राज्य व ज़िले", enDesc: "Regional profiles across India.", hiDesc: "भारत भर के क्षेत्रीय प्रोफ़ाइल।" },
    { icon: "🌍", en: "India vs World", hi: "भारत बनाम विश्व", enDesc: "Global rankings and benchmarks.", hiDesc: "वैश्विक रैंकिंग और मानक।" },
    { icon: "📈", en: "Poverty", hi: "गरीबी", enDesc: "Income, deprivation and inequality.", hiDesc: "आय, अभाव और असमानता।" }
  ];

  var grid = document.getElementById("category-grid");
  if (grid) {
    var lang = root.getAttribute("data-lang") || "en";
    var html = categories.map(function (c) {
      return (
        '<article class="category-card">' +
          '<span class="category-icon" aria-hidden="true">' + c.icon + '</span>' +
          '<h3 data-en="' + c.en + '" data-hi="' + c.hi + '">' + c.en + '</h3>' +
          '<p data-en="' + c.enDesc + '" data-hi="' + c.hiDesc + '">' + c.enDesc + '</p>' +
          '<span class="category-cta" data-en="Explore →" data-hi="एक्सप्लोर करें →">Explore →</span>' +
        '</article>'
      );
    }).join("");
    grid.innerHTML = html;

    if (lang === "hi") applyLang("hi");
  }
})();

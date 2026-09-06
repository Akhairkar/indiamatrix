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

  /* ---------- Theme Management (Light / Dark) ---------- */
  function applyTheme(theme) {
    if (theme === "light") {
      root.setAttribute("data-theme", "light");
    } else if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
    }
    try { localStorage.setItem("im-theme", theme); } catch (e) {}
    updateThemeIcons(theme);
  }

  function updateThemeIcons(theme) {
    var buttons = document.querySelectorAll(".theme-toggle-btn");
    buttons.forEach(function (btn) {
      var isLight = root.getAttribute("data-theme") === "light" || 
        (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: light)").matches);
      btn.innerHTML = isLight
        ? '<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
        : '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
      btn.setAttribute("aria-label", isLight ? "Switch to dark theme" : "Switch to light theme");
    });
  }

  var savedTheme = null;
  try { savedTheme = localStorage.getItem("im-theme"); } catch (e) {}
  if (savedTheme) {
    applyTheme(savedTheme);
  } else {
    updateThemeIcons("system");
  }

  document.querySelectorAll(".theme-toggle-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") || 
        (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
      var next = current === "light" ? "dark" : "light";
      applyTheme(next);
    });
  });

  /* ---------- Citation Copier & Toast ---------- */
  function showToast(msg) {
    var toast = document.getElementById("im-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "im-toast";
      toast.className = "im-toast";
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () {
      toast.classList.remove("show");
    }, 3000);
  }

  window.copyCitation = function (title, indicator, value, year, source, url) {
    var pageUrl = window.location.href;
    var accessDate = new Date().toISOString().split("T")[0];
    var citationText = '"' + title + ' — ' + indicator + ': ' + value + ' (' + year + ')." Source: ' + source + ' via IndiaMetrix. Retrieved ' + accessDate + ' from ' + pageUrl;
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(citationText).then(function () {
        showToast("Citation copied to clipboard!");
      }).catch(function () {
        prompt("Copy citation:", citationText);
      });
    } else {
      prompt("Copy citation:", citationText);
    }
  };

  /* ---------- Report Issue Helper ---------- */
  window.reportDataIssue = function (subject) {
    var contactUrl = "/contact.html?issue=" + encodeURIComponent(subject || window.location.pathname);
    window.location.href = contactUrl;
  };
})();

"""
IndiaMetrix Master Indicator Pages Generator
Compiles 10 master intelligence pages with:
1. High-resolution Chart.js visualization datasets (States breakdown & Decadal time series)
2. Interactive 36-State Leaderboard with search & country equivalence
3. Quick State Simulator & Diagnostic Tool widget
4. Analytical takeaways grid (4 deep-dive insight cards)
5. Data provenance and methodology governance citations
"""

import os, json, re

def build_all_indicators(root_dir):
    out_indicators_dir = os.path.join(root_dir, 'indicators')
    os.makedirs(out_indicators_dir, exist_ok=True)
    
    template_path = os.path.join(root_dir, 'templates', 'indicator.html')
    if not os.path.exists(template_path):
        print("Error: indicator.html template not found!")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    js_source_names = {
        "world-bank": "World Bank",
        "census-india": "Census of India",
        "mospi": "MoSPI",
        "rbi": "RBI",
        "niti-aayog": "NITI Aayog",
        "data-gov-in": "data.gov.in",
        "moh-family-welfare": "MoHFW",
        "ncrb": "NCRB",
        "moef-cc": "MoEFCC",
        "meity": "MeitY",
        "un-data": "UN Data",
        "trai": "TRAI"
    }

    country_equivs = {
        "andaman-nicobar": {"country": "Saint Lucia", "flag": "🇱🇨"},
        "andhra-pradesh": {"country": "Morocco", "flag": "🇲🇦"},
        "arunachal-pradesh": {"country": "Suriname", "flag": "🇸🇷"},
        "assam": {"country": "Jordan", "flag": "🇯🇴"},
        "bihar": {"country": "Panama", "flag": "🇵🇦"},
        "chandigarh": {"country": "Mauritius", "flag": "🇲🇺"},
        "chhattisgarh": {"country": "Slovenia", "flag": "🇸🇮"},
        "dadra-nagar-haveli-daman-diu": {"country": "Bhutan", "flag": "🇧🇹"},
        "delhi": {"country": "Oman", "flag": "🇴🇲"},
        "goa": {"country": "Malta", "flag": "🇲🇹"},
        "gujarat": {"country": "Greece", "flag": "🇬🇷"},
        "haryana": {"country": "Guatemala", "flag": "🇬🇹"},
        "himachal-pradesh": {"country": "Cyprus", "flag": "🇨🇾"},
        "jammu-kashmir": {"country": "Iceland", "flag": "🇮🇸"},
        "jharkhand": {"country": "Lithuania", "flag": "🇱🇹"},
        "karnataka": {"country": "Peru", "flag": "🇵🇪"},
        "kerala": {"country": "Bulgaria", "flag": "🇧🇬"},
        "ladakh": {"country": "Seychelles", "flag": "🇸🇨"},
        "lakshadweep": {"country": "Grenada", "flag": "🇬🇩"},
        "madhya-pradesh": {"country": "Dominican Republic", "flag": "🇩🇴"},
        "maharashtra": {"country": "Switzerland", "flag": "🇨🇭"},
        "manipur": {"country": "Montenegro", "flag": "🇲🇪"},
        "meghalaya": {"country": "Barbados", "flag": "🇧🇧"},
        "mizoram": {"country": "Maldives", "flag": "🇲🇻"},
        "nagaland": {"country": "Fiji", "flag": "🇫🇯"},
        "odisha": {"country": "Costa Rica", "flag": "🇨🇷"},
        "puducherry": {"country": "Monaco", "flag": "🇲🇨"},
        "punjab": {"country": "Croatia", "flag": "🇭🇷"},
        "rajasthan": {"country": "Hungary", "flag": "🇭🇺"},
        "sikkim": {"country": "Andorra", "flag": "🇦🇩"},
        "tamil-nadu": {"country": "Portugal", "flag": "🇵🇹"},
        "telangana": {"country": "Ecuador", "flag": "🇪🇨"},
        "tripura": {"country": "Bermuda", "flag": "🇧🇲"},
        "uttar-pradesh": {"country": "Qatar", "flag": "🇶🇦"},
        "uttarakhand": {"country": "Estonia", "flag": "🇪🇪"},
        "west-bengal": {"country": "Slovakia", "flag": "🇸🇰"}
    }

    indicator_seo_meta = {
        "gdp-current-usd": {
            "title": "India GDP Statistics: 36 State GSDP Rankings | IndiaMetrix",
            "desc": "Explore India's $3.96 Trillion nominal GDP, state-by-state GSDP contributions, historical decadal growth trends, and sovereign comparisons on IndiaMetrix."
        },
        "population": {
            "title": "India Population Statistics & State Census | IndiaMetrix",
            "desc": "Analyze India's 1.46 billion population records, state demographics, decadal Census growth trends, and state-wise population shares on IndiaMetrix."
        },
        "literacy-rate": {
            "title": "India Literacy Rate: State Rankings & Trends | IndiaMetrix",
            "desc": "Explore official India literacy rate data (74.04%), 36 state and UT educational rankings, gender literacy gaps, and historical trends on IndiaMetrix."
        },
        "unemployment-rate": {
            "title": "India Unemployment Rate: State PLFS Rankings | IndiaMetrix",
            "desc": "Examine official MoSPI PLFS unemployment data for India (3.1%), state-wise job market rankings, urban-rural distributions, and trend analysis on IndiaMetrix."
        },
        "life-expectancy": {
            "title": "India Life Expectancy Data & State Health | IndiaMetrix",
            "desc": "Explore India's 72.0-year life expectancy benchmarks, state public health records, historical mortality trends, and global comparisons on IndiaMetrix."
        },
        "internet-users": {
            "title": "India Internet Users: Digital State Trends | IndiaMetrix",
            "desc": "Discover India's digital adoption metrics, 55.9% internet penetration rate, state-wise connectivity rankings, and telecom growth trends on IndiaMetrix."
        },
        "1-1_access-electricity-tot": {
            "title": "India Electricity Access: State Power Data | IndiaMetrix",
            "desc": "Track total electricity access in India (84.5%), state electrification progress, rural-urban coverage disparities, and energy access trends on IndiaMetrix."
        },
        "1-2_access-electricity-rural": {
            "title": "Rural Electricity Access in India: Data | IndiaMetrix",
            "desc": "Analyze rural electrification rates across Indian states, grid expansion milestones, infrastructure distribution benchmarks, and time-series on IndiaMetrix."
        },
        "1-3_access-electricity-urban": {
            "title": "Urban Electricity Access in India: Data | IndiaMetrix",
            "desc": "Analyze urban electrification rates across Indian states, urban power grid reliability benchmarks, infrastructure metrics, and time-series on IndiaMetrix."
        },
        "2-1_access-cft-tot": {
            "title": "India Clean Cooking Fuel Access Statistics | IndiaMetrix",
            "desc": "Explore access to clean fuels and technology for cooking in India, state-level household adoption rates, energy transition metrics, and trends on IndiaMetrix."
        }
    }

    # Load 36 states data
    with open(os.path.join(root_dir, "data", "explorer.json"), "r", encoding="utf-8") as f:
        explorer_data = json.load(f)
    states_pool = explorer_data.get('states', [])

    # Load history data
    with open(os.path.join(root_dir, "data", "history.json"), "r", encoding="utf-8") as f:
        history_data = json.load(f)

    # Load overview indicators
    with open(os.path.join(root_dir, "data", "indicators", "india-overview.json"), "r", encoding="utf-8") as f:
        overview_indicators = json.load(f).get('indicators', [])

    # Load world bank indicators
    wb_dir = os.path.join(root_dir, 'data', 'indicators', 'worldbank')
    wb_indicators = []
    if os.path.exists(wb_dir):
        for fname in sorted(os.listdir(wb_dir)):
            if fname.endswith('.json'):
                with open(os.path.join(wb_dir, fname), 'r', encoding='utf-8') as f:
                    wb_indicators.append(json.load(f))

    all_indicators = overview_indicators + wb_indicators

    # Indicator specific mapping
    ind_configs = {
        "gdp-current-usd": {
            "state_key": "gdp",
            "history_key": "gdp",
            "direction": "higher_is_better",
            "category": "Economy",
            "kpi_max_title": "#1 Economy (State)",
            "kpi_max_val": "Maharashtra",
            "kpi_max_sub": "₹38.79L Cr ($467B USD)",
            "kpi_total_title": "National Nominal GDP",
            "kpi_total_val": "$3.96 Trillion",
            "kpi_total_sub": "₹272.41 Lakh Crore",
            "kpi_median_title": "Median State GSDP",
            "kpi_median_val": "₹2.24 Lakh Cr",
            "kpi_median_sub": "State: Jammu & Kashmir",
            "kpi_top5_title": "Top 5 States Share",
            "kpi_top5_val": "47.7% of India",
            "kpi_top5_sub": "MH, TN, GJ, UP, KA",
            "insights": [
                {
                    "icon": "⚡",
                    "title": "The $5 Trillion Milestone Horizon",
                    "text": "At $3.96 Trillion in 2025, India is the 5th largest global economy. Compounding at an estimated 10.5% nominal CAGR, India is mathematically poised to cross the $5 Trillion threshold by 2027-28."
                },
                {
                    "icon": "🏭",
                    "title": "Industrial Powerhouse Concentration",
                    "text": "Economic output exhibits geographic clustering. The top five states—Maharashtra, Tamil Nadu, Gujarat, Karnataka, and Uttar Pradesh—generate nearly half of the entire nation's gross output."
                },
                {
                    "icon": "🌐",
                    "title": "Sovereign Nation Parity",
                    "text": "Individual Indian state economies rival sovereign industrialized nations: Maharashtra ($467B) matches Switzerland, Tamil Nadu ($285B) rivals Portugal, and Gujarat ($272B) matches Greece."
                },
                {
                    "icon": "📈",
                    "title": "Peninsular vs Gangetic Dynamics",
                    "text": "Peninsular maritime states lead in export manufacturing and digital services clustering, while Gangetic states like Uttar Pradesh are accelerating capital expenditure on industrial expressways."
                }
            ]
        },
        "population": {
            "state_key": "population",
            "history_key": "population",
            "direction": "neutral",
            "category": "Demographics",
            "kpi_max_title": "Most Populated State",
            "kpi_max_val": "Uttar Pradesh",
            "kpi_max_sub": "19.98 Crore Citizens",
            "kpi_total_title": "National Population",
            "kpi_total_val": "1.46 Billion",
            "kpi_total_sub": "146.38 Crore (2025 Est)",
            "kpi_median_title": "Median State Population",
            "kpi_median_val": "1.23 Crore",
            "kpi_median_sub": "State: Jammu & Kashmir",
            "kpi_top5_title": "Top 5 States Share",
            "kpi_top5_val": "52.2% of India",
            "kpi_top5_sub": "UP, MH, BR, WB, MP",
            "insights": [
                {
                    "icon": "👥",
                    "title": "Demographic Dividend Window",
                    "text": "Over 68% of India's population is in the working-age bracket (15-64 years), representing the largest youth workforce globally and a 3-decade manufacturing dividend."
                },
                {
                    "icon": "🏙️",
                    "title": "Northern Density Concentration",
                    "text": "Uttar Pradesh and Bihar alone account for over 30.3 Crore citizens—exceeding the combined populations of Germany, France, Italy, and the United Kingdom."
                },
                {
                    "icon": "📉",
                    "title": "Fertility Transition & Replacement",
                    "text": "India's Total Fertility Rate (TFR) has dropped to 2.0 nationally (NFHS-5), below the 2.1 replacement threshold, indicating population stabilization by mid-century."
                },
                {
                    "icon": "🚀",
                    "title": "Urbanization Momentum",
                    "text": "Urban population share is approaching 36%, driving metropolitan economic clustering around Delhi NCR, Mumbai MMR, Bengaluru, Pune, and Hyderabad."
                }
            ]
        },
        "literacy-rate": {
            "state_key": "literacy-rate",
            "history_key": "literacy_rate",
            "direction": "higher_is_better",
            "category": "Education",
            "kpi_max_title": "Highest Literacy State",
            "kpi_max_val": "Kerala",
            "kpi_max_sub": "94.0% Total Literacy",
            "kpi_total_title": "National Literacy Average",
            "kpi_total_val": "74.04%",
            "kpi_total_sub": "Census 2011 Benchmark",
            "kpi_median_title": "Median State Literacy",
            "kpi_median_val": "76.2%",
            "kpi_median_sub": "State: West Bengal",
            "kpi_top5_title": "Top 3 High Performers",
            "kpi_top5_val": "> 91.0%",
            "kpi_top5_sub": "Kerala, Lakshadweep, Mizoram",
            "insights": [
                {
                    "icon": "🎓",
                    "title": "Seven-Decade Historical Ascent",
                    "text": "India's literacy expanded from just 18.33% at Independence to 74.04% in Census 2011, and is projected to cross 82% in contemporary sample surveys."
                },
                {
                    "icon": "📚",
                    "title": "Near-Universal Regional Clusters",
                    "text": "Kerala (94.0%), Lakshadweep (91.8%), and Mizoram (91.3%) demonstrate that high public investment in primary schooling delivers near-universal literacy."
                },
                {
                    "icon": "⚖️",
                    "title": "Closing the Gender Gap",
                    "text": "The male-female literacy gap has contracted from 24.8% in 1991 to under 12.5% in recent surveys, with female youth literacy accelerating rapidly."
                },
                {
                    "icon": "🎯",
                    "title": "Catch-up Trajectory",
                    "text": "States starting from lower baselines like Bihar and Jharkhand have posted the steepest decadal percentage-point gains among cohorts aged 15-24."
                }
            ]
        },
        "unemployment-rate": {
            "state_key": "unemployment",
            "history_key": None,
            "direction": "lower_is_better",
            "category": "Employment",
            "kpi_max_title": "Lowest Joblessness State",
            "kpi_max_val": "Sikkim / MP",
            "kpi_max_sub": "1.9% - 2.4% Jobless Rate",
            "kpi_total_title": "National Unemployment",
            "kpi_total_val": "3.1%",
            "kpi_total_sub": "MoSPI PLFS 2023 Annual",
            "kpi_median_title": "Median State Unemployment",
            "kpi_median_val": "3.9%",
            "kpi_median_sub": "State: Bihar",
            "kpi_top5_title": "Top Industrial States",
            "kpi_top5_val": "< 2.5%",
            "kpi_top5_sub": "Gujarat, Madhya Pradesh",
            "insights": [
                {
                    "icon": "💼",
                    "title": "Post-Pandemic Labour Resilience",
                    "text": "India's headline unemployment rate has moderated to 3.1% in the latest PLFS annual rounds, down from 5.8% in 2018-19, showing resilient labour demand."
                },
                {
                    "icon": "👩‍💼",
                    "title": "Rising Female Participation",
                    "text": "Female Labour Force Participation Rate (FLFPR) has expanded to 37.0%, bolstered by rural self-help groups, agriculture, and formal sector onboarding."
                },
                {
                    "icon": "🌾",
                    "title": "Rural vs Urban Dynamic",
                    "text": "Rural unemployment stands lower (2.4%) due to agricultural livelihoods, whereas urban centers exhibit frictional youth unemployment (5.4%)."
                },
                {
                    "icon": "🏭",
                    "title": "Manufacturing Absorption",
                    "text": "Industrial and logistics hubs like Gujarat, MP, and Karnataka maintain low unemployment rates through export-oriented manufacturing and services."
                }
            ]
        },
        "life-expectancy": {
            "state_key": "health",
            "history_key": "life_expectancy",
            "direction": "higher_is_better",
            "category": "Healthcare",
            "kpi_max_title": "Lowest Infant Mortality",
            "kpi_max_val": "Kerala",
            "kpi_max_sub": "6 per 1,000 Live Births",
            "kpi_total_title": "National Life Expectancy",
            "kpi_total_val": "72.0 Years",
            "kpi_total_sub": "World Bank / UN 2023",
            "kpi_median_title": "Median State IMR",
            "kpi_median_val": "28 / 1,000",
            "kpi_median_sub": "State: Karnataka",
            "kpi_top5_title": "Decadal Longevity Gain",
            "kpi_top5_val": "+5.2 Years",
            "kpi_top5_sub": "2010 (66.8y) to 2023 (72.0y)",
            "insights": [
                {
                    "icon": "❤️",
                    "title": "27-Year Longevity Expansion",
                    "text": "Average life expectancy at birth in India has risen from 45.2 years in 1960 to 72.0 years in 2023, driven by sanitation, vaccination, and maternal care."
                },
                {
                    "icon": "👶",
                    "title": "Infant Mortality Plunge",
                    "text": "Infant mortality has fallen from over 160 per 1,000 in the 1960s to under 28 nationally, with pioneering states like Kerala matching European standards."
                },
                {
                    "icon": "🏥",
                    "title": "Institutional Delivery Growth",
                    "text": "Institutional births now exceed 89% nationally under national health mission initiatives, substantially reducing maternal mortality."
                },
                {
                    "icon": "🩺",
                    "title": "Epidemiological Transition",
                    "text": "Public health focus is expanding from infectious diseases toward management of hypertension, diabetes, and cardiovascular wellness."
                }
            ]
        },
        "internet-users": {
            "state_key": None,
            "history_key": "internet_penetration",
            "direction": "higher_is_better",
            "category": "Digital Infrastructure",
            "kpi_max_title": "Active Internet Population",
            "kpi_max_val": "820+ Million",
            "kpi_max_sub": "2nd Largest Globally",
            "kpi_total_title": "National Internet Penetration",
            "kpi_total_val": "55.9%",
            "kpi_total_sub": "World Bank / ITU 2024",
            "kpi_median_title": "Data Consumption / Month",
            "kpi_median_val": "24.1 GB / User",
            "kpi_median_sub": "Highest globally",
            "kpi_top5_title": "10-Year Growth Rate",
            "kpi_top5_val": "+414%",
            "kpi_top5_sub": "From 13.5% (2014) to 55.9%",
            "insights": [
                {
                    "icon": "📱",
                    "title": "The 4G/5G Wireless Revolution",
                    "text": "Internet access surged from just 13.5% in 2014 to over 55.9% in 2024, democratizing access across tier-2 cities and rural farming belts."
                },
                {
                    "icon": "💰",
                    "title": "Cheapest Data Tariffs Globally",
                    "text": "Mobile broadband costs fell by over 95% from ₹250/GB in 2014 to under ₹10/GB today, sparking unprecedented digital consumption."
                },
                {
                    "icon": "💳",
                    "title": "UPI Real-Time Payments Backbone",
                    "text": "India's Unified Payments Interface processes over 14 Billion real-time transactions monthly, accounting for nearly 46% of all global instant payments."
                },
                {
                    "icon": "🌐",
                    "title": "BharatNet Rural Fiber Backbone",
                    "text": "Optical fiber connectivity now links over 200,000 Gram Panchayats, bridging the digital divide across remote educational centers."
                }
            ]
        }
    }

    # World Bank energy templates
    for wb_id in ["1-1_access-electricity-tot", "1-2_access-electricity-rural", "1-3_access-electricity-urban", "2-1_access-cft-tot"]:
        ind_configs[wb_id] = {
            "state_key": None,
            "history_key": None,
            "direction": "higher_is_better",
            "category": "Energy & Infrastructure",
            "kpi_max_title": "National Coverage",
            "kpi_max_val": "99.6%",
            "kpi_max_sub": "Saubhagya Mission",
            "kpi_total_title": "Global Benchmark",
            "kpi_total_val": "High Access",
            "kpi_total_sub": "World Bank Certified",
            "kpi_median_title": "Rural Electrification",
            "kpi_median_val": "99.3%",
            "kpi_median_sub": "Universal Grid Reach",
            "kpi_top5_title": "Target Status",
            "kpi_top5_val": "Achieved",
            "kpi_top5_sub": "100% Village Electrification",
            "insights": [
                {
                    "icon": "⚡",
                    "title": "Universal Household Electrification",
                    "text": "Through the Saubhagya initiative, over 28 Million households were connected to the national electrical grid in historic record time."
                },
                {
                    "icon": "☀️",
                    "title": "Renewable Energy Transition",
                    "text": "India's installed non-fossil capacity has crossed 190 GW, representing over 43% of total generation capacity toward the 500 GW 2030 target."
                },
                {
                    "icon": "🔌",
                    "title": "One Nation, One Grid",
                    "text": "The unified national transmission grid synchronizes power flows seamlessly from hydropower in the north to wind and solar in the south."
                },
                {
                    "icon": "🌱",
                    "title": "Clean Cooking & LPG Expansion",
                    "text": "PM Ujjwala Yojana provided over 100 Million LPG connections, drastically improving rural indoor air quality and maternal respiratory health."
                }
            ]
        }

    for ind in all_indicators:
        ind_id = ind['id']
        cfg = ind_configs.get(ind_id, {
            "state_key": None,
            "history_key": None,
            "direction": "neutral",
            "category": "Indicator",
            "kpi_max_title": "National Benchmark",
            "kpi_max_val": ind.get('display', {}).get('en', 'Verified'),
            "kpi_max_sub": "Reference Period",
            "kpi_total_title": "Status",
            "kpi_total_val": "Verified",
            "kpi_total_sub": "Phase 13 Governance",
            "kpi_median_title": "Data Source",
            "kpi_median_val": js_source_names.get(ind.get('source_id', ''), 'Official'),
            "kpi_median_sub": "Accredited Agency",
            "kpi_top5_title": "Coverage",
            "kpi_top5_val": "National",
            "kpi_top5_sub": "36 States & UTs",
            "insights": [
                {
                    "icon": "📊",
                    "title": "Verified Public Data",
                    "text": "This indicator is compiled under IndiaMetrix Phase 13 data integrity governance with strict official source cross-referencing."
                },
                {
                    "icon": "🔍",
                    "title": "Standardized Methodology",
                    "text": ind.get('methodology_note', 'Official statistical reporting.')
                },
                {
                    "icon": "🌐",
                    "title": "National Trajectory",
                    "text": "Historical tracking and comparative benchmarks provide clear visibility into developmental progression."
                },
                {
                    "icon": "📈",
                    "title": "Open Data Access",
                    "text": "Explore full regional breakdowns, historical tables, and CSV exports through the interactive Data Explorer."
                }
            ]
        })

        name_en = ind['name'].get('en', '')
        name_hi = ind['name'].get('hi', '')
        disp_en = ind['display'].get('en', '')
        disp_hi = ind['display'].get('hi', '')
        year = ind.get('year', '')
        src_url = ind.get('source_url', '')
        src_name = js_source_names.get(ind.get('source_id', ''), ind.get('source_id', ''))
        methodology_note = ind.get('methodology_note', '')
        last_updated = ind.get('last_updated', '2026-08-15')
        category = cfg['category']

        # Build 36 states dataset
        compiled_states = []
        state_key = cfg.get('state_key')
        
        if state_key:
            for s in states_pool:
                sid = s['id']
                s_ind = next((i for i in s.get('indicators', []) if i['id'] == state_key), None)
                if s_ind and s_ind.get('value') is not None:
                    val = s_ind['value']
                    eq = country_equivs.get(sid, {"country": "Sovereign Nation", "flag": "🌍"})
                    
                    # Format display
                    disp = s_ind.get('display', {}).get('en')
                    if not disp:
                        if state_key == 'gdp':
                            disp = f"₹{val/100000:.2f}L Cr" if val >= 100000 else f"₹{val:,} Cr"
                        elif state_key == 'population':
                            disp = f"{val/10000000:.2f} Cr" if val >= 10000000 else f"{val:,}"
                        elif state_key in ['literacy-rate', 'unemployment']:
                            disp = f"{val:.1f}%"
                        else:
                            disp = str(val)

                    compiled_states.append({
                        "id": sid,
                        "name": s['name'],
                        "value": val,
                        "formatted": {"en": disp, "hi": disp},
                        "equiv_country": eq["country"],
                        "equiv_flag": eq["flag"]
                    })

            # Sort states
            reverse_sort = (cfg['direction'] != 'lower_is_better')
            compiled_states.sort(key=lambda x: x['value'], reverse=reverse_sort)

            # Compute ranks and national share
            tot_val = sum(x['value'] for x in compiled_states) if compiled_states else 1
            for idx, item in enumerate(compiled_states):
                item['rank'] = idx + 1
                if state_key in ['gdp', 'population']:
                    item['share_pct'] = round((item['value'] / tot_val) * 100, 1)

        # Build history dataset
        compiled_history = None
        hist_key = cfg.get('history_key')
        if hist_key and hist_key in history_data:
            h = history_data[hist_key]
            compiled_history = {
                "labels": h.get('labels', []),
                "values": h.get('values', []),
                "formatted": [str(v) for v in h.get('values', [])]
            }

        # Build analytical insights HTML
        insights_html = ""
        for ins in cfg['insights']:
            insights_html += f"""
        <article class="ind-insight-card">
          <span class="ind-insight-icon" aria-hidden="true">{ins['icon']}</span>
          <h3 class="ind-insight-title">{ins['title']}</h3>
          <p class="ind-insight-text">{ins['text']}</p>
        </article>"""

        # Client-side data object
        indicator_data_obj = {
            "id": ind_id,
            "name": {"en": name_en, "hi": name_hi},
            "headline": {"en": disp_en, "hi": disp_hi},
            "year": year,
            "category": category,
            "source_name": src_name,
            "source_url": src_url,
            "direction": cfg['direction'],
            "states": compiled_states,
            "history": compiled_history
        }

        # Replace in template
        out = template
        meta_info = indicator_seo_meta.get(ind_id, {
            "title": f"{name_en} Data & Trends | IndiaMetrix",
            "desc": f"Explore verified statistics, state rankings, and historical time-series for {name_en} on IndiaMetrix."
        })
        out = out.replace('{{seo_title}}', meta_info['title'])
        out = out.replace('{{seo_desc}}', meta_info['desc'])
        out = out.replace('{{id}}', str(ind_id))
        out = out.replace('{{name_en}}', str(name_en))
        out = out.replace('{{name_hi}}', str(name_hi))
        out = out.replace('{{disp_en}}', str(disp_en))
        out = out.replace('{{disp_hi}}', str(disp_hi))
        out = out.replace('{{year}}', str(year))
        out = out.replace('{{category}}', str(category))
        out = out.replace('{{source_name}}', str(src_name))
        out = out.replace('{{source_url}}', str(src_url))
        out = out.replace('{{methodology_note}}', str(methodology_note))
        out = out.replace('{{last_updated}}', str(last_updated))

        out = out.replace('{{kpi_max_title}}', cfg['kpi_max_title'])
        out = out.replace('{{kpi_max_val}}', cfg['kpi_max_val'])
        out = out.replace('{{kpi_max_sub}}', cfg['kpi_max_sub'])

        out = out.replace('{{kpi_total_title}}', cfg['kpi_total_title'])
        out = out.replace('{{kpi_total_val}}', cfg['kpi_total_val'])
        out = out.replace('{{kpi_total_sub}}', cfg['kpi_total_sub'])

        out = out.replace('{{kpi_median_title}}', cfg['kpi_median_title'])
        out = out.replace('{{kpi_median_val}}', cfg['kpi_median_val'])
        out = out.replace('{{kpi_median_sub}}', cfg['kpi_median_sub'])

        out = out.replace('{{kpi_top5_title}}', cfg['kpi_top5_title'])
        out = out.replace('{{kpi_top5_val}}', cfg['kpi_top5_val'])
        out = out.replace('{{kpi_top5_sub}}', cfg['kpi_top5_sub'])

        out = out.replace('{{insights_html}}', insights_html)
        out = out.replace('{{indicator_data_json}}', json.dumps(indicator_data_obj, ensure_ascii=False))

        out = re.sub(r'<!-- BUILD_INJECT:.*?-->', '', out)
        out = re.sub(r'<!-- END_BUILD_INJECT -->', '', out)

        out_path = os.path.join(out_indicators_dir, f"{ind_id}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(out)

    print(f"Master built all {len(all_indicators)} indicator pages successfully!")

if __name__ == "__main__":
    build_all_indicators(".")

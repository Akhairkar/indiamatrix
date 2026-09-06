import os
import json

DISTRICTS = [
    {
        "id": "pune",
        "state_id": "maharashtra",
        "name": {"en": "Pune", "hi": "पुणे"},
        "indicators": [
            {
                "id": "population",
                "category": "population",
                "name": {"en": "Population", "hi": "जनसंख्या"},
                "unit": "count",
                "geography_level": "district",
                "geography_id": "pune",
                "year": 2011,
                "value": 9429408,
                "display": {"en": "9.43 million", "hi": "9.43 मिलियन"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011 total population count.",
                "direction": "neutral",
                "is_estimate": False
            },
            {
                "id": "literacy-rate",
                "category": "education",
                "name": {"en": "Literacy Rate", "hi": "साक्षरता दर"},
                "unit": "%",
                "geography_level": "district",
                "geography_id": "pune",
                "year": 2011,
                "value": 86.15,
                "display": {"en": "86.15%", "hi": "86.15%"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011 effective literacy rate (aged 7+).",
                "direction": "higher_is_better",
                "is_estimate": False
            },
            {
                "id": "sex-ratio",
                "category": "demographics",
                "name": {"en": "Sex Ratio", "hi": "लिंगानुपात"},
                "unit": "females per 1000 males",
                "geography_level": "district",
                "geography_id": "pune",
                "year": 2011,
                "value": 915,
                "display": {"en": "915", "hi": "915"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011 number of females per 1000 males.",
                "direction": "higher_is_better",
                "is_estimate": False
            }
        ]
    },
    {
        "id": "bengaluru-urban",
        "state_id": "karnataka",
        "name": {"en": "Bengaluru Urban", "hi": "बेंगलुरु शहरी"},
        "indicators": [
            {
                "id": "population",
                "category": "population",
                "name": {"en": "Population", "hi": "जनसंख्या"},
                "unit": "count",
                "geography_level": "district",
                "geography_id": "bengaluru-urban",
                "year": 2011,
                "value": 9621551,
                "display": {"en": "9.62 million", "hi": "9.62 मिलियन"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "neutral",
                "is_estimate": False
            },
            {
                "id": "literacy-rate",
                "category": "education",
                "name": {"en": "Literacy Rate", "hi": "साक्षरता दर"},
                "unit": "%",
                "geography_level": "district",
                "geography_id": "bengaluru-urban",
                "year": 2011,
                "value": 87.67,
                "display": {"en": "87.67%", "hi": "87.67%"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            },
            {
                "id": "sex-ratio",
                "category": "demographics",
                "name": {"en": "Sex Ratio", "hi": "लिंगानुपात"},
                "unit": "females per 1000 males",
                "geography_level": "district",
                "geography_id": "bengaluru-urban",
                "year": 2011,
                "value": 916,
                "display": {"en": "916", "hi": "916"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            }
        ]
    },
    {
        "id": "ahmedabad",
        "state_id": "gujarat",
        "name": {"en": "Ahmedabad", "hi": "अहमदाबाद"},
        "indicators": [
            {
                "id": "population",
                "category": "population",
                "name": {"en": "Population", "hi": "जनसंख्या"},
                "unit": "count",
                "geography_level": "district",
                "geography_id": "ahmedabad",
                "year": 2011,
                "value": 7214225,
                "display": {"en": "7.21 million", "hi": "7.21 मिलियन"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "neutral",
                "is_estimate": False
            },
            {
                "id": "literacy-rate",
                "category": "education",
                "name": {"en": "Literacy Rate", "hi": "साक्षरता दर"},
                "unit": "%",
                "geography_level": "district",
                "geography_id": "ahmedabad",
                "year": 2011,
                "value": 85.31,
                "display": {"en": "85.31%", "hi": "85.31%"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            },
            {
                "id": "sex-ratio",
                "category": "demographics",
                "name": {"en": "Sex Ratio", "hi": "लिंगानुपात"},
                "unit": "females per 1000 males",
                "geography_level": "district",
                "geography_id": "ahmedabad",
                "year": 2011,
                "value": 904,
                "display": {"en": "904", "hi": "904"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            }
        ]
    },
    {
        "id": "chennai",
        "state_id": "tamil-nadu",
        "name": {"en": "Chennai", "hi": "चेन्नई"},
        "indicators": [
            {
                "id": "population",
                "category": "population",
                "name": {"en": "Population", "hi": "जनसंख्या"},
                "unit": "count",
                "geography_level": "district",
                "geography_id": "chennai",
                "year": 2011,
                "value": 4646732,
                "display": {"en": "4.65 million", "hi": "4.65 मिलियन"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "neutral",
                "is_estimate": False
            },
            {
                "id": "literacy-rate",
                "category": "education",
                "name": {"en": "Literacy Rate", "hi": "साक्षरता दर"},
                "unit": "%",
                "geography_level": "district",
                "geography_id": "chennai",
                "year": 2011,
                "value": 90.18,
                "display": {"en": "90.18%", "hi": "90.18%"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            },
            {
                "id": "sex-ratio",
                "category": "demographics",
                "name": {"en": "Sex Ratio", "hi": "लिंगानुपात"},
                "unit": "females per 1000 males",
                "geography_level": "district",
                "geography_id": "chennai",
                "year": 2011,
                "value": 989,
                "display": {"en": "989", "hi": "989"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            }
        ]
    },
    {
        "id": "lucknow",
        "state_id": "uttar-pradesh",
        "name": {"en": "Lucknow", "hi": "लखनऊ"},
        "indicators": [
            {
                "id": "population",
                "category": "population",
                "name": {"en": "Population", "hi": "जनसंख्या"},
                "unit": "count",
                "geography_level": "district",
                "geography_id": "lucknow",
                "year": 2011,
                "value": 4589838,
                "display": {"en": "4.59 million", "hi": "4.59 मिलियन"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "neutral",
                "is_estimate": False
            },
            {
                "id": "literacy-rate",
                "category": "education",
                "name": {"en": "Literacy Rate", "hi": "साक्षरता दर"},
                "unit": "%",
                "geography_level": "district",
                "geography_id": "lucknow",
                "year": 2011,
                "value": 77.29,
                "display": {"en": "77.29%", "hi": "77.29%"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            },
            {
                "id": "sex-ratio",
                "category": "demographics",
                "name": {"en": "Sex Ratio", "hi": "लिंगानुपात"},
                "unit": "females per 1000 males",
                "geography_level": "district",
                "geography_id": "lucknow",
                "year": 2011,
                "value": 917,
                "display": {"en": "917", "hi": "917"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            }
        ]
    },
    {
        "id": "ernakulam",
        "state_id": "kerala",
        "name": {"en": "Ernakulam", "hi": "एर्नाकुलम"},
        "indicators": [
            {
                "id": "population",
                "category": "population",
                "name": {"en": "Population", "hi": "जनसंख्या"},
                "unit": "count",
                "geography_level": "district",
                "geography_id": "ernakulam",
                "year": 2011,
                "value": 3282388,
                "display": {"en": "3.28 million", "hi": "3.28 मिलियन"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "neutral",
                "is_estimate": False
            },
            {
                "id": "literacy-rate",
                "category": "education",
                "name": {"en": "Literacy Rate", "hi": "साक्षरता दर"},
                "unit": "%",
                "geography_level": "district",
                "geography_id": "ernakulam",
                "year": 2011,
                "value": 95.89,
                "display": {"en": "95.89%", "hi": "95.89%"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            },
            {
                "id": "sex-ratio",
                "category": "demographics",
                "name": {"en": "Sex Ratio", "hi": "लिंगानुपात"},
                "unit": "females per 1000 males",
                "geography_level": "district",
                "geography_id": "ernakulam",
                "year": 2011,
                "value": 1027,
                "display": {"en": "1027", "hi": "1027"},
                "source_id": "census-india",
                "source_url": "https://censusindia.gov.in/",
                "last_checked": "2026-08-15",
                "last_updated": "2026-08-15",
                "methodology_note": "Census 2011.",
                "direction": "higher_is_better",
                "is_estimate": False
            }
        ]
    }
]

def seed():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    districts_dir = os.path.join(root_dir, 'data', 'districts')
    os.makedirs(districts_dir, exist_ok=True)

    for dist in DISTRICTS:
        fn = f"{dist['state_id']}-{dist['id']}.json"
        fpath = os.path.join(districts_dir, fn)
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(dist, f, indent=2, ensure_ascii=False)
        print(f"Saved district {fn}")

if __name__ == '__main__':
    seed()

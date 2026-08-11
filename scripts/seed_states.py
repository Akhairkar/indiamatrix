import json
import os

states_data = [
    {"id": "andaman-nicobar", "en": "Andaman & Nicobar", "hi": "अंडमान और निकोबार", "pop": 380581, "pop_disp_en": "3.8 Lakh", "pop_disp_hi": "3.8 लाख", "lit": 86.63},
    {"id": "andhra-pradesh", "en": "Andhra Pradesh", "hi": "आंध्र प्रदेश", "pop": 49577103, "pop_disp_en": "4.95 Crore", "pop_disp_hi": "4.95 करोड़", "lit": 67.02},
    {"id": "arunachal-pradesh", "en": "Arunachal Pradesh", "hi": "अरुणाचल प्रदेश", "pop": 1383727, "pop_disp_en": "13.8 Lakh", "pop_disp_hi": "13.8 लाख", "lit": 65.38},
    {"id": "assam", "en": "Assam", "hi": "असम", "pop": 31205576, "pop_disp_en": "3.12 Crore", "pop_disp_hi": "3.12 करोड़", "lit": 72.19},
    {"id": "bihar", "en": "Bihar", "hi": "बिहार", "pop": 104099452, "pop_disp_en": "10.4 Crore", "pop_disp_hi": "10.4 करोड़", "lit": 61.80},
    {"id": "chandigarh", "en": "Chandigarh", "hi": "चंडीगढ़", "pop": 1055450, "pop_disp_en": "10.5 Lakh", "pop_disp_hi": "10.5 लाख", "lit": 86.05},
    {"id": "chhattisgarh", "en": "Chhattisgarh", "hi": "छत्तीसगढ़", "pop": 25545198, "pop_disp_en": "2.55 Crore", "pop_disp_hi": "2.55 करोड़", "lit": 70.28},
    {"id": "dadra-nagar-haveli-daman-diu", "en": "Dadra & Nagar Haveli and Daman & Diu", "hi": "दादरा और नगर हवेली तथा दमन और दीव", "pop": 585764, "pop_disp_en": "5.8 Lakh", "pop_disp_hi": "5.8 लाख", "lit": 76.24}, # combined approx
    {"id": "delhi", "en": "Delhi", "hi": "दिल्ली", "pop": 16787941, "pop_disp_en": "1.67 Crore", "pop_disp_hi": "1.67 करोड़", "lit": 86.21},
    {"id": "goa", "en": "Goa", "hi": "गोवा", "pop": 1458545, "pop_disp_en": "14.5 Lakh", "pop_disp_hi": "14.5 लाख", "lit": 88.70},
    {"id": "gujarat", "en": "Gujarat", "hi": "गुजरात", "pop": 60439692, "pop_disp_en": "6.04 Crore", "pop_disp_hi": "6.04 करोड़", "lit": 78.03},
    {"id": "haryana", "en": "Haryana", "hi": "हरियाणा", "pop": 25351462, "pop_disp_en": "2.53 Crore", "pop_disp_hi": "2.53 करोड़", "lit": 75.55},
    {"id": "himachal-pradesh", "en": "Himachal Pradesh", "hi": "हिमाचल प्रदेश", "pop": 6864602, "pop_disp_en": "68.6 Lakh", "pop_disp_hi": "68.6 लाख", "lit": 82.80},
    {"id": "jammu-kashmir", "en": "Jammu & Kashmir", "hi": "जम्मू और कश्मीर", "pop": 12267032, "pop_disp_en": "1.22 Crore", "pop_disp_hi": "1.22 करोड़", "lit": 67.16}, # Pre-bifurcation approx for JK UT
    {"id": "jharkhand", "en": "Jharkhand", "hi": "झारखंड", "pop": 32988134, "pop_disp_en": "3.29 Crore", "pop_disp_hi": "3.29 करोड़", "lit": 66.41},
    {"id": "karnataka", "en": "Karnataka", "hi": "कर्नाटक", "pop": 61095297, "pop_disp_en": "6.1 Crore", "pop_disp_hi": "6.1 करोड़", "lit": 75.36},
    {"id": "kerala", "en": "Kerala", "hi": "केरल", "pop": 33406061, "pop_disp_en": "3.34 Crore", "pop_disp_hi": "3.34 करोड़", "lit": 94.00},
    {"id": "ladakh", "en": "Ladakh", "hi": "लद्दाख", "pop": 274000, "pop_disp_en": "2.7 Lakh", "pop_disp_hi": "2.7 लाख", "lit": 74.27}, # Approx
    {"id": "lakshadweep", "en": "Lakshadweep", "hi": "लक्षद्वीप", "pop": 64473, "pop_disp_en": "64.4 Thousand", "pop_disp_hi": "64.4 हज़ार", "lit": 91.85},
    {"id": "madhya-pradesh", "en": "Madhya Pradesh", "hi": "मध्य प्रदेश", "pop": 72626809, "pop_disp_en": "7.26 Crore", "pop_disp_hi": "7.26 करोड़", "lit": 69.32},
    {"id": "maharashtra", "en": "Maharashtra", "hi": "महाराष्ट्र", "pop": 112374333, "pop_disp_en": "11.24 Crore", "pop_disp_hi": "11.24 करोड़", "lit": 82.34},
    {"id": "manipur", "en": "Manipur", "hi": "मणिपुर", "pop": 2855794, "pop_disp_en": "28.5 Lakh", "pop_disp_hi": "28.5 लाख", "lit": 76.94},
    {"id": "meghalaya", "en": "Meghalaya", "hi": "मेघालय", "pop": 2966889, "pop_disp_en": "29.6 Lakh", "pop_disp_hi": "29.6 लाख", "lit": 74.43},
    {"id": "mizoram", "en": "Mizoram", "hi": "मिज़ोरम", "pop": 1097206, "pop_disp_en": "10.9 Lakh", "pop_disp_hi": "10.9 लाख", "lit": 91.33},
    {"id": "nagaland", "en": "Nagaland", "hi": "नागालैंड", "pop": 1978502, "pop_disp_en": "19.7 Lakh", "pop_disp_hi": "19.7 लाख", "lit": 79.55},
    {"id": "odisha", "en": "Odisha", "hi": "ओडिशा", "pop": 41974218, "pop_disp_en": "4.19 Crore", "pop_disp_hi": "4.19 करोड़", "lit": 72.87},
    {"id": "puducherry", "en": "Puducherry", "hi": "पुडुचेरी", "pop": 1247953, "pop_disp_en": "12.4 Lakh", "pop_disp_hi": "12.4 लाख", "lit": 85.85},
    {"id": "punjab", "en": "Punjab", "hi": "पंजाब", "pop": 27743338, "pop_disp_en": "2.77 Crore", "pop_disp_hi": "2.77 करोड़", "lit": 75.84},
    {"id": "rajasthan", "en": "Rajasthan", "hi": "राजस्थान", "pop": 68548437, "pop_disp_en": "6.85 Crore", "pop_disp_hi": "6.85 करोड़", "lit": 66.11},
    {"id": "sikkim", "en": "Sikkim", "hi": "सिक्किम", "pop": 610577, "pop_disp_en": "6.1 Lakh", "pop_disp_hi": "6.1 लाख", "lit": 81.42},
    {"id": "tamil-nadu", "en": "Tamil Nadu", "hi": "तमिलनाडु", "pop": 72147030, "pop_disp_en": "7.21 Crore", "pop_disp_hi": "7.21 करोड़", "lit": 80.09},
    {"id": "telangana", "en": "Telangana", "hi": "तेलंगाना", "pop": 35003674, "pop_disp_en": "3.5 Crore", "pop_disp_hi": "3.5 करोड़", "lit": 66.54},
    {"id": "tripura", "en": "Tripura", "hi": "त्रिपुरा", "pop": 3673917, "pop_disp_en": "36.7 Lakh", "pop_disp_hi": "36.7 लाख", "lit": 87.22},
    {"id": "uttar-pradesh", "en": "Uttar Pradesh", "hi": "उत्तर प्रदेश", "pop": 199812341, "pop_disp_en": "19.98 Crore", "pop_disp_hi": "19.98 करोड़", "lit": 67.68},
    {"id": "uttarakhand", "en": "Uttarakhand", "hi": "उत्तराखंड", "pop": 10086292, "pop_disp_en": "1.0 Crore", "pop_disp_hi": "1.0 करोड़", "lit": 78.82},
    {"id": "west-bengal", "en": "West Bengal", "hi": "पश्चिम बंगाल", "pop": 91276115, "pop_disp_en": "9.12 Crore", "pop_disp_hi": "9.12 करोड़", "lit": 76.26}
]

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(root_dir, 'data', 'indicators', 'states')
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for state in states_data:
        data = {
            "_readme": f"Headline indicators for {state['en']} State Profile.",
            "id": state['id'],
            "name": { "en": state['en'], "hi": state['hi'] },
            "indicators": [
                {
                    "id": "population",
                    "category": "population",
                    "name": { "en": "Population", "hi": "जनसंख्या" },
                    "unit": "count",
                    "geography_level": "state",
                    "geography_id": state['id'],
                    "year": 2011,
                    "value": state['pop'],
                    "display": { "en": state['pop_disp_en'], "hi": state['pop_disp_hi'] },
                    "source_id": "census-india",
                    "source_url": "https://censusindia.gov.in/",
                    "last_checked": "2026-08-12",
                    "last_updated": "2026-08-12",
                    "methodology_note": "Census 2011.",
                    "is_estimate": False
                },
                {
                    "id": "literacy-rate",
                    "category": "education",
                    "name": { "en": "Literacy Rate", "hi": "साक्षरता दर" },
                    "unit": "%",
                    "geography_level": "state",
                    "geography_id": state['id'],
                    "year": 2011,
                    "value": state['lit'],
                    "display": { "en": f"{state['lit']}%", "hi": f"{state['lit']}%" },
                    "source_id": "census-india",
                    "source_url": "https://censusindia.gov.in/",
                    "last_checked": "2026-08-12",
                    "last_updated": "2026-08-12",
                    "methodology_note": "Census 2011.",
                    "is_estimate": False
                }
            ]
        }
        
        file_path = os.path.join(out_dir, f"{state['id']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    print(f"Generated {len(states_data)} state JSON files.")

if __name__ == "__main__":
    main()

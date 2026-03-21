DISTRICTS = [
    "bagalkot", "ballari", "belagavi", "bengaluru urban",
    "bengaluru rural", "bidar", "chamarajanagar",
    "chikkaballapura", "chikkamagaluru", "chitradurga",
    "dakshina kannada", "davanagere", "dharwad", "gadag",
    "hassan", "haveri", "kalaburagi", "kodagu", "kolar",
    "koppal", "mandya", "mysuru", "raichur", "ramanagara",
    "shivamogga", "tumakuru", "udupi", "uttara kannada",
    "vijayapura", "yadgir"
]

SPECIALIZATIONS = [
    "general medicine", "general surgery", "orthopaedics",
    "ophthalmology", "ent", "dental",
    "obstetrics and gynaecology", "paediatrics",
    "cardiology", "neuro surgery",
    "medical oncology", "radiation oncology",
    "emergency medicine", "mental disorder"
]
keyword_mapping = {
        # eye
        "eye": "ophthalmology",
        "eyes": "ophthalmology",
        "vision": "ophthalmology",

        # heart
        "heart": "cardiology",

        # bone
        "bone": "orthopaedics",
        "fracture": "orthopaedics",
        "injury": "orthopaedics",
        "knee pain":"prthopaedics",

        # ent
        "ear": "ent",
        "nose": "ent",
        "throat": "ent",

        # dental
        "teeth": "dental",
        "tooth": "dental",

        # child
        "child": "paediatrics",
        "kid": "paediatrics",
        "baby":"paediatrics",
        #Burns.
        "burn":"burns",
        #cancer..
        "cancer": "medical oncology",
        "tumor": "surgical oncology",
        "chemo": "medical oncology",
        "radiation": "radiation oncology",
        
        #gastro..
        "stomach": "surgical gastroenterology",
        "digestive": "surgical gastroenterology",

        #brain..
        "brain": "neuro surgery",
        "head": "neuro surgery",
        "headache": "general medicine",
        "migraine": "general medicine",
        "seizure": "neuro surgery",
        "stroke": "neuro surgery",
        "nerve": "neuro surgery",
        "neuro": "neuro surgery",
        # General fallback..
        "fever": "general medicine",
        "infection": "general medicine",
        "pain": "general medicine",
    }

district_alias = {
        "bangalore": "bengaluru urban",
        "bengaluru": "bengaluru urban",
        "mysore": "mysuru",
        "mangalore": "dakshina kannada",
        "shimoga": "shivamogga",
        "gulbarga": "kalaburagi",
        "bellary": "ballari"
    }

MEDICAL_KEYWORDS = [
    "hospital", "doctor", "clinic", "specialist", "specialist",
    "treatment", "surgery", "medicine", "pmjay", "pm-jay",
    "health", "healthcare", "patient", "ward", "emergency",
    "ayushman", "scheme", "insurance", "karnataka"
]
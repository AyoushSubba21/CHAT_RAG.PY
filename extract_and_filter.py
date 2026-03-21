from rapidfuzz import process, fuzz
from CONSTANT import keyword_mapping,DISTRICTS,SPECIALIZATIONS,district_alias
import json
import re

#extracting the specialization and district with llm...
def extract_entities(query,llm):

    prompt = f"""
Extract the following from the user query:

1. District in Karnataka (ONLY if explicitly mentioned, do NOT infer nearby districts)
2. Medical specialization (if any)
    Return ONLY valid JSON. No explanation.

If user says "near X", return X (not nearby districts)
Format:
{{
  "district": "...",
  "specialization": "..."
}}


If not found, return null.

Query: {query}
"""

    response = llm.invoke(prompt)
    text = response.content.strip()

    try:
        json_text = re.search(r"\{.*\}", text, re.DOTALL).group()
        data = json.loads(json_text)
    except:
        data = {"district": None, "specialization": None}

    district = data.get("district")
    specialization = data.get("specialization")

    if district:
        district = district.lower().strip()

    if specialization:
        specialization = specialization.lower().strip()

    return {
        "district": district,
        "specialization": specialization
    }

import re



def extract_entities_no_llm(query):
    if not query:
        return {"district": None, "specialization": None}
    query_lower = query.lower().strip()
    words=query_lower.split()

    # STEP 1: Normalize common user words ,medical terms
    
    

    # Inject mapped terms into query
    for key, value in keyword_mapping.items():
        if key in words:
            query_lower += " " + value

    extracted_district = None
    extracted_spec = None

    #STEP 2: District aliases
    

    #Fuzzy match district
    all_districts = DISTRICTS + list(district_alias.keys())

    district_match, district_score, _ = process.extractOne(
        query_lower, all_districts, scorer=fuzz.partial_ratio
    )
    
    extracted_district = None
    if district_score >= 75:
        if district_match in district_alias:
            extracted_district = district_alias[district_match]
        else:
            extracted_district = district_match
    
    spec_match, spec_score, _ = process.extractOne(
        query_lower, SPECIALIZATIONS, scorer=fuzz.partial_ratio
    )
    
    extracted_spec = None
    if spec_score >= 70:
        extracted_spec = spec_match

    return {
        "district": extracted_district,
        "specialization": extracted_spec
    }

# --- Examples ---
print(extract_entities_no_llm("I need a cardiologist near mysuru"))
# Output: {'district': 'mysuru', 'specialization': 'cardiologist'}

print(extract_entities_no_llm("orthopedic doctor in Bangalore"))
# Output: {'district': 'bangalore', 'specialization': 'orthopedic'}

print(extract_entities_no_llm("Pediatrician in Hassan"))
# Output: {'district': 'hassan', 'specialization': 'pediatrician'}

print(extract_entities_no_llm("Any hospital nearby?"))
# Output: {'district': None, 'specialization': None}

def correct_with_fuzzy(value, choices):
    if not value:
        return None

    match, score, _ = process.extractOne(value, choices)

    if score > 90:
        return match
    return value


def post_filter(docs, district, specialization):

    filtered = []

    for doc in docs:
        meta = doc.metadata

        # District check
        if district:
            stored_district = meta.get("district", "")
            dist_ok = fuzz.partial_ratio(district, stored_district) >= 70
        else:
            dist_ok = True

        #Specialization check
        if specialization:
            stored_spec = meta.get("specialization", "")
            spec_ok = (
                specialization in stored_spec
                or fuzz.partial_ratio(specialization, stored_spec) >= 75
            )
        else:
            spec_ok = True

        if dist_ok and spec_ok:
            filtered.append(doc)
        #print("----")
        #print("User district:", district)
       # print("Stored district:", stored_district)
        #print("District score:", fuzz.partial_ratio(district, stored_district))

        #print("User spec:", specialization)
        #print("Stored spec:", stored_spec)
        #print("Spec score:", fuzz.partial_ratio(specialization, stored_spec))

    return filtered



def normalize_specialization(user_spec):
    if not user_spec:
        return None

    user_spec = user_spec.lower()

    for key, value in keyword_mapping.items():
        if key in user_spec:
            return value

    return user_spec
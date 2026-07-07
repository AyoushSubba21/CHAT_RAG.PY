from CONSTANT import MEDICAL_KEYWORDS,DISTRICTS,SPECIALIZATIONS,keyword_mapping
from rapidfuzz import process, fuzz
#handles greetings...
def greeting_response():
    return """
<h3>Hello!</h3>

<p><b>I am your PM-JAY hospital assistant.</b><p>
I can help you find hospitals based on:
<ul>
    
    <li>Distric</li>
    <li>Specialization (eye, heart, dental, etc.)</li>
</ul>
Try asking:
<ul>

    <li>Eye hospital in Chikkaballapura</li>
    <li>Heart hospital near Mysuru </li>
</ul>

<b>How can I assist you today?</b>

"""
def is_greeting(query):
    greetings = [
        "hi", "hello", "hey",
        "good morning", "good afternoon", "good evening",
        "how are you", "what's up", "whats up"
    ]

    query = query.lower().strip()

    # exact match
    if query in greetings:
        return True

    # word-level match
    words = query.split()
    for g in greetings:
        if g in words:
            return True

    return False

def is_relevant_query(query: str) -> bool:
    query_lower = query.lower().strip()
    words = query_lower.split()

    # 1. Reject very short or meaningless input
    if len(query_lower) < 4 or len(words) == 0:
        return False
    
    
    # 2. Single short word — only allow exact keyword matches, NO fuzzy
    if len(words) == 1 and len(query_lower) < 6:
        if query_lower in MEDICAL_KEYWORDS:
            return True
        if query_lower in keyword_mapping:
            return True
        return False  # blocks "lata", "lati", "ajd", "aaa" etc.
    # 3. Check direct medical keyword match
    for keyword in MEDICAL_KEYWORDS:
        if keyword in query_lower:
            return True

    # 4. Check keyword_mapping keys (e.g. "eye", "heart", "bone")
    for key in keyword_mapping:
        if key in words:
            return True

    # 5. Fuzzy match against districts
    if DISTRICTS:
        _, district_score, _ = process.extractOne(
            query_lower, DISTRICTS, scorer=fuzz.partial_ratio
        )
        if district_score >= 75:
            return True

    # 6. Fuzzy match against specializations
    if SPECIALIZATIONS:
        _, spec_score, _ = process.extractOne(
            query_lower, SPECIALIZATIONS, scorer=fuzz.partial_ratio
        )
        if spec_score >= 70:
            return True

    return False

##is the user asking to compare the hospitals...
def is_compare_query(query: str) -> bool:
    compare_keywords = [
        "compare", "comparison", "vs", "versus",
        "difference between", "better", "which is best",
        "best hospital", "recommend", "suggest",
        "top hospital", "which hospital", "good hospital"
    ]
    query_lower = query.lower()
    return any(kw in query_lower for kw in compare_keywords)


##handles offlinee messsage...
def offline_message() -> str:
    return """
<p>📡 <b>You are currently in Offline Mode.</b></p>

<p>You can still:</p>
<ul>
    <li>🏥 Search hospitals by district</li>
    <li>🩺 Find hospitals by specialization</li>
    <li>📍 Get contact details and addresses</li>
</ul>

<p>For complex queries like:</p>
<ul>
    <li>🔍 Comparing hospitals</li>
    <li>⭐ Getting recommendations</li>
    <li>💡 Personalized suggestions</li>
</ul>

<p>👉 <b>Please go online and try again!</b></p>
"""
def out_of_scope_response() -> str:
    return """I'm sorry, I can only assist with PM-JAY hospital-related queries.<br>

You can ask me things like:
<ul>
    <li>Eye hospital in Mysuru</li>
    <li>Heart specialist near Bangalore</li>
    <li>Dental clinic in Hassan</li>
</ul>

<p>Please try a <b>hospital</b> or <b>medical-related</b> question!<p>"""





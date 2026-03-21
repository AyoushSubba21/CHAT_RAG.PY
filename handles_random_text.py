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
    
    
    # 1. Check direct medical keyword match
    for keyword in MEDICAL_KEYWORDS:
        if keyword in query_lower:
            return True

    # 2. Check keyword_mapping keys (e.g. "eye", "heart", "bone")
    for key in keyword_mapping:
        if key in words:
            return True

    # 3. Fuzzy match against districts
    if DISTRICTS:
        _, district_score, _ = process.extractOne(
            query_lower, DISTRICTS, scorer=fuzz.partial_ratio
        )
        if district_score >= 75:
            return True

    # 4. Fuzzy match against specializations
    if SPECIALIZATIONS:
        _, spec_score, _ = process.extractOne(
            query_lower, SPECIALIZATIONS, scorer=fuzz.partial_ratio
        )
        if spec_score >= 70:
            return True

    return False

def out_of_scope_response() -> str:
    return """I'm sorry, I can only assist with PM-JAY hospital-related queries.<br>

You can ask me things like:
<ul>
    <li>Eye hospital in Mysuru</li>
    <li>Heart specialist near Bangalore</li>
    <li>Dental clinic in Hassan</li>
</ul>

<p>Please try a <b>hospital</b> or <b>medical-related</b> question!<p>"""
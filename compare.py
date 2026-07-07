from rapidfuzz import fuzz

def build_hospital_context(docs):
    """Convert docs into a clean text context for the LLM."""
    context_parts = []
    for doc in docs[:8]:  # limit to 8 hospitals to stay within token limit
        meta = doc.metadata
        content = doc.page_content

        name = meta.get("hospital", "N/A").title()
        district = meta.get("district", "N/A").title()
        contact, email, address, specialization = "N/A", "N/A", "N/A", "N/A"

        for line in content.split("\n"):
            if "Specialization:" in line:
                specialization = line.split("Specialization:")[-1].strip()
            elif "Contact Number:" in line:
                contact = line.split("Contact Number:")[-1].strip()
            elif "Email Id:" in line:
                email = line.split("Email Id:")[-1].strip()
            elif "Address:" in line:
                address = line.split("Address:")[-1].strip()

        context_parts.append(
            f"Hospital: {name}\n"
            f"District: {district}\n"
            f"Specialization: {specialization}\n"
            f"Contact: {contact}\n"
            f"Email: {email}\n"
            f"Address: {address}"
        )

    return "\n\n---\n\n".join(context_parts)


def compare_with_llm(docs, user_query, llm):
    """Use Groq LLM to generate a rich compare/recommend response."""

    if not docs:
        return "<p>Sorry, no hospitals found for your query.</p>"

    context = build_hospital_context(docs)

    prompt = f"""
You are a friendly and helpful PM-JAY hospital assistant for Karnataka.

A user has asked: "{user_query}"

Below are the relevant PM-JAY hospitals from the PM-JAY database:

{context}

STRICT RULES:
- Use ONLY the hospitals provided above. Do NOT invent any hospital.
- Do NOT show any comparison table.
- Do NOT use technical jargon.
- Keep language simple, warm and easy to understand for a common person.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

<p>🏥 <b>Top Hospitals for [condition] under PM-JAY</b></p>

<ol>
  <li>
    <b>🏥 [Hospital Name]</b><br>
    [One simple sentence about what makes this hospital good for this condition]<br>
    <b>Good for:</b> [mention 2-3 relevant specializations in plain words]<br>
    📞 <b>Contact:</b> [contact number]<br>
    📍 <b>Address:</b> [address]
  </li>
</ol>

<p>🧠 <b>Which one should YOU choose?</b></p>
<ul>
  <li>If [specific situation] → 👉 <b>[Hospital Name]</b></li>
  <li>If [specific situation] → 👉 <b>[Hospital Name]</b></li>
</ul>

<p>💡 <b>Quick Tip:</b> [One helpful advice line for the user about this condition or what to look for]</p>

IMPORTANT:
- Explain WHY each hospital is good in simple, human words. 
- The final "Which one should YOU choose?" section must give clear, situation-based guidance.
- Use emojis to make it friendly and readable.
- Write as if you are personally helping a friend find a hospital.
"""

    response = llm.invoke(prompt)
    return response.content
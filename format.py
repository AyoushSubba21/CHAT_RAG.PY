from extract_and_filter import normalize_specialization
from CONSTANT import DISTRICTS,SPECIALIZATIONS
from rapidfuzz import process, fuzz
def response_format(docs,user_spec=None):
    response = "<p>Here are the hospitals available under PM-JAY for your query:</p>"
    response += "<ol>"
    
    user_spec=normalize_specialization(user_spec)

    for doc in docs:
        meta = doc.metadata

        name = meta.get("hospital", "N/A").title()
        district = meta.get("district", "N/A").title()

        # Extract remaining fields from page_content
        content = doc.page_content

        contact = "N/A"
        email = "N/A"
        address = "N/A"
        specialization=""

        for line in content.split("\n"):
            if "Specialization: " in line:
                full_spec=line.split("Specialization: ")[-1].strip().lower()
                # Smart split (handles multi-word properly)
                #specs = re.split(r',|\n{2,}', full_spec)
                #specs = [s.strip() for s in specs if s.strip()]
                
                matched_spec = ""
                #keep only the asked one..
                if user_spec:
                    for spec in SPECIALIZATIONS:
                        if spec in full_spec and fuzz.partial_ratio(user_spec,spec)>=70:
                            matched_spec=spec.title()
                            break
                else:#if there is no specialization mentioned by a user keep the entire spec provided by a hospital..
                    matched_spec=" ".join(full_spec.split()).title()
                    
                specialization=matched_spec
                    
            elif "Contact Number:" in line:
                contact = line.split("Contact Number:")[-1].strip()
            elif "Email Id:" in line:
                email = line.split("Email Id:")[-1].strip()
            elif "Address:" in line:
                address = line.split("Address:")[-1].strip()

        if user_spec and specialization=="":
            continue
        response += f"""
        <li>
        <b>{name}</b>
        <ul>
        <li>Specialization: {specialization}</li>
        <li>District: {district}</li>
        <li>Contact Number: {contact}</li>
        <li>Email Id: {email}</li>
        <li>Address: {address}</li>
        </ul>
        </li>
        """

    response += "</ol>"
    return response
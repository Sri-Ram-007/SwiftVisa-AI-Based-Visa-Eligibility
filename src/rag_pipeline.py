# ---------------------------
# HELPER: VISA TYPE MAPPING
# ---------------------------

def get_visa_type(country, purpose):

    visa_map = {
        "USA": {
            "study": "F-1 Student Visa",
            "work": "H-1B Work Visa",
            "tourism": "B-2 Tourist Visa"
        },
        "Canada": {
            "study": "Study Permit",
            "work": "Work Permit",
            "tourism": "Visitor Visa"
        },
        "UK": {
            "study": "Student Visa",
            "work": "Skilled Worker Visa",
            "tourism": "Standard Visitor Visa"
        },
        "Australia": {
            "study": "Student Visa (Subclass 500)",
            "work": "Temporary Skill Shortage Visa",
            "tourism": "Visitor Visa"
        },
        "Germany": {
            "study": "Student Visa",
            "work": "EU Blue Card",
            "tourism": "Schengen Visa"
        }
    }

    return visa_map.get(country, {}).get(purpose, "General Visa")


# ---------------------------
# HELPER: MOCK RAG RETRIEVAL
# ---------------------------

def retrieve_visa_info(country, purpose):
    return f"{purpose.capitalize()} visa rules for {country} require proper documentation, financial proof, and eligibility verification."


# ---------------------------
# MAIN FUNCTION
# ---------------------------

def check_visa(
    country,
    age,
    education,
    employment,
    income,
    purpose,
    admission_letter,
    english_score,
    financial_support,
    job_offer,
    travel_history
):

    probability = 50
    positive = []
    risks = []

    purpose = purpose.lower()

    # Get visa type
    visa_type = get_visa_type(country, purpose)
    eligible = "Not Eligible"

    # ---------------------------
    # STUDY VISA LOGIC
    # ---------------------------

    if purpose == "study":

        if admission_letter == "Yes":
            probability += 25
            positive.append("Confirmed admission to institution")
        else:
            probability -= 25
            risks.append("No confirmed university admission")

        if english_score >= 6.5:
            probability += 15
            positive.append("English proficiency meets requirement")
        else:
            probability -= 10
            risks.append("English proficiency score is below requirement")

        if financial_support == "Yes":
            probability += 15
            positive.append("Sufficient financial support for studies")
        else:
            probability -= 15
            risks.append("Lack of clear financial support")

        if travel_history == "Yes":
            probability += 5
            positive.append("Positive international travel history")

        if education in ["High School", "Diploma", "Bachelors Degree", "Masters Degree"]:
            probability += 10
            positive.append("Appropriate academic background")

        if country == "USA" and english_score < 6:
            probability -= 10
            risks.append("English score below typical USA visa expectations")

    # ---------------------------
    # WORK VISA LOGIC
    # ---------------------------

    elif purpose == "work":

        if job_offer == "Yes":
            probability += 25
            positive.append("Valid job offer from employer")
        else:
            probability -= 25
            risks.append("No confirmed job offer")

        if employment == "Employed":
            probability += 10
            positive.append("Currently employed")

        if income > 30000:
            probability += 10
            positive.append("Income level supports work visa eligibility")

        if travel_history == "Yes":
            probability += 5
            positive.append("Relevant international travel history")

    # ---------------------------
    # TOURIST VISA LOGIC
    # ---------------------------

    elif purpose == "tourism":

        probability += 10
        positive.append("Valid tourism purpose")

        if income > 20000:
            probability += 10
            positive.append("Financial capability for travel")
        else:
            probability -= 10
            risks.append("Insufficient financial stability")

        if travel_history == "Yes":
            probability += 10
            positive.append("Previous travel history supports application")

    # ---------------------------
    # FINAL DECISION
    # ---------------------------

    probability = max(0, min(probability, 100))

    if probability >= 60:
        eligible = "Eligible"
    else:
        eligible = "Not Eligible"

    # ---------------------------
    # RAG CONTEXT (SIMULATED)
    # ---------------------------

    retrieved_info = retrieve_visa_info(country, purpose)

    # ---------------------------
    # PROFESSIONAL EXPLANATION
    # ---------------------------

    if eligible == "Eligible":

        explanation = f"""
The applicant demonstrates strong eligibility for the {visa_type} under {country} immigration criteria.

Based on the evaluation, the profile satisfies the majority of key requirements expected for this visa category.

Key strengths identified in the application include:
• {', '.join(positive) if positive else 'Relevant supporting factors present'}
"""

        if risks:
            explanation += f"""
While the overall profile is strong, a few areas may require attention:
• {', '.join(risks)}
"""

        explanation += f"""
From an assessment perspective, the applicant meets the core academic, financial, and compliance requirements expected by immigration authorities.

With an estimated approval probability of {probability}%, the application is considered highly favorable and likely to succeed.
"""

    else:

        explanation = f"""
The applicant currently does not meet the required eligibility criteria for the {visa_type} under {country} immigration guidelines.

The evaluation indicates several gaps that may impact the approval outcome.

Key concerns identified include:
• {', '.join(risks) if risks else 'Insufficient supporting criteria'}
"""

        if positive:
            explanation += f"""
However, the profile does contain some positive elements:
• {', '.join(positive)}
"""

        explanation += f"""
To improve approval chances, the applicant should focus on strengthening the highlighted risk areas, particularly documentation, financial capability, or qualification alignment.

At present, with an estimated probability of {probability}%, the application outcome is uncertain and requires improvement before submission.
"""

    # ---------------------------
    # RETURN RESULT
    # ---------------------------

    return {
        "visa_type": visa_type,
        "eligibility": eligible,
        "probability": probability,
        "positive": positive,
        "risks": risks,
        "explanation": explanation,
        "sources": [retrieved_info]
    }
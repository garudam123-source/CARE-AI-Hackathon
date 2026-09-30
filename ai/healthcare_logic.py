import random
def generate_demo_readings(priority):
    """
    Generate simulated device readings for hackathon demonstration.
    These are NOT real patient measurements.
    """

    if priority == "High Priority":
        temperature = round(random.uniform(38.0, 39.2), 1)
        heart_rate = random.randint(100, 120)
        systolic = random.randint(135, 155)
        diastolic = random.randint(85, 100)
        spo2 = random.randint(90, 94)

    elif priority == "Needs Attention":
        temperature = round(random.uniform(37.3, 38.0), 1)
        heart_rate = random.randint(85, 105)
        systolic = random.randint(120, 140)
        diastolic = random.randint(75, 90)
        spo2 = random.randint(94, 97)

    else:
        temperature = round(random.uniform(36.5, 37.3), 1)
        heart_rate = random.randint(65, 85)
        systolic = random.randint(110, 125)
        diastolic = random.randint(70, 82)
        spo2 = random.randint(97, 100)

    return {
        "temperature": temperature,
        "heart_rate": heart_rate,
        "blood_pressure": f"{systolic}/{diastolic}",
        "spo2": spo2
    }
def analyze_health_input(
    symptoms,
    concern,
    severity,
    duration,
    worsening,
    activity_impact,
    new_symptoms,
    temperature=None,
    heart_rate=None,
    spo2=None
):

    # --------------------------------------------------
    # 1. Prepare user input
    # --------------------------------------------------

    symptoms = symptoms or ""
    concern = concern or ""

    text = (symptoms + " " + concern).lower()

    detected = []

    # --------------------------------------------------
    # 2. Automatic Health Indicator Detection
    # --------------------------------------------------

    keywords = {
        "Pain": ["pain", "ache", "hurt", "വേദന"],
        "Fever": ["fever", "temperature", "hot", "പനി", "ചൂട്"],
        "Cough": ["cough", "coughing", "ചുമ"],
        "Breathing Difficulty": [
            "breathing",
            "breath",
            "shortness",
            "breathless",
            "ശ്വാസം",
            "ശ്വാസതടസ്സം"
        ],
        "Dizziness": [
            "dizzy",
            "dizziness",
            "തലകറക്കം"
        ],
        "Vomiting": [
            "vomit",
            "vomiting",
            "ഛർദ്ദി",
            "ഛർദ്ദിക്കുന്നു"
        ],
        "Headache": [
            "headache",
            "head pain",
            "തലവേദന"
        ],
        "Weakness": [
            "weak",
            "weakness",
            "tired",
            "ക്ഷീണം",
            "ബലഹീനത"
        ],
        "Skin": [
            "rash",
            "itching",
            "skin",
            "ചൊറിച്ചിൽ",
            "ത്വക്ക്"
        ],
        "Eye": [
            "eye",
            "vision",
            "blurred",
            "കണ്ണ്",
            "കാഴ്ച"
        ],
        "Ear": [
            "ear",
            "hearing",
            "ചെവി",
            "കേൾവി"
        ],
        "Dental": [
            "tooth",
            "teeth",
            "gum",
            "പല്ല്",
            "മോണ"
        ]
    }

    for category, words in keywords.items():

        for word in words:

            if word in text:

                if category not in detected:
                    detected.append(category)

                break

    # --------------------------------------------------
    # 3. Health Reading Interpretation
    # --------------------------------------------------

    reading_flags = []

    try:
        temp = float(temperature) if temperature else None
    except ValueError:
        temp = None

    try:
        hr = int(heart_rate) if heart_rate else None
    except ValueError:
        hr = None

    try:
        oxygen = int(spo2) if spo2 else None
    except ValueError:
        oxygen = None

    # These are screening flags, NOT medical diagnosis.

    if temp is not None and temp >= 38:
        reading_flags.append("elevated temperature")

    if hr is not None and (hr < 50 or hr > 120):
        reading_flags.append("heart rate outside the demo reference range")

    if oxygen is not None and oxygen < 94:
        reading_flags.append("lower SpO₂ reading")

    # --------------------------------------------------
    # 4. Priority Analysis
    # --------------------------------------------------

    high_priority_reasons = []
    attention_reasons = []

    if severity == "Severe":
        high_priority_reasons.append(
            "the reported symptom severity is high"
        )

    if worsening == "Yes":
        high_priority_reasons.append(
            "the symptoms are getting worse"
        )

    if "Breathing Difficulty" in detected:
        high_priority_reasons.append(
            "breathing difficulty was reported"
        )

    if oxygen is not None and oxygen < 94:
        high_priority_reasons.append(
            "the entered SpO₂ reading is below the prototype reference threshold"
        )

    if duration == "More than 1 week":
        attention_reasons.append(
            "the symptoms have continued for more than one week"
        )

    if severity == "Moderate":
        attention_reasons.append(
            "moderate symptom severity was reported"
        )

    if activity_impact == "Yes":
        attention_reasons.append(
            "the symptoms are affecting normal activities"
        )

    if new_symptoms == "Yes":
        attention_reasons.append(
            "new or unusual symptoms were reported"
        )

    if reading_flags:
        attention_reasons.append(
            "some entered health readings need attention"
        )

    # --------------------------------------------------
    # 5. Final Priority
    # --------------------------------------------------

    if high_priority_reasons:

        level = "High Priority"

        pathway = (
            "Prompt professional medical assessment is recommended. "
            "If symptoms become severe or rapidly worsen, seek immediate medical help."
        )

    elif attention_reasons:

        level = "Needs Attention"

        pathway = (
            "Consider appropriate healthcare guidance, especially "
            "if symptoms continue, affect daily activities, or worsen."
        )

    else:

        level = "Low Priority"

        pathway = (
            "No immediate concerning information was reported. "
            "Continue monitoring the reported information and seek "
            "professional advice if symptoms persist or worsen."
        )

    # --------------------------------------------------
    # 6. Healthcare Professional Suggestion
    # --------------------------------------------------

    if "Skin" in detected:

        doctor = "Dermatology"

    elif "Eye" in detected:

        doctor = "Ophthalmology"

    elif "Ear" in detected:

        doctor = "ENT"

    elif "Dental" in detected:

        doctor = "Dentist"

    elif (
        "Breathing Difficulty" in detected
        or "Cough" in detected
        or "Fever" in detected
        or "Headache" in detected
        or "Dizziness" in detected
    ):

        doctor = "General Physician"

    else:

        doctor = "General Physician"

    # --------------------------------------------------
    # 7. Explainable AI
    # --------------------------------------------------

    reasons = []

    reasons.extend(high_priority_reasons)
    reasons.extend(attention_reasons)

    if reasons:

        explanation = (
            "DR AI HEALTHBOX generated this priority based on "
            + ", ".join(reasons)
            + "."
        )

    else:

        explanation = (
            "DR AI HEALTHBOX considered the reported symptoms, "
            "severity, duration, progression, activity impact "
            "and available health readings. "
            "No immediate concerning information was reported."
        )

    # --------------------------------------------------
    # 8. Suggested Next Steps
    # --------------------------------------------------

    if level == "High Priority":

        next_steps = [
            "Seek prompt professional medical assessment.",
            "Do not ignore symptoms that are severe or getting worse.",
            "Seek immediate medical help if serious warning signs develop."
        ]

    elif level == "Needs Attention":

        next_steps = [
            "Monitor your symptoms closely.",
            "Consider professional healthcare assessment if symptoms continue.",
            "Seek help if symptoms become worse or new concerning symptoms appear."
        ]

    else:

        next_steps = [
            "Monitor your symptoms.",
            "Maintain adequate hydration and rest.",
            "Seek professional advice if symptoms persist or worsen."
        ]

    # --------------------------------------------------
    # 9. Return Complete AI Analysis
    # --------------------------------------------------

    return {
        "level": level,
        "detected_symptoms": detected,
        "pathway": pathway,
        "doctor": doctor,
        "explanation": explanation,
        "next_steps": next_steps,
        "reading_flags": reading_flags
    }
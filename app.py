from flask import Flask, render_template, request
from ai.healthcare_logic import analyze_health_input, generate_demo_readings
app = Flask(__name__)
# Demo dashboard data
assessments = []
emergency_alerts = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    age_group = request.form.get("age_group")
    concern = request.form.get("concern", "")
    symptoms = request.form.get("symptoms", "")
    duration = request.form.get("duration")
    severity = request.form.get("severity")
    temperature = request.form.get("temperature")
    heart_rate = request.form.get("heart_rate")
    spo2 = request.form.get("spo2")

    worsening = request.form.get("worsening")
    activity_impact = request.form.get("activity_impact")
    new_symptoms = request.form.get("new_symptoms")

    analysis = analyze_health_input(
        symptoms,
        concern,
        severity,
        duration,
        worsening,
        activity_impact,
        new_symptoms,
        temperature,
        heart_rate,
        spo2
    )     # Generate simulated device readings for prototype
    demo_readings = generate_demo_readings(analysis["level"])   
    # Save assessment for dashboard
    assessments.append({
        "priority": analysis["level"],
        "symptoms": symptoms if symptoms else "No symptoms provided",
        "doctor": analysis["doctor"],

        # Simulated device readings for prototype
        "temperature": demo_readings["temperature"],
        "heart_rate": demo_readings["heart_rate"],
        "blood_pressure": demo_readings["blood_pressure"],
        "spo2": demo_readings["spo2"]
    })
    return render_template(
        "result.html",
        result=analysis["level"],
        detected_symptoms=analysis["detected_symptoms"],
        severity=severity,
        duration=duration,
        worsening=worsening,
        activity_impact=activity_impact,
        new_symptoms=new_symptoms,
        temperature=demo_readings["temperature"],
        heart_rate=demo_readings["heart_rate"],
        blood_pressure=demo_readings["blood_pressure"],
        spo2=demo_readings["spo2"],
        doctor=analysis["doctor"],
        explanation=analysis["explanation"],
        care_pathway=analysis["pathway"],
        next_steps=analysis["next_steps"]
    )


@app.route("/emergency", methods=["POST"])
def emergency():
    emergency_type = request.form.get("emergency_type")

    # Save emergency alert for dashboard
    emergency_alerts.append({
        "type": emergency_type
    })

    return render_template(
        "emergency.html",
        emergency_type=emergency_type
    )
@app.route("/dashboard")
def dashboard():
    total_cases = len(assessments)

    high_cases = sum(
        1 for assessment in assessments
        if assessment["priority"] == "High Priority"
    )

    medium_cases = sum(
        1 for assessment in assessments
        if assessment["priority"] == "Needs Attention"
    )

    low_cases = sum(
        1 for assessment in assessments
        if assessment["priority"] == "Low Priority"
    )

    return render_template(
        "dashboard.html",
        total_cases=total_cases,
        high_cases=high_cases,
        medium_cases=medium_cases,
        low_cases=low_cases,
        assessments=assessments,
        emergency_alerts=emergency_alerts
    )

if __name__ == "__main__":
    app.run(debug=True)
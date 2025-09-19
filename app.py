from flask import Flask, render_template, request
from groq import Groq
import re
import math
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------------
# Body Fat & LBM calculations
# -----------------------------
def calculate_body_composition(gender, height, weight, waist, neck, hip=None):
    height = float(height)
    weight = float(weight)
    waist = float(waist)
    neck = float(neck)
    hip = float(hip) if hip else None

    if gender.lower() == "male":
        # U.S. Navy formula for men
        body_fat = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
    else:
        # U.S. Navy formula for women
        body_fat = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387

    # Lean Body Mass
    lbm = weight * (1 - body_fat / 100)

    # Approx Muscle Mass (derived as 50% of LBM, rough estimate)
    muscle_mass = lbm * 0.5

    return round(body_fat, 2), round(lbm, 2), round(muscle_mass, 2)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Collect user inputs
        height = request.form.get("height")
        weight = request.form.get("weight")
        age = request.form.get("age")
        gender = request.form.get("gender")
        activity = request.form.get("activity")
        budget = request.form.get("budget")
        allergy = request.form.get("allergy")
        preference = request.form.get("preference")
        region = request.form.get("region")
        waist = request.form.get("waist")
        neck = request.form.get("neck")
        hip = request.form.get("hip")

        # Calculate body fat, LBM, muscle mass
        body_fat, lbm, muscle_mass = calculate_body_composition(gender, height, weight, waist, neck, hip)

        # Prompt for AI
        prompt = f"""
You are an expert Indian dietitian with knowledge of all Indian states and their regional specialties.
User details:
- Height: {height} cm
- Weight: {weight} kg
- Age: {age}
- Gender: {gender}
- Activity level: {activity}
- Dietary preference: {preference}
- Allergies: {allergy}
- Budget: {budget}
- Region/State: {region}
- Body Fat %: {body_fat}
- Lean Body Mass (kg): {lbm}
- Muscle Mass (kg): {muscle_mass}

Create a **weekly Indian diet plan** (Monday to Sunday) tailored to the user's body type, fat %, and muscle mass.
**Requirements**:
1. Include **regional-specific dishes** popular in the user's state.
2. Mention **calories, protein, carbs, fats** for each meal.
3. Explain in **friendly, short sentences why this meal is healthy**.
4. Include **breakfast, lunch, dinner, snacks**.
5. Use **bullets, emojis, and easy-to-read formatting**, no markdown symbols.
6. Make it **detailed but user-friendly**.
7. At the end, include a disclaimer: ⚠️ Not medical advice, consult a doctor or nutritionist.
"""

        # Groq API call
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )

        # Extract AI response
        ai_response = response.choices[0].message.content

        # Clean AI output
        ai_response = re.sub(r"\*\*(.*?)\*\*", r"\1", ai_response)
        ai_response = ai_response.replace("* ", "• ")

        return render_template("result.html", ai_response=ai_response,
                               body_fat=body_fat, lbm=lbm, muscle_mass=muscle_mass)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

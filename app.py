from flask import Flask, render_template, request
from groq import Groq
import re
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Groq API key from .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

Create a **weekly Indian diet plan** (Monday to Sunday) tailored to the user's body and lifestyle.
**Requirements**:
1. Include **regional-specific dishes** popular in the user's state.
2. Mention **calories, protein, carbs, fats** for each meal.
3. Explain in **friendly, short sentences why this meal is healthy**.
4. Include **breakfast, lunch, dinner, snacks**.
5. Use **bullets, emojis, and easy-to-read formatting**, no markdown symbols like ** or *.
6. Make it **detailed but user-friendly**.
7. At the end, include a **disclaimer**: ⚠️ Not medical advice, consult a doctor or nutritionist.

Example: 
- Breakfast: Dosa with coconut chutney (200 cal, 6g protein, 35g carbs, 5g fat) 🥞
  Why it's healthy: Good source of protein & carbs, keeps energy steady.

Generate **all meals similarly** and consider allergies & dietary preferences.
"""

        # Groq API call
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )

        # Extract AI response
        ai_response = response.choices[0].message.content

        # Clean AI output: remove ** and simplify bullets
        ai_response = re.sub(r"\*\*(.*?)\*\*", r"\1", ai_response)
        ai_response = ai_response.replace("* ", "• ")

        return render_template("result.html", ai_response=ai_response)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

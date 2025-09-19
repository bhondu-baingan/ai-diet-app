# 🥗 Indian Diet AI

**Indian Diet AI** is a Flask-based web application that generates **personalized weekly Indian diet plans** using the **Groq AI API**.  
It tailors meal recommendations based on user details like **age, weight, height, gender, dietary preferences, allergies, budget, and region/state**.

The app emphasizes **regional-specific Indian dishes**, ensuring healthier and culturally relevant choices.

---

## ✨ Features
- ✅ Personalized diet plans (Mon–Sun)  
- ✅ Regional & state-specific Indian meals  
- ✅ Nutritional values (calories, protein, carbs, fats)  
- ✅ User-friendly output with emojis & simple text  
- ✅ Dietary preferences & allergies support  
- ✅ Budget-friendly suggestions  
- ✅ Modern UI with pastel theme  

---

## 🚀 Tech Stack
- Python 3  
- Flask  
- Groq AI API (LLaMA model)  
- HTML, CSS (pastel UI)  

---

## 🔑 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/indian-diet-ai.git
cd indian-diet-ai
```
### 2️⃣ Create & activate virtual environment
```bash
python -m venv venv
```
On Windows:

```bash
venv\Scripts\activate
```
On Mac/Linux:

```bash
source venv/bin/activate
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Set up environment variables
Create a .env file in the project root and add:

```env
GROQ_API_KEY=your_api_key_here
```
👉 You can get your free API key from Groq Console.

### 5️⃣ Run the Flask app
```bash
python app.py
```
### 6️⃣ Open in browser
Go to:
👉 http://127.0.0.1:5000/

📝 Usage
Enter your age, weight, height, gender, state, budget, allergies, and preferences.

Click Generate Plan.

Get a personalized weekly Indian diet chart with nutritional info.

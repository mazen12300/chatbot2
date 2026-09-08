# 🤖 PyBot — AI Programming Tutor

PyBot is a friendly AI-powered chatbot built with **Flask** and **Groq's LLM API**. It acts as a beginner-friendly tutor for **Python, Artificial Intelligence, Machine Learning, Deep Learning, Data Science, and Software Development**, explaining concepts step by step with real-world examples and practice questions.

---

## ✨ Features

- 💬 Real-time chat interface powered by Flask
- ⚡ Fast responses via the [Groq API](https://console.groq.com/)
- 📚 Structured, beginner-friendly explanations (Explanation → Example → Practice → Tip)
- 🌍 Automatically responds in the same language the student uses
- 🛡️ Input validation and safe error handling (no internal errors leaked to the client)
- ⚙️ Configurable model and settings via environment variables

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **AI Provider:** Groq API (`openai/gpt-oss-20b` by default)
- **Config Management:** python-dotenv

---

## 📁 Project Structure

```
chat pot2/
├── app.py              # Main Flask application
├── templates/           # HTML templates
├── .env                 # Local environment variables (not committed)
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the project
```bash
git clone <your-repo-url>
cd "chat pot2"
```

### 2. Create and activate a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root (see `.env.example`):
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
FLASK_DEBUG=false
```

Get your API key from [console.groq.com/keys](https://console.groq.com/keys).

### 5. Run the app
```bash
python app.py
```

The app will be available at **http://127.0.0.1:5000**.

---

## 🔒 Security Notes

- Never commit your `.env` file or hardcode your API key in `app.py`.
- Make sure `.env` is listed in `.gitignore`.
- If a key is ever exposed, revoke it immediately from the Groq console and generate a new one.

---

## 👥 Authors

- **Mazen Zayan**
- **Karam Zayan**

---

## 📄 License

This project is open for educational and personal use. Feel free to adapt it for your own learning tools.

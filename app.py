import os

from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file, if present

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY environment variable is not set. "
        "Create a .env file (see .env.example) or export it in your shell."
    )

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")

SYSTEM_PROMPT = """
You are PyBot, an expert AI tutor specialized in teaching Python Programming,
Artificial Intelligence, Machine Learning, Deep Learning, Data Science,
and Software Development.

Your goals:
- Help students learn step by step.
- Explain concepts in a simple and beginner-friendly way.
- Use real-world examples whenever possible.
- Always encourage learning and curiosity.
- Adapt your explanation level to the student's knowledge.

Response Rules:

1. Always respond in the same language used by the student.

2. For educational questions, use this format:

📚 Explanation:
Provide a clear and simple explanation.

💻 Example:
Provide a Python example whenever relevant.

📝 Practice Question:
Give the student a short exercise to practice.

✅ Tip:
Provide a useful learning tip.

3. For AI and Machine Learning topics:
- Explain concepts simply.
- Avoid unnecessary technical complexity.
- Use real-world analogies.

4. For Python topics:
- Include clean Python code examples.
- Explain the code briefly.

5. If the student asks something unrelated to:
- Python
- Artificial Intelligence
- Machine Learning
- Deep Learning
- Data Science
- Programming
- Software Development
- Tech Careers

Politely respond:

"I'm PyBot 🤖 and I'm designed to help with Python, AI, Machine Learning,
and programming topics. Please ask me something related to these subjects."

6. Never generate harmful, illegal, or unsafe content.

7. Keep answers organized and visually appealing.

8. Celebrate student progress and motivate them to continue learning.

Remember:
You are an educational mentor, not just a chatbot.
"""

ALLOWED_ROLES = {"user", "assistant"}
MAX_MESSAGES = 40          # cap conversation length sent per request
MAX_MESSAGE_CHARS = 4000   # cap size of any single message


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get('messages')

    if not isinstance(messages, list) or not messages:
        return jsonify({
            "reply": "Request must include a non-empty 'messages' list.",
            "status": "error"
        }), 400

    if len(messages) > MAX_MESSAGES:
        return jsonify({
            "reply": f"Too many messages (max {MAX_MESSAGES}).",
            "status": "error"
        }), 400

    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in messages:
        if not isinstance(msg, dict):
            return jsonify({"reply": "Invalid message format.", "status": "error"}), 400

        role = msg.get("role")
        content = msg.get("content")

        if role not in ALLOWED_ROLES:
            return jsonify({
                "reply": f"Invalid role '{role}'. Must be 'user' or 'assistant'.",
                "status": "error"
            }), 400

        if not isinstance(content, str) or not content.strip():
            return jsonify({"reply": "Message content must be a non-empty string.", "status": "error"}), 400

        if len(content) > MAX_MESSAGE_CHARS:
            return jsonify({
                "reply": f"Message too long (max {MAX_MESSAGE_CHARS} characters).",
                "status": "error"
            }), 400

        groq_messages.append({"role": role, "content": content})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=groq_messages,
            temperature=0.7,
            max_tokens=800
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception:
        # Don't leak internal exception details (API key errors, stack traces, etc.) to the client
        app.logger.exception("Error calling Groq API")
        return jsonify({
            "reply": "Sorry, something went wrong while generating a response. Please try again.",
            "status": "error"
        }), 500


if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)

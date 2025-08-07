# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

quiz = [
    {"question": "What is encapsulation in Java?", "answers": {"a": "Wrapping data and methods into a single unit", "b": "Hiding the main class", "c": "Using inheritance", "d": "None of the above"}, "correctAnswer": "a"},
    {"question": "Which operator is used to compare two values?", "answers": {"a": "=", "b": "==", "c": "===", "d": "!="}, "correctAnswer": "b"},
    {"question": "Which keyword is used for inheritance in Java?", "answers": {"a": "inherits", "b": "extends", "c": "implements", "d": "super"}, "correctAnswer": "b"},
    # Add more up to 20 questions here...
]

@app.route('/')
def index():
    return render_template("index.html", quiz_data=quiz)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.json
    score = sum(1 for i, q in enumerate(quiz) if i < len(user_answers) and user_answers[i] == q['correctAnswer'])
    return jsonify({"score": score})

if __name__ == '__main__':
    app.run(debug=True)

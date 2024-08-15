from flask import Flask, request, jsonify, render_template, session
from datetime import timedelta
from flask_session import Session
import openai
import os
from dotenv import load_dotenv


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'  # Storing sessions on the filesystem
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 5)

Session(app)

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def load_allergy_info(filepath):
    with open(filepath, 'r') as file:
        return file.read()


allergy_info = load_allergy_info('allergy documents-txt/allergy_summaries_combined.txt')



def query_gpt_next_question(conversation_history, asked_questions):
    prompt = "Considering the conversation so far, ask a single, direct question to clarify the user's allergy symptoms or triggers. Ensure that no similar questions are asked more than once."
    while True:
        conversation_history.append({"role": "system", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0.5,
            max_tokens=200,
        )
        next_question = response.choices[0].message['content'].strip()
        conversation_history.pop()

        # Normalize the question for the uniqueness check.
        normalized_next_question = next_question.lower().strip()

        if normalized_next_question not in asked_questions and next_question.endswith('?'):
            # Add the normalized version
            asked_questions.add(normalized_next_question)
            return next_question


def make_final_prediction(conversation_history):
    prompt = "Now that you have gathered enough information, please provide a prediction about the user's potential allergies."
    conversation_history.append({"role": "system", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.5,
        max_tokens=200,
    )
    prediction = response.choices[0].message['content'].strip()
    conversation_history.pop()
    return prediction


conversation_history = []
asked_questions = set()
number_of_questions_asked = 0


@app.route('/')
def index():
    # Initialize user-specific session data
    if 'conversation_history' not in session:
        session['conversation_history'] = [
            {"role": "system", "content": "You are an AI trained to help users identify potential allergies."},
            {"role": "system", "content": allergy_info},
            {"role": "assistant", "content": "Hello! I'm here to help you identify potential allergies. Can you describe any allergic reactions you've experienced?"}
        ]
        session['asked_questions'] = set()
        session['number_of_questions_asked'] = 0

    greeting_message = session['conversation_history'][-1]['content']
    return render_template('index.html', greeting_message=greeting_message)

@app.route('/interact', methods=['POST'])
def interact():
    user_input = request.json['user_input']
    if 'conversation_history' not in session or 'asked_questions' not in session or 'number_of_questions_asked' not in session:
        session['conversation_history'] = [
            {"role": "system", "content": "You are an AI trained to help users identify potential allergies."},
            {"role": "system", "content": allergy_info},
            {"role": "assistant", "content": "Hello! I'm here to help you identify potential allergies. Can you describe any allergic reactions you've experienced?"}
        ]
        session['asked_questions'] = set()
        session['number_of_questions_asked'] = 0

    # Now we're sure that session keys exist, we can safely append to conversation_history
    session['conversation_history'].append({"role": "user", "content": user_input})

    if session['number_of_questions_asked'] < 10:
        ai_output = query_gpt_next_question(
            session['conversation_history'], session['asked_questions'])
        session['number_of_questions_asked'] += 1
    elif session['number_of_questions_asked'] == 10:
        ai_output = make_final_prediction(session['conversation_history'])
        session['number_of_questions_asked'] += 1
    else:
        ai_output = "Our assessment is complete. If you have further questions, please consult a healthcare professional."

    session.modified = True  # Ensure session is marked as modified for changes to be saved
    return jsonify({"ai_output": ai_output})



if __name__ == '__main__':
    app.run(debug=True)

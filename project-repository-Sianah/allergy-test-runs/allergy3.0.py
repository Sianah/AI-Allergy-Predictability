import time
import openai
from dotenv import load_dotenv
import os
import sys

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def load_allergy_info(filepath):
    with open(filepath, 'r') as file:
        allergy_info = file.read()
    return allergy_info


def query_gpt_next_question(conversation_history, asked_questions):
    """
    Queries GPT for the next question based on the conversation history and
    filters out any repeated questions. Adjusts the prompt to encourage single, direct questions.
    """
    prompt = "Considering the conversation so far, ask a single, direct question to clarify the user's allergy symptoms or triggers."
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

        if next_question not in asked_questions and next_question.endswith('?'):
            asked_questions.add(next_question)
            return next_question


def allergy_assistant(allergy_info):
    
    conversation_history = [
        {"role": "system", "content": "You are an AI trained to help users identify potential allergies by asking a series of questions about their symptoms and history."},
        # Add the content of the text file to the history
        {"role": "system", "content": allergy_info},
    ]

    asked_questions = set()
    print("AI: Hello! I'm here to help you identify potential allergies. Can you describe any allergic reactions you've experienced?")

    while len(asked_questions) < 10:  # Ensure 10 unique questions
        user_input = input("You: ")
        conversation_history.append({"role": "user", "content": user_input})

        ai_output = query_gpt_next_question(
            conversation_history, asked_questions)
        print(f"AI: {ai_output}")

        time.sleep(2)

    conversation_history.append({
        "role": "system",
        "content": "Now that you have gathered enough information, please provide a prediction about the user's potential allergies."
    })
    # Ask for a prediction
    for _ in range(10):
        start_time = time.time()
        start_memory = get_current_memory_usage()

        ai_prediction = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0.5,
            max_tokens=200,
        ).choices[0].message['content'].strip()

        elapsed_time = time.time() - start_time
        memory_used = get_current_memory_usage() - start_memory

        print(f"AI: {ai_prediction}")
        print(f"Time taken for prediction: {elapsed_time:.2f} seconds")
        print(f"Additional memory used for prediction: {memory_used:.2f} MB")

def get_current_memory_usage():
    """Return the current memory usage of the Python process."""
    import os
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB


allergy_info = load_allergy_info(
    'allergy-detection-gpt/allergy documents-txt/allergy_summaries_combined.txt')

if __name__ == "__main__":
    allergy_assistant(allergy_info)

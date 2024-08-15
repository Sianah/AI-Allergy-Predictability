import time
import openai

openai.api_key = 'API-KEY'

def query_gpt_next_question(conversation_history, asked_questions):
    """
    Queries GPT for the next question based on the conversation history and
    filters out any repeated questions.
    """
    prompt = "What is the next question I should ask to gather more information about the user's potential allergies?"
    while True:
        conversation_history.append({
            "role": "system",
            "content": prompt
        })

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0.5,
            max_tokens=150,
        )

        next_question = response.choices[0].message['content'].strip()

        conversation_history.pop()

        if next_question not in asked_questions and next_question.endswith('?'):
            asked_questions.add(next_question)
            return next_question

def allergy_assistant():
    conversation_history = [
        {"role": "system", "content": "You are an AI trained to help users identify potential allergies by asking a series of questions about their symptoms and history."},
    ]

    asked_questions = set() 
    print("AI: Hello! I'm here to help you identify potential allergies. Can you describe any allergic reactions you've experienced?")

    for _ in range(10): 
        user_input = input("You: ")
        conversation_history.append({"role": "user", "content": user_input})
        
        ai_output = query_gpt_next_question(conversation_history, asked_questions)
        print(f"AI: {ai_output}")

        time.sleep(2) 

    conversation_history.append({
        "role": "system",
        "content": "Now that you have gathered enough information, please provide a prediction about the user's potential allergies."
    })

    ai_prediction = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.5,
        max_tokens=150,
    ).choices[0].message['content'].strip()
    
    print(f"AI: {ai_prediction}")

if __name__ == "__main__":
    allergy_assistant()












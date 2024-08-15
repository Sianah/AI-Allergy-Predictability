import time
import openai

# NEXT STEPS(for now):
# 1. ALLOW THE AI TO ASK THE QUESTIONS IN A LOOP(check)
# 2. ADD A FUNCTION TO LOAD ALLERGENS INFO FROM A FILE AND THAT GPT READS FROM IT TO GIVE OUTPUT(check)
# 3. ENSURE USER CAN'T ASK GPT ANY NON-ALLERGY RELATED QUESTIONS, AND THAT PROPER RESPONSE IS GIVEN IF THE USER DOES SO(checK)
# 4. ENSURE THAT GPT CAN USE REAL WORLD DATA ALONGSIDE FED INFO AS WELL TO GIVE OUTPUT(checK)
# 5. MAKE WEB APP
# 5.5. Maybe allow AI to ask more than ten questions(?)
# 6. FIGURE OUT HOW TO HIDE API KEY(check)


def load_allergens_info(filepath):
    allergens_info = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            allergen = parts[0]
            symptoms = parts[1].split(',')
            exposures = parts[2].split(',')
            allergens_info[allergen] = {
                "symptoms": symptoms, "exposures": exposures}
    return allergens_info


def query_gpt_about_allergies(user_responses):
    user_summary = " ".join(user_responses)

    gpt_prompt = f"Considering the symptoms and conditions described: {user_summary}, based on common knowledge and data, what could be the most likely allergies? Provide a reasoned analysis based on patterns seen in real-world data."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI trained on a wide range of medical texts, including information about allergies and symptoms."},
            {"role": "user", "content": gpt_prompt},
        ],
        temperature=0.5,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response['choices'][0]['message']['content'].strip()


openai.api_key = 'API-KEY'


def allergy_assistant():
    filepath = 'allergens_info.txt'
    allergens_info = load_allergens_info(filepath)

    messages = [
        {
            "role": "system",
            "content": ("Welcome to the Allergy Guessing AI! This tool is designed to help you uncover potential allergies based on a series of questions. "
                        "Please answer each question to the best of your knowledge. Let's get started!")
        },
        {
            "role": "system",
            "content": "Have you experienced any allergic reactions recently? Please describe your symptoms (e.g., sneezing, itching, rash)."
        },
        {
            "role": "system",
            "content": "How long have you experienced these symptoms, and how frequently do they occur?"
        },
        {
            "role": "system",
            "content": ("Think about when your symptoms occur. Are they worse indoors, outdoors, or both? This can help us identify if your allergies "
                        "are related to indoor allergens like dust mites or outdoor allergens like pollen.")
        },
        {
            "role": "system",
            "content": "Have you noticed if your symptoms worsen after eating certain foods? If yes, please specify which foods."
        },
        {
            "role": "system",
            "content": "Do you have pets or have you been around animals recently when your symptoms occurred?"
        },
        {
            "role": "system",
            "content": "Do any of your immediate family members have allergies? Knowing if allergies run in your family can help identify your own potential allergies."
        },
        {
            "role": "system",
            "content": "Have you been diagnosed with any allergies in the past? If so, what are they?"
        },
        {
            "role": "system",
            "content": "Do your symptoms appear or worsen during specific seasons? This can indicate seasonal allergies, such as to pollen."
        },
        {
            "role": "system",
            "content": "Have you ever undergone allergy testing (skin test, blood test)? If yes, what were the results?"
        },
        {
            "role": "system",
            "content": "Please describe any recent changes in your lifestyle, home, or work environment. Changes in your environment can introduce new allergens."
        },
        {
            "role": "system",
            "content": ("Thank you for answering the questions. Based on your responses, the AI is analyzing the information to guess your potential allergies.")
        },
        {
            "role": "system",
            "content": ("Based on the information provided, you may have allergies to [Allergen(s)]. Please note that this AI tool is for informational purposes only and not "
                        "a substitute for professional medical advice. We recommend consulting with an allergist for official diagnosis and treatment.")
        },
        {
            "role": "system",
            "content": ("Would you like to learn more about managing these potential allergies or book an appointment with an allergy specialist? Please let us know!")
        }
    ]

    user_responses = []

    for message in messages:
        print(f"AI: {message['content']}")

        if message['content'] != messages[-1]['content']:
            user_input = input("You: ")
            user_responses.append(user_input)

    print("\nAI: Analyzing your responses...")
    time.sleep(2)

    gpt_analysis = query_gpt_about_allergies(user_responses)
    print(f"\nAI: {gpt_analysis}")


if __name__ == "__main__":
    allergy_assistant()

import time
import openai

# Make sure to replace 'your-api-key-here' with your actual OpenAI API key
openai.api_key = 'API-KEY'

def load_allergens_info(filepath):
    """
    Load allergens information from a specified file.
    """
    allergens_info = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) < 3:  # Ensure there are enough parts
                continue
            allergen = parts[0]
            symptoms = parts[1].split(',')
            exposures = parts[2].split(',')
            allergens_info[allergen] = {
                "symptoms": symptoms, "exposures": exposures}
    return allergens_info


def query_gpt_about_allergies(user_responses, allergens_info):
    """
    Query GPT with the user's responses and consider allergens information in its analysis.
    """
    user_summary = " ".join(user_responses)

    # Integrating the allergens information into the system message
    allergens_summary = "; ".join([f"{allergen}: symptoms - {', '.join(info['symptoms'])}, exposures - {', '.join(info['exposures'])}" 
                                    for allergen, info in allergens_info.items()])
    system_message = f"You are an AI trained on a wide range of medical texts, including information about allergies and symptoms, and the following specific allergens information: {allergens_summary}."

    gpt_prompt = f"Considering the symptoms and conditions described: {user_summary}, what could be the most likely allergies? Provide a reasoned analysis."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": gpt_prompt},
        ],
        temperature=0.5,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response['choices'][0]['message']['content'].strip()

def allergy_assistant():
    """
    Main function to interact with the user, collecting responses to predefined questions about allergies,
    and using those responses along with allergens information for GPT analysis.
    """
    filepath = 'allergy-detection-gpt/allergy documents-txt/allergy_summaries_combined.txt'
    allergens_info = load_allergens_info(filepath)

    messages = [
        {"content": "Welcome to the Allergy Guessing AI! This tool is designed to help you uncover potential allergies based on a series of questions. Please answer each question to the best of your knowledge. Let's get started!"},
        {"content": "Have you experienced any allergic reactions recently? Please describe your symptoms (e.g., sneezing, itching, rash)."},
        {"content": "How long have you experienced these symptoms, and how frequently do they occur?"},
        {"content": "Think about when your symptoms occur. Are they worse indoors, outdoors, or both? This can help us identify if your allergies are related to indoor allergens like dust mites or outdoor allergens like pollen."},
        {"content": "Have you noticed if your symptoms worsen after eating certain foods? If yes, please specify which foods."},
        {"content": "Do you have pets or have you been around animals recently when your symptoms occurred?"},
        {"content": "Do any of your immediate family members have allergies? Knowing if allergies run in your family can help identify your own potential allergies."},
        {"content": "Have you been diagnosed with any allergies in the past? If so, what are they?"},
        {"content": "Do your symptoms appear or worsen during specific seasons? This can indicate seasonal allergies, such as to pollen."},
        {"content": "Have you ever undergone allergy testing (skin test, blood test)? If yes, what were the results?"},
        {"content": "Please describe any recent changes in your lifestyle, home, or work environment. Changes in your environment can introduce new allergens."},
        {"content": "Thank you for answering the questions. Based on your responses, the AI is analyzing the information to guess your potential allergies."},
    ]

    user_responses = []

    for message in messages:
        print(f"AI: {message['content']}")

        # Assuming the last message does not require a user response, so skipping input
        if message['content'] != messages[-2]['content']:
            user_input = input("You: ")
            user_responses.append(user_input)

    print("\nAI: Analyzing your responses...")
    time.sleep(2)  # Simulate processing time

    # Pass both the user responses and the loaded allergen information to GPT
    gpt_analysis = query_gpt_about_allergies(user_responses, allergens_info)
    print(f"\nAI: {gpt_analysis}")

    # Final message about informational purpose and recommendation to see a specialist
    print(messages[-1]['content'])

if __name__ == "__main__":
    allergy_assistant()


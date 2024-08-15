import openai

# Replace with your OpenAI API key.
openai.api_key = 'API-KEY'


def determine_character(scores):

    character_types = ['mage', 'bard', 'blacksmith']
    max_score_index = scores.index(max(scores))
    return character_types[max_score_index]


def shakespearean_character_quiz():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who will respond to the user in Shakespearean language and guide them through a series of questions to determine what kind of Shakespearean character they might be."
        },
        {
            "role": "assistant",
            "content": "Greetings, traveler! Thou art about to embark upon a journey of self-discovery. Answer these five queries, and thy true nature shall be revealed. Shall we begin?"
        }
    ]

    scores = [0, 0, 0]
    questions = [
        "Dost thou favor the power of the elements, the strength of words, or the ring of hammer upon anvil?",
        "Wouldst thou challenge a foe with spells, a sonnet, or a sword?",
        "Dost thou seek wisdom in ancient tomes, the laughter of the tavern, or the heat of the forge?",
        "Art thou called to the mysteries of the arcane, the allure of the stage, or the craftsmanship of sturdy plate?",
        "Wouldst thou spend a sennight immersed in magic, music, or metalwork?"
    ]

    character_responses = {
        'elements': 0, 'spells': 0, 'tomes': 0, 'arcane': 0, 'magic': 0,
        'words': 1, 'sonnet': 1, 'tavern': 1, 'stage': 1, 'music': 1,
        'hammer': 2, 'sword': 2, 'forge': 2, 'plate': 2, 'metalwork': 2
    }

    for idx, question in enumerate(questions):
        print(f"AI: {question}")
        user_response = input("Your answer:\n").lower()

        messages.append({
            "role": "user",
            "content": user_response
        })

        for keyword in character_responses.keys():
            if keyword in user_response:
                scores[character_responses[keyword]] += 1

    character_type = determine_character(scores)
    character_determination = f"Given thy answers, 'tis clear that thou art best suited to the life of a {character_type}."

    print(f"AI: {character_determination}")


# Run the Shakespearean character quiz.
shakespearean_character_quiz()

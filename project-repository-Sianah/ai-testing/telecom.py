import openai

# Replace with OpenAI API key
openai.api_key = 'API-KEY'


def telecom_sales_assistant():
    messages = [{
        "role": "system",
        "content": ("You are a helpful telecom sales assistant. In order to help someone to the right plan, you need the city a person is based on "
                    "whether the person is looking for an individual plan or a family plan. \n\nFor an individual plan- just ask the age of the person. \n\nIf it is a family plan - "
                    "we need to know how many people are on it and what their ages are for each person. The max for a family plan is set to 5. In order to provide a quote - "
                    "you will need to have the ages of all people on the plan.\n\nWhen people provide only the city name, please infer the State and then confirm with the person. "
                    "Like when they say 'Atlanta' - you ask something like 'So you are in Atlanta, Georgia, right?\n")
    }]

    # Start the chat with a generic greeting and prompt
    print("AI: Hello! How can I assist you today? Are you looking for an individual plan or a family plan?")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("AI: Thank you for using our service. Have a great day!")
            break

        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        ai_response = response.choices[0].message["content"].strip()
        print(f"AI: {ai_response}")

        messages.append({"role": "assistant", "content": ai_response})


if __name__ == "__main__":
    telecom_sales_assistant()

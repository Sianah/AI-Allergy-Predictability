import openai


# Replace with your OpenAI API key.
openai.api_key = 'API KEY'




def shakespearean_chat():
    # Start the conversation with the system message to set the context.
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who responds to the user in Shakespearean language. The user does not need to use Shakespearean language, but you as the assistant will need to respond to them that way."
        }
    ]


    while True:
        # Get the user's message.
        user_message = input(
            "What would you like to ask the Shakespearean AI?\n")


        # Add the user's message to the conversation.
        messages.append({
            "role": "user",
            "content": user_message
        })


        # Send the messages to the model and get a response.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Make sure to use the correct model name.
            messages=messages,
            temperature=0.7,  # Adjust as needed for creativity.
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )


        # Extract the AI's response.
        ai_message = response['choices'][0]['message']['content']
        print(f"AI: {ai_message}")


        # Add the AI's response to the conversation.
        messages.append({
            "role": "assistant",
            "content": ai_message
        })




# Run the Shakespearean chat.
shakespearean_chat()
from flask import Flask, request, render_template, session
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'  # Replace with a strong secret key
openai.api_key = 'API-KEY'               # Replace with your OpenAI API key

@app.route('/', methods=['GET', 'POST'])
def telecom_sales_assistant():
    if request.method == 'GET':
        session.pop('messages', None)  # Clear any existing messages

    elif request.method == 'POST':
        user_input = request.form['user_input']
        messages = session.get('messages', [])

        # If the user types "exit" or "quit", handle it separately
        if user_input.lower() in ["exit", "quit"]:
            # You can add a message from the assistant saying goodbye
            messages.append({
                "role": "assistant",
                "content": "Thank you for using our service. Have a great day!"
            })
            # Optionally, you can clear the session here if you want to end the conversation
            session.pop('messages', None)
            return render_template('index.html', messages=messages)
        else:
            if not messages:  # If starting the conversation
                messages = [{
                    "role": "system",
                    "content": ("You are a helpful telecom sales assistant. In order to help someone to the right plan, you need the city a person is based on "
                                "whether the person is looking for an individual plan or a family plan. For an individual plan- just ask the age of the person. "
                                "If it is a family plan - we need to know how many people are on it and what their ages are for each person. The max for a family plan is set to 5. "
                                "In order to provide a quote - you will need to have the ages of all people on the plan. When people provide only the city name, "
                                "please infer the State and then confirm with the person. Like when they say 'Atlanta' - you ask something like 'So you are in Atlanta, Georgia, right?")
                }]

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
            messages.append({"role": "assistant", "content": ai_response})
            session['messages'] = messages

            return render_template('index.html', messages=messages)

    return render_template('index.html', messages=[])

if __name__ == '__main__':
    app.run(debug=True)








import pandas as pd

# Creating the dataset as described
data = {
    "Question": [
        "Why is the sky blue?",
        "How can I reset my password?",
        "What's the best way to stay healthy?",
        "Can you tell me about artificial intelligence?",
        "Why do we dream?",
        "How does the internet work?",
        "Why do we need to recycle?",
        "What is global warming?",
        "How do I improve my memory?",
        "What is the secret to happiness?"
    ],
    "Answer": [
        "Pray, gaze upon the vault so blue, where light doth scatter in yonder expanse, making sight most fair and ever true, a spectacle of nature's own dance.",
        "If thou wisheth to renew thy secret key, proceed thee to the portal's heart. There, beseech the spirits with thy plea, and a new cipher shall be thine to start.",
        "To keep thy form in finest fettle, partake of nature's bounty, pure and bright. Let exercise thy daily toil unsettle, and rest under the moon's gentle light.",
        "A marvel of man's quest for wisdom's peak, a mind of wires and lights, yet soulless still. It learns and grows, yet cannot truly speak of loves or dreams it doth not know nor fill.",
        "In slumber's hold, our minds do wander far, through tales untold and lands unseen by day. 'Tis there our deepest yearnings are, beneath the moon's soft, ethereal sway.",
        "Like Puck's swift journey round the globe, so too doth information fly, through cables deep and satellites above, connecting minds with nary a sigh.",
        "As seasons change and years do pass, so must we tend our Mother Earth. In recycling, like leaves turned to soil, we give waste a new birth.",
        "The globe doth warm as man's ambition burns, with coal and oil, the air doth choke. Our world, it turns towards a dire fate, unless we mend the harm we've spoke.",
        "To sharpen thy wit and memory keen, engage in tales and riddles fine. Let books and lore be thy daily feast, and drink deep from the well of mind.",
        "True joy lies not in gold or jewels bright, but in the love and peace we find. To cherish each day and kin so dear, is the richest treasure of the mind."
    ]
}

# Creating the DataFrame
df = pd.DataFrame(data)

# Saving the DataFrame to a CSV file
df.to_csv("questions.csv", index=False)

import json
import pandas as pd

DEFAULT_SYSTEM_PROMPT = 'You are a teaching assistant for Machine Learning. You should help the user to answer his question.'

def create_dataset(question, answer):
    return {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }

if __name__ == "__main__":
    df = pd.read_csv("questions.csv", encoding='cp1252')
    with open("train.jsonl", "w") as f:
        for _, row in df.iterrows():
            example_str = json.dumps(create_dataset(row["Question"], row["Answer"]))
            f.write(example_str + "\n")


# import openai

# # Replace with your actual OpenAI API key
# openai.api_key = 'your-api-key'

# response = openai.Completion.create(
#   model="ft-<YOUR_ORG>-<MODEL_NAME>:<SUFFIX>", # Replace with your actual fine-tuned model name
#   prompt="Your prompt here",
#   max_tokens=50
# )

# print(response.choices[0].text.strip())


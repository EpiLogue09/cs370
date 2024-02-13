from openai import OpenAI
import argparse
import numpy as np
import pandas as pd
import os

def openai_chat(question, story):
    with open('openai_api_key.txt', 'r') as file:
        api_key = file.read().strip()

    prompt = ("Now you will receive a story and a question in the end of this prompt, and\
your job is to read the story and find out if the answer to the question is \
Yes or No. You can only output one of the following 4 options: 'Yes' (when the question asked matches\
with what happened the story), 'No' (when the question asked is relevant about the story, but\
the claim or its presupposition is erroneous or wrong), 'Maybe' (when the question asked is relevant to\
the story but the claim is ambiguous and hard to deduce from the story alone if it is right or wrong), \
'Irrelevant' (when the answer of the question is not explicitly included in the story, not in the form \
of a question, or asking something completely irrelevant), or Many (the question involves too many questions\
). You should only output exactly one of the words ('Yes', 'No', 'Maybe', 'Irrelevant', 'Many‘) in all circumstances. You\
will never provide an explanation." + '\n' + "The story and the question are as follows: " + "Story: " + story + '\n' + "Question: " + question + "")

    client = OpenAI(api_key=api_key)

    #print(prompt)
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=10,
    )
    #return the response
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description='OpenAI Chatbot')
    #parser.add_argument('--prompt', type=str, help="This is a prompt")
    #let the user interact with the chatbot via realtime terminal input
    #parser.add_argument('--story', type=str, help="This is a story")
    #parser.add_argument('--question', type=str, help="This is a question")
    story = "Jack had eaten a cake full of cyanide, a poisonous substance. \
He was rushed to the hospital, and when the doctors try to save him, his wife \
was asked to sign a consent form.\
The wife refused to sign the consent form, and Jack hence died in the hospital."
    story_prompt = "Jack ate a cake and died"
    print("Thank you for playing DetectAIve! Now you will ask question to figure out what truly happened!")
    print("Your story is: " + story_prompt)
    print()
    while True:
        question = input("Ask your question (type 'exit' to exit the question mode): ")
        if question.lower() == "exit":
            break
        result = openai_chat(question, story)
        print(result)

if __name__ == "__main__":
    main()
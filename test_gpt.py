from openai import OpenAI
import argparse
import numpy as np
import pandas as pd
import os
import csv

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
        seed=1234
    )
    #return the response
    return response.choices[0].message.content

def win_or_lose(user_answer, story, surface_prompt):
    with open('openai_api_key.txt', 'r') as file:
        api_key = file.read().strip()
    client = OpenAI(api_key=api_key)
    prompt = ("Now I will give you a surface prompt, a story, and an answer. Your job is to"
              "determine if the answer about the story is correct or not and if it is the root cause of what"
              "happened in the surface prompt. Notice you can only output the exact word of either \'correct\' or \'incorrect\'. "
              "Notice that the answer must hit the core of the story to be evaluated as correct. "
              "For example, if the dog is killed by eating too much of a chocolate cake (as chocolate"
              "is toxic to dogs), the answer needs to point out the determinate details of the story that is not "
              "explicitly stated in the surface prompt. If the answer is only partially correct (the dog is died by a chemical cause, etc.),"
              "it is still considered incorrect. The answer needs to hit all criteria below to be considered as correct:"
              "1. explicitly stating the subject (a doll, a dog, a man, etc.) if the identity of this subject is not explicitly"
              " stated in the surface prompt; 2. explicitly stating all root causes of what happened in the surface prompt (if I don\'t"
              " want to step into the house again because of both there is a dead person in the house and that I had an illusion of"
              "greeting someone in the house (who is already dead), the two causes should be both narrated in the answer); 3."
              "explicitly stating how the causes are related to the strange/weird details appeared in the surface prompt, if some parts"
              "of the prompt is not accounted, the answer is considered incorrect. "
              "Now the story and the answer are as follows: " +
              "surface_prompt: " + surface_prompt + '\n' + "story: " +
              story + '\n' + "Answer: " + user_answer + "")
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=10,
        seed=1234
    )
    # return the response
    return response.choices[0].message.content

def main():
    #find the database file
    database_path = os.path.join(os.getcwd(), 'story_database\story_table.csv')
    df = pd.read_csv(database_path)
    #randomly select a story from the database
    story = df.sample(n=1)
    hidden_story = story['truth'].values[0]
    surface_prompt = story['surface_story'].values[0]

    #dummy story (Jake and the dog)
    dummy_story = "Jack is having his birthday party today. He has a 3 month old dog, who accidentally ate the whole 12oz \
chocolate cake which is intended to be given to people who comes to the house for the party. \
Since the chocolate is toxic to the dogs, and Jack's dog is a particularly young one (which makes him more sensitive to \
the toxins, i.e., chocolate). When Jack finds his dog in the living room, the dog is already dead. Jack is very sad \
and arranges a funeral for the dog. Note that the chocolate is in itself not a poison, hence you should answer 'maybe' if\
the user asks about food poisoning or anything related."
    dummy_story_prompt = "It is Jake's birthday today. His dog died in the afternoon."

    #starting the game
    print("Thank you for playing the Beta version of DetectAIve! You will act as a detective and ask any questions that can get you closer to the truth!")
    print("Your riddle is: " + surface_prompt)
    print()
    while True:
        user_question = input("Ask your question (type 'exit' to exit the question mode): ")
        if user_question.lower() == "exit":
            break
        #result = openai_chat(question, story)
        result = win_or_lose(user_question, hidden_story, surface_prompt)
        print(result)

if __name__ == "__main__":
    main()
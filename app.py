from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
import pymysql.cursors
import pymysql.cursors
from openai import OpenAI
from test_gpt import openai_chat

app = Flask(__name__)
CORS(app)

with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

with open('openai_api_key.txt', 'r') as file:
    api_key = file.read().strip()

openai_client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return "Welcome to the Story Game! Access /single_player_game to start a new game."

@app.route('/single_player_game', methods=['GET', 'POST'])
def single_player_game():
    if request.method == 'GET':
        # Fetch a random story from the database
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT surface_story, truth FROM stories")
                result = cursor.fetchall()
                random_story = random.choice(result) if result else None
                return jsonify({"surface_story": random_story['surface_story']})
        finally:
            connection.close()
    elif request.method == 'POST':
        # Get the user's question and the story from the POST request
        data = request.json
        question = data.get('question')
        story = data.get('story')
        
        # Call the OpenAI API with the user's question and the story
        response = openai_chat(question, story)
        return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
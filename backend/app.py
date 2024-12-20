import json
import logging
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from joblib import load
import sys
import os
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
import psycopg2

# Add the path to the machine_learning directory
sys.path.append(os.path.join(os.getcwd(), '../machine_learning/classic_nlp'))
from classifier import nlp_classifier

sys.path.append(os.path.join(os.getcwd(), '../machine_learning/gpt_api'))
from gpt_model import llm_response
from generate_questions import generate_multiple_choice_questions_with_gpt, generate_related_questions

# Load the model at the start
model = load('../machine_learning/classic_nlp/visitor_classifier_model.pkl')


# loading ChatGPT API
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=api_key,
)

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Visitor Classification API!"

@app.route('/scrape-and-classify', methods=['POST'])
def scrape_and_classify():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data (modify as needed based on your needs)
        title = soup.title.string if soup.title else 'No Title'
        content = soup.get_text()

        # Implement classification logic based on content
        classification = nlp_classifier(content=content, model=model)
        gpt_response = llm_response(content = content, client = client)
        # generating questions
        muilt_choice = generate_multiple_choice_questions_with_gpt(category=gpt_response, client=client, content = content)
        general_questions = generate_related_questions(category=gpt_response, client=client, content=content)
        return jsonify({
            "title": title,
            "classification": classification,
            "gpt_classification": gpt_response,
            "multi_choice_questions" : muilt_choice,
            "general_questions" : general_questions,
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

logging.basicConfig(level=logging.INFO)
# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        dbname='user_responses',
        user='postgres',
        password='Cmj74-cmj74-',
        host='localhost',
        port='5432'
    )
    return conn

def process_and_insert_data(data):
    classification = data.get('classification')
    gpt_classification = data.get('gpt_classification')
    questions = data.get('questions', {})

    multi_choice_questions = json.dumps(questions.get('multi_choice', []))  # Default to empty list
    general_questions = json.dumps(questions.get('general', []))  # Default to empty list
    user_responses = json.dumps(data.get('user_responses', {}))  # Default to empty dict
    
    try:
        # Use context managers for connection and cursor
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO questionnaire_responses (classification, gpt_classification, multi_choice_questions, general_questions, user_responses)
                    VALUES (%s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (
                    classification,
                    gpt_classification,
                    multi_choice_questions,
                    general_questions,
                    user_responses
                ))
                conn.commit()

    except Exception as e:
        logging.error("Error while inserting data: %s", e)
        raise  # Reraise the exception to handle it in the route
    

@app.route('/submit-response', methods=['POST'])
def submit_response():
    data = request.get_json()
    logging.info("Incoming data: %s", data)  # Log the incoming data
    try:
        process_and_insert_data(data)  # Function to handle your insertion logic
        return jsonify({'message': 'Responses submitted successfully!'}), 200

    except KeyError as ke:
        logging.warning("KeyError: %s", ke)
        return jsonify({'error': f'Missing key: {str(ke)}'}), 400

    except Exception as e:
        logging.error("Error processing data: %s", e)
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500



if __name__ == '__main__':
    app.run(debug=True)

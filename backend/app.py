from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from joblib import load
import sys
import os
from openai import OpenAI
# Add the path to the machine_learning directory
sys.path.append(os.path.join(os.getcwd(), '../machine_learning/classic_nlp'))

from classifier import nlp_classifier

sys.path.append(os.path.join(os.getcwd(), '../machine_learning/gpt_api'))
from gpt_model import llm_response


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
        return jsonify({
            "title": title,
            "classification": classification,
            "gpt_classification": gpt_response
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

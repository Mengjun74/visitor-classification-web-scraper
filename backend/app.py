from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

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

        # TODO: Implement classification logic based on content
        classification = classify_visitor(content)  # Placeholder function

        return jsonify({
            "title": title,
            "classification": classification
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def classify_visitor(content):
    # Example classification logic
    if "technology" in content.lower():
        return "Technology"
    elif "finance" in content.lower():
        return "Finance"
    else:
        return "General"

if __name__ == '__main__':
    app.run(debug=True)

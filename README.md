# Website Visitor Classification Tool

This project is a web-based tool designed to classify website visitors based on their interests or industry. By taking a website URL as input, the tool scrapes its content, analyzes it, and then dynamically generates relevant questions and multiple-choice options that help categorize users visiting the site. The backend is built with Python and Flask, while the frontend uses React. User responses are stored in a PostgreSQL database.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [License](#license)

## Project Overview
The primary goal of this project is to classify website visitors dynamically by analyzing a website's content and prompting users with relevant questions. It aims to enhance user profiling by providing custom questions based on user interest and industry, enabling website owners to understand visitor categories better.

## Features
- **Web Content Scraping**: Extracts content from a given URL using BeautifulSoup.
- **Dynamic Question Generation**: Uses ChatGPT API to generate industry-relevant questions.
- **Classification**: Employs ChatGPT method (this one is better) and classic machine learning models trained on the [Website Classification Dataset](https://www.kaggle.com/datasets/hetulmehta/website-classification?resource=download) to categorize user interests.
- **Frontend and Backend**: Built with Python Flask for backend and React for the frontend.
- **User Response Storage**: Responses are stored in PostgreSQL for future analysis.

## Dataset
The classic machine learning model for initial classification uses the **Website Classification Dataset** from Kaggle:
- **Link**: [Website Classification Dataset](https://www.kaggle.com/datasets/hetulmehta/website-classification?resource=download)
- **Description**: This dataset provides labeled data to train a model that classifies websites based on content, helping categorize visitors' interests.

## Technologies Used
- **Backend**: Flask, SQLAlchemy, psycopg2
- **Frontend**: React, Axios
- **Machine Learning**: scikit-learn, joblib
- **NLP and Visualization**: TfidfVectorizer, WordCloud, Matplotlib
- **Database**: PostgreSQL
- **Environment Management**: Python-dotenv
- **APIs**: OpenAI ChatGPT API (for question generation and first classification you should use your own API key)

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/website-visitor-classification.git
    cd website-visitor-classification
    ```

2. **Backend Setup**:
   - Install Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure PostgreSQL and update `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in `.env`.

   - Initialize the database by creating necessary tables (sample script provided in `/database/init.sql`).

3. **Frontend Setup**:
   - Navigate to the `frontend` directory and install dependencies:
     ```bash
     cd frontend
     npm install
     ```

4. **Environment Variables**:
   - Create a `.env` file in the root directory with the following:
     ```plaintext
     OPENAI_API_KEY=<your_openai_api_key>
     DB_NAME=user_responses
     DB_USER=postgres
     DB_PASSWORD=your_password
     DB_HOST=localhost
     DB_PORT=5432
     ```

5. **Start the Application**:
   - Run the Flask server:
     ```bash
     python app.py
     ```
   - Run the React frontend:
     ```bash
     npm start
     ```

## Usage
1. **Input**: Enter the URL of a website you want to analyze.
2. **Scraping and Analysis**: The backend scrapes the website content and uses it to generate questions that help categorize the user.
3. **Response Submission**: Users answer questions, which are then saved to the PostgreSQL database.

## License
This project is licensed under the MIT License.

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


# Load dataset
df = pd.read_csv("../data/website_classification.csv")

# 1. Data Preprocessing
X = df['cleaned_website_text']
y = df['Category']

# 2. Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Pipeline: Vectorization and Model Training
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)), 
    ('clf', MultinomialNB())
])

pipeline.fit(X_train, y_train)

# 5. Save the model
joblib.dump(pipeline, 'visitor_classifier_model.pkl')

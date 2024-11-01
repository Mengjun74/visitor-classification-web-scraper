import joblib

# Load the model
model = joblib.load('visitor_classifier_model.pkl')

def classify_visitor(content):
    # Use the model to predict the category
    prediction = model.predict([content])
    return prediction[0]

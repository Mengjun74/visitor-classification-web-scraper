def nlp_classifier(content, model):
    prediction = model.predict([content])
    return prediction[0]

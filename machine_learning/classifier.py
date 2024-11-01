

def classify_visitor(content, model):
    prediction = model.predict([content])
    return prediction[0]

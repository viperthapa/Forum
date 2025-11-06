import os
import pickle

from django.conf import settings

model = None
vectorizer = None
model_path = os.path.join(settings.BASE_DIR, 'question_model.pkl')
vectorizer_path = os.path.join(settings.BASE_DIR, 'vectorizer.pkl')
try:
    with open(model_path, 'rb') as mf:
        model = pickle.load(mf)
    with open(vectorizer_path, 'rb') as vf:
        vectorizer = pickle.load(vf)
except FileNotFoundError:
    # Model files not present — we'll handle below and show a friendly error
    model = None
    vectorizer = None

def predict_category(question):
    # Convert text → vector
    question_vector = vectorizer.transform([question])
    
    # Predict category
    prediction = model.predict(question_vector)[0]
    return prediction
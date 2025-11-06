import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load CSV
df = pd.read_csv("questions_category.csv")   # columns: category, question

# Use the question column as input (text)
X = df["question"].astype(str)
y = df["category"].astype(str)

# Convert text → vectors
vectorizer = TfidfVectorizer(stop_words='english')
X_vectors = vectorizer.fit_transform(X)

# Split training/testing
X_train, X_test, y_train, y_test = train_test_split(
    X_vectors, y, test_size=0.2, random_state=42
)

# Train model (Logistic Regression works very well)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Accuracy (optional)
print("Training accuracy:", model.score(X_train, y_train))
print("Test accuracy:", model.score(X_test, y_test))

# Save model + vectorizer
with open("question_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved successfully.")

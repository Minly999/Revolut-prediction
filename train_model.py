import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def train_ai():
    input_file = "data/cleaned_reviews.csv"
    
    if not os.path.exists(input_file):
        print(f"[ERROR] Could not find {input_file}")
        return

    print("[INFO] Loading cleaned dataset...")
    df = pd.read_csv(input_file)

    df = df.dropna(subset=['cleaned_text'])

    X = df['cleaned_text']
    y = df['sentiment']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"[INFO] Training on {len(X_train)} reviews, testing on {len(X_test)} reviews.")

    print("[INFO] Vectorizing text features via TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000)
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    print("[INFO] Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vectorized, y_train)

    print("[INFO] Training complete. Evaluating model performance...")
    predictions = model.predict(X_test_vectorized)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f"\n{'='*40}")
    print(f"MODEL ACCURACY SCORE: {accuracy * 100:.2f}%")
    print(f"{'='*40}\n")
    
    print("[INFO] Classification Report:")
    print(classification_report(y_test, predictions, target_names=['Negative (1-Star)', 'Positive (5-Star)']))

    if not os.path.exists('models'):
        os.makedirs('models')
    
    joblib.dump(model, 'models/sentiment_model.pkl')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    print("[SUCCESS] Model and vectorizer artifacts saved to 'models/' folder.")

if __name__ == "__main__":
    train_ai()
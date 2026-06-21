import joblib
import re
import nltk
from nltk.corpus import stopwords
import os

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    cleaned_words = [w for w in words if w not in stop_words]
    return ' '.join(cleaned_words)

def run_tester():
    model_path = 'models/sentiment_model.pkl'
    vec_path = 'models/tfidf_vectorizer.pkl'

    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        print("[ERROR] Model files missing.")
        return

    print("[INFO] Loading model files...")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    
    print("\n[READY] Sentiment analyzer ready.")
    print("[INFO] Type your review below. Type 'quit' to exit.")
    print("-" * 50)

    while True:
        user_input = input("\nWrite a review: ")
        
        if user_input.lower().strip() == 'quit':
            print("[INFO] Shutting down.")
            break
            
        if not user_input.strip():
            continue

        cleaned_input = clean_text(user_input)
        
        vectorized_input = vectorizer.transform([cleaned_input])
        
        prediction = model.predict(vectorized_input)[0]
        probabilities = model.predict_proba(vectorized_input)[0]
        
        print("\n[ANALYSIS]")
        print(f"Cleaned Text: '{cleaned_input}'")
        
        if prediction == 1:
            confidence = probabilities[1] * 100
            print(f"Prediction:   5-STAR (Positive)")
            print(f"Confidence:   {confidence:.2f}%")
        else:
            confidence = probabilities[0] * 100
            print(f"Prediction:   1-STAR (Negative)")
            print(f"Confidence:   {confidence:.2f}%")
        print("-" * 50)

if __name__ == "__main__":
    run_tester()
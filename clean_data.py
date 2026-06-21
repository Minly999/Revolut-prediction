import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import os

nltk.download('stopwords', quiet=True)

def clean_text(text):
    text = str(text).lower()
    
    text = re.sub(r'[^a-z\s]', '', text)
    
    words = text.split()
    
    stop_words = set(stopwords.words('english'))
    cleaned_words = [w for w in words if w not in stop_words]
    
    return ' '.join(cleaned_words)

def process_data():
    input_file = "data/raw_reviews.csv"
    output_file = "data/cleaned_reviews.csv"

    if not os.path.exists(input_file):
        print(f"[ERROR] Could not find {input_file}.")
        return

    print("[INFO] Loading raw reviews...")
    df = pd.read_csv(input_file)
    print(f"[INFO] Original dataset size: {len(df)} rows")

    print("[INFO] Cleaning text data...")
    df['cleaned_text'] = df['text'].apply(clean_text)

    df = df[df['cleaned_text'].str.strip() != '']

    print("[INFO] Converting ratings to binary sentiment (5=1, 1=0)...")
    df['sentiment'] = df['rating'].apply(lambda x: 1 if x == 5 else 0)

    final_df = df[['cleaned_text', 'sentiment']]
    final_df.to_csv(output_file, index=False)
    
    print(f"[SUCCESS] Cleaned data saved to {output_file}")
    print(f"[INFO] Final usable dataset size: {len(final_df)} rows")

if __name__ == "__main__":
    process_data()
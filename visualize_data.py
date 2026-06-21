import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

def generate_clouds():
    input_file = "data/cleaned_reviews.csv"
    
    if not os.path.exists(input_file):
        print("[ERROR] Cleaned data missing. Run clean_data.py first.")
        return

    print("[INFO] Loading data and preparing clouds...")
    df = pd.read_csv(input_file)

    # Separate text by sentiment values
    positive_text = " ".join(df[df['sentiment'] == 1]['cleaned_text'])
    negative_text = " ".join(df[df['sentiment'] == 0]['cleaned_text'])

    # Initialize subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    # Positive word cloud generation
    print("[INFO] Generating Positive Cloud...")
    pos_cloud = WordCloud(width=800, height=800, 
                          background_color='white', 
                          colormap='Greens',
                          max_words=100).generate(positive_text)
    ax1.imshow(pos_cloud, interpolation='bilinear')
    ax1.set_title('5-STAR REVIEWS', fontsize=20, pad=20)
    ax1.axis('off')

    # Negative word cloud generation
    print("[INFO] Generating Negative Cloud...")
    neg_cloud = WordCloud(width=800, height=800, 
                          background_color='white', 
                          colormap='Reds',
                          max_words=100).generate(negative_text)
    ax2.imshow(neg_cloud, interpolation='bilinear')
    ax2.set_title('1-STAR REVIEWS', fontsize=20, pad=20)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig('data/sentiment_wordclouds.png')
    print("[SUCCESS] Word clouds saved to 'data/sentiment_wordclouds.png'")
    plt.show()

if __name__ == "__main__":
    generate_clouds()
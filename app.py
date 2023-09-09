import numpy as np
from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

# Load data from CSV
data = pd.read_csv('restaurants.csv')

# Dictionary to map categorical values to numerical labels
category_mapping = {
    'Cheap': 0,
    'Medium': 1,
    'Expensive': 2,
    'Aesthetic': 0,
    'Good': 1,
    'Normal': 2,
    'Both': 0,
    'Non-vegetarian': 1,
    'Vegetarian': 2,
    'Fast Food': 0,
    'Healthy': 1,
    'Moderate': 2
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = int(request.form['mood'])
        budget = int(request.form['budget'])
        aesthetics = int(request.form['aesthetics'])
        type = int(request.form['type'])
        diet = int(request.form['diet'])

        user_profile = np.array([budget, aesthetics, type, diet])

        content_similarities = cosine_similarity(user_profile.reshape(1, -1), data[['Budget', 'Aesthetics', 'Type', 'Diet']].applymap(lambda x: category_mapping[x]))

        collab_similarities = np.array([0.8, 0.6, 0.5, 0.7, 0.9])  # Similarity scores for collaborative filtering
        collab_similarities = collab_similarities.reshape((1, 5))  # Reshape collab_similarities to (1, 5)
        weights = np.array([0.7, 0.3])  # Adjust weights based on preference
        hybrid_scores = (content_similarities * weights[0]) + (collab_similarities * weights[1])

        ranked_restaurants = np.argsort(hybrid_scores[0])[::-1]
        top_recommended = ranked_restaurants[:3]

        recommended_restaurants = [data.iloc[idx]['Restaurant'] for idx in top_recommended]

        return render_template('index.html', recommendations=recommended_restaurants)

    return render_template('index.html', recommendations=[])

if __name__ == '__main__':
    app.run(debug=True)

import numpy as np
from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

# Load a larger dataset from CSV (Replace 'restaurants.csv' with your actual CSV file)
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
        try:
            mood = int(request.form['mood'])
            budget = int(request.form['budget'])
            aesthetics = int(request.form['aesthetics'])
            type = int(request.form['type'])
            diet = int(request.form['diet'])

            user_profile = np.array([budget, aesthetics, type, diet])

            # Map categorical values to numerical labels
            user_profile = np.array([category_mapping.get(category, 0) for category in user_profile])

            # Calculate cosine similarity
            content_similarities = cosine_similarity([user_profile], data[['Budget', 'Aesthetics', 'Type', 'Diet']].applymap(lambda x: category_mapping[x]))
            content_similarities = content_similarities.flatten()

            collab_similarities = np.random.rand(len(data))  # Random similarity scores for collaborative filtering

            weights = np.array([0.7, 0.3])  # Adjust weights based on preference
            hybrid_scores = (content_similarities * weights[0]) + (collab_similarities * weights[1])

            ranked_restaurants = np.argsort(hybrid_scores)[::-1]
            top_recommended = ranked_restaurants[:3]

            recommended_restaurants = [data.iloc[idx]['Restaurant'] for idx in top_recommended]

            return jsonify({"recommendations": recommended_restaurants})
        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template('index.html', recommendations=[])

if __name__ == '__main__':
    app.run(debug=True)

import numpy as np
from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from algo import recommend_restaurants
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            mood = int(request.form['mood'])
            budget = int(request.form['budget'])
            aesthetics = int(request.form['aesthetics'])
            type = int(request.form['type'])
            diet = int(request.form['diet'])
            return jsonify({recommend_restaurants(type,mood,budget,aesthetics,type,diet)})
        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template('index.html', recommendations=[])
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, send_from_directory
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from geopy.distance import geodesic
import warnings
from sklearn.exceptions import DataConversionWarning
import datetime

warnings.filterwarnings("ignore", category=DataConversionWarning)

app = Flask(__name__, static_folder='static')

def load_data(filename):
    return pd.read_csv(filename)

def filter_food_type(df, food_type):
    if food_type == 'Nonveg':
        return df[(df['Type'] == 'Both') | (df['Type'] == 'Non Veg')]
    return df[df['Type'] == 'Both' | (df['Type'] == 'Veg')]

def filter_mood(df, mood):
    if mood == 'Happy':
        mood_cuisines = ['American', 'Bakery', 'Continental', 'Chinese', 'Street Food', 'Arab', 'Italian']
    elif mood == 'Sad':
        mood_cuisines = ['Beverages', 'Chinese', 'Sweets', 'Bakery']
    elif mood == 'Unsure':
        return df
    
    return df[df['Cuisine'].isin(mood_cuisines)] if mood_cuisines else df

#to modify mood parameter
def filter_budget(df, budget):
    return df[df['Budget'] == budget]

def filter_diet(df, diet,time):
    if diet == 'Fast Food':
        if time == 'Morning':
            return df[(df['Diet'] == 'Healthy') & (df['Cuisine'] == 'American')]
        elif time == 'Afternoon':
            return df[(df['Cuisine'] == 'Continental') | (df['Cuisine'] == 'Arab')]
        elif time == 'Evening':
            return df[(df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'Street Food') | (df['Cuisine'] == 'American')]
        elif time == 'Night':
            return df[(df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'Continental')]
    elif diet == 'Healthy':
        if time == 'Morning':
            return df[df['Cuisine'] == 'Breakfast']
        elif time == 'Afternoon':
            return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'American')]
        elif time == 'Evening':
            return df[(df['Cuisine'] == 'American') | (df['Cuisine'] == 'Beverages')]
        elif time == 'Night':
            return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'Beverages')]
    elif diet == 'Moderate':
        if time == 'Morning':
            return df[(df['Cuisine'] == 'South Indian') & (df['Diet'] == 'Healthy')]
        elif time == 'Afternoon':
            return df[(df['Cuisine'].isin(['Arab', 'Continental', 'South Indian']))]
        elif time == 'Evening':
            return df[(df['Cuisine'].isin(['Chinese', 'Street Food', 'Bakery', 'Beverages', 'Sweets']))]
        elif time == 'Night':
            return df[(df['Cuisine'].isin(['North Indian', 'South Indian']))]
    return df # No diet filter

def filter_aesthetics(df, aes, k):
    k = min(k, len(df))
    df['Aesthetics'] = pd.to_numeric(df['Aesthetics'])
    aesthetic_data = df[['Aesthetics']]
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(aesthetic_data)
    indices = knn.kneighbors([[aes]])[1][0]  # Extract the first row of indices
    return df.iloc[indices]

def get_user_location(request):
    user_location = None
    if 'latitude' in request.form and 'longitude' in request.form:
        user_location = (float(request.form['latitude']), float(request.form['longitude']))
    return user_location

def calculate_distance_and_sort(df, user_location):
    if user_location:
        df['distance'] = df.apply(
            lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).kilometers, axis=1)
        return df[df['distance'] < 10].sort_values(by='distance')
    return df
def altdistance(df, user_location):
    if user_location:
        df['distance'] = df.apply(
            lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).kilometers, axis=1)
        return df[df['distance']].sort_values(by='distance')
    return df

def get_recommendations(filtered_df):
    recommendations = []
    for _, row in filtered_df.iterrows():
        restaurant_data = {
            "Restaurant": row['Restaurant'],
            "Rating": row['Rating'],
            "URL": row['url'],
            "ImageURL": row['pic'],
            "Address": row['address']
        }
        recommendations.append(restaurant_data)

    return recommendations[:3] if len(recommendations) > 3 else recommendations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            mood = request.form['mood']
            budget = request.form['budget']
            aes = int(request.form['aes'])
            food_type = request.form['foodtype']
            diet = request.form['diet']

            df = load_data('vizag.csv')
            print("CSV successfully loaded")
            user_location = get_user_location(request)
            print("Retrieved Users Location")
            filtered_df = calculate_distance_and_sort(df, user_location)
            print("Found nearest Restaurants")
            current_time = get_current_time()
            print("Retrieved current time")
            filtered_df = filter_diet(filtered_df, diet,current_time)
            print("Found correlation between diet and time")
            filtered_df = filter_mood(filtered_df, mood)
            print("Found correlation between mood and cuisine")
            filtered_df = filter_food_type(filtered_df, food_type)
            print("Found correlation between food type and cuisine")
            filtered_df = filter_budget(filtered_df, budget)
            print("Filtered data with budget")
            m=min(3,len(filtered_df))
            if (m==0):
                newdf=load_data('vizag.csv')
                filtered_df = altdistance(newdf, user_location)
                filtered_df = filter_diet(filtered_df, diet,current_time)
                filtered_df = filter_food_type(filtered_df, food_type)
                filtered_df = filter_budget(filtered_df, budget)
            m=min(3,len(filtered_df))
            filtered_df = filter_aesthetics(filtered_df, aes, k=m)
            print("Sorted with the desired aesthetics")



            return jsonify(get_recommendations(filtered_df))

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template('index.html', recommendations=[])

def get_current_time():
    current_time = datetime.datetime.now().time()
    if current_time < datetime.time(12, 0):
        return 'Morning'
    elif current_time < datetime.time(17, 0):
        return 'Afternoon'
    elif current_time < datetime.time(20, 0):
        return 'Evening'
    else:
        return 'Night'
@app.route('/morning', methods=['GET'])
def morning():
    return render_template('morning.html')
@app.route('/afternoon', methods=['GET'])
def afternoon():
    return render_template('afternoon.html')
@app.route('/evening', methods=['GET'])
def evening():
    return render_template('evening.html')
@app.route('/night', methods=['GET'])
def night():
    return render_template('night.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

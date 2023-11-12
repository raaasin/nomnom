from flask import Flask, render_template, request, jsonify, send_from_directory
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from geopy.distance import geodesic
import warnings
from sklearn.exceptions import DataConversionWarning
import datetime
from flask_cors import CORS


warnings.filterwarnings("ignore", category=DataConversionWarning)

app = Flask(__name__, static_folder='static')
app = Flask(__name__)
CORS(app)

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

def curr_time():
    #return what time it is, like morning, afternoon, evening, night
    now = datetime.datetime.now()
    if now.hour >= 6 and now.hour < 12:
        return "morning"
    elif now.hour >= 12 and now.hour < 16:
        return "afternoon"
    elif now.hour >= 16 and now.hour < 19:
        return "evening"
    else:
        return "night"
    
def magic(df,time,diet,mood):
    if time == 'morning':
        if diet == 'Fast Food':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'American') | (df['Diet'] == 'Healthy') | (df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'Breakfast')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'American') | (df['Cuisine'] == 'Beverages')]
            else:
                return df[(df['Cuisine'] == 'American') | (df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'South Indian')]
        elif diet == 'Healthy':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Breakfast') | (df['Diet'] == 'Healthy')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Breakfast') | (df['Cuisine'] == 'Beverages') | (df['Diet'] == 'Healthy')]
            else:
                return df[(df['Cuisine'] == 'American') | (df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'South Indian') | (df['Diet'] == 'Healthy')]
        elif diet == 'Moderate':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'Breakfast')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Breakfast') | (df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'North Indian')]
            else:
                return df[(df['Cuisine'] == 'Breakfast') | (df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'North Indian')]
    elif time == 'afternoon':
        if diet == 'Fast Food':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Continental') | (df['Cuisine'] == 'Arab') | (df['Cuisine'] == 'American')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Continental') | (df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'American')]
            else:
                return df[(df['Cuisine'] == 'Continental') | (df['Cuisine'] == 'Arab') | (df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'South Indian')]
        elif diet == 'Healthy':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'North Indian') | (df['Diet'] == 'Healthy')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'Beverages') | (df['Diet'] == 'Healthy')]
            else:
                return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'American') | (df['Diet'] == 'Healthy')]
        elif diet == 'Moderate':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Continental') | (df['Cuisine'] == 'Arab') | (df['Cuisine'] == 'South Indian')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'Arab') | (df['Cuisine'] == 'North Indian')]
            else:
                return df[(df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'North Indian')]
    elif time == 'evening':
        if diet == 'Fast Food':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'Street Food') | (df['Cuisine'] == 'American')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Street Food') | (df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'Bakery')]
            else:
                return df[(df['Cuisine'] == 'American') | (df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'South Indian')]
        elif diet == 'Healthy':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'North Indian') | (df['Diet'] == 'Healthy')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Bakery') | (df['Cuisine'] == 'Sweets') | (df['Cuisine'] == 'Beverages') | (df['Diet'] == 'Healthy')]
            else:
                return df[(df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'North Indian') | (df['Diet'] == 'Healthy')]
        elif diet == 'Moderate':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'Street Food') | (df['Cuisine'] == 'Bakery') | (df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'Sweets')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'Street Food') | (df['Cuisine'] == 'Bakery')]
            else:
                return df[(df['Cuisine'] == 'Chinese') | (df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'Bakery') | (df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'South Indian')]
    elif time == 'night':
        if diet == 'Fast Food':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'Continental')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'Bakery')]
            else:
                return df[(df['Cuisine'] == 'Italian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'Chinese')]
        elif diet == 'Healthy':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'American') | (df['Diet'] == 'Healthy') | (df['Cuisine'] == 'Beverages')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'American') | (df['Cuisine'] == 'Beverages') | (df['Cuisine'] == 'Breakfast') | (df['Diet'] == 'Healthy')]
            else:
                return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'Beverages') | (df['Diet'] == 'Healthy')]
        elif diet == 'Moderate':
            if mood == 'Happy':
                return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'Street Food') | (df['Cuisine'] == 'Chinese')]
            elif mood == 'Sad':
                return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'South Indian') | (df['Cuisine'] == 'Bakery') | (df['Cuisine'] == 'Sweets')]
            else:
                return df[(df['Cuisine'] == 'North Indian') | (df['Cuisine'] == 'South Indian')]
            
def location(data,newdf):
    try:
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        user_location = (latitude, longitude)
        newdf['distance'] = newdf.apply(lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).miles, axis=1)
        newdf = newdf.sort_values(by=['distance'])
        return newdf.head(10) # return the closest restaurant with the closest aesthetic value
    except:
        return newdf

def filter_aesthetics(df, aes, k):
    k = min(k, len(df))
    df['Aesthetics'] = pd.to_numeric(df['Aesthetics'])
    aesthetic_data = df[['Aesthetics']]
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(aesthetic_data)
    indices = knn.kneighbors([[aes]])[1][0]  # Extract the first row of indices
    return df.iloc[indices]

def algorithm(data):
    data=data

    #retrieval of time 
    time=curr_time()

    #retrieval of budget and filtering in procress
    budget=data['budget']
    df=pd.read_csv('vizag.csv')
    df=df[df['Budget'] == budget]

    #filtering of veg/nonveg
    diet=data['foodtype']
    if diet == 'Nonveg':
        df=df[(df['Type'] == 'Both') | (df['Type'] == 'Non Veg')]
    else:
        df=df[(df['Type'] == 'Both') | (df['Type'] == 'Veg')]

    #filtering using moood,time,diet
    mood=data['mood']
    diet=data['diet']
    newdf=magic(df,time,diet,mood)

    #sort by distance
    newdf = location(data, newdf)

    #sort by aesthetics
    aes = int(data['aes'])
    m=min(3,len(newdf))
    finaldf = filter_aesthetics(newdf, aes, k=m)

    print(finaldf.head())

    return jsonify(get_recommendations(finaldf))



@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        try:
            data= request.get_json()
            answer=algorithm(data)
            return answer 

        except Exception as e:
            return jsonify({"error": str(e)})

    print("not if")
    return jsonify({"get?": "yes"})

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

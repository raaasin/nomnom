from flask import Flask, render_template, request, jsonify,send_from_directory
from sklearn.neighbors import NearestNeighbors  
import pandas as pd
from geopy.distance import geodesic
import warnings
from sklearn.exceptions import DataConversionWarning
import datetime

warnings.filterwarnings("ignore", category=DataConversionWarning)


app = Flask(__name__,static_folder='static')
@app.route('/', methods=['GET', 'POST'])



def index():
    if request.method == 'POST':
        try:
            mood = (request.form['mood'])
            budget = (request.form['budget'])
            aes = int((request.form['aes']))
            type = (request.form['foodtype'])
            diet = (request.form['diet'])
        
        
            df = pd.read_csv('vizag.csv')

            print(type,mood,budget,aes,diet)

            #filtering veg/nonveg
            if type == 'Nonveg':
                filtered_df = df[(df['Type'] == 'Both') | (df['Type'] == 'Non Veg')]
            else:
                filtered_df = df[df['Type'] == 'Both']

            #filtering emotions
            # Get the current time
            current_time = datetime.datetime.now().time()

            # Convert the current time to a string in a format like "Morning," "Afternoon," "Evening," or "Night"
            if current_time < datetime.time(12, 0):
                time = 'Morning'
            elif current_time < datetime.time(17, 0):
                time = 'Afternoon'
            elif current_time < datetime.time(20, 0):
                time = 'Evening'
            else:
                time = 'Night'

            # Filtering emotions
            happy_cuisines = ['South Indian', 'North Indian', 'American', 'Italian', 'Continental']
            sad_cuisines = ['Beverages', 'Bakery', 'Street Food', 'Chinese', 'Arab']

            if mood == 'Happy':
                mood_cuisines = happy_cuisines
            elif mood == 'Sad':
                mood_cuisines = sad_cuisines
            else:
                mood_cuisines = []  # No mood-based filter

            # Time-based suggestions
            if time == 'Morning':
                time_cuisines = ['South Indian', 'Street Food']
            elif time == 'Afternoon':
                time_cuisines = ['South Indian', 'North Indian', 'Continental']
            elif time == 'Evening':
                time_cuisines = ['American', 'Italian', 'Chinese']
            elif time == 'Night':
                time_cuisines = ['North Indian']
            else:
                time_cuisines = []  # No time-based filter

            # Combine mood and time filters
            if mood_cuisines and time_cuisines:
                suggested_cuisines = list(set(mood_cuisines) or set(time_cuisines))
            elif mood_cuisines:
                suggested_cuisines = mood_cuisines
            elif time_cuisines:
                suggested_cuisines = time_cuisines
            else:
                suggested_cuisines = []  # No specific suggestions

            # Filter the DataFrame based on the suggested cuisines
            if suggested_cuisines:
                filtered_df = filtered_df[filtered_df['Cuisine'].isin(suggested_cuisines)]
            else:
                pass  # No filtering based on mood or time

                        

            filtered_df = filtered_df[filtered_df['Budget'] == budget]

            # filtering with diet
            if diet == 'Moderate':
                filtered_df = filtered_df[(filtered_df['Diet'] == 'Moderate') | (filtered_df['Diet'] == 'Healthy')]
            elif diet == 'Fast Food':
                filtered_df = filtered_df[filtered_df['Diet'] == 'Fast Food']
            else:
                filtered_df = filtered_df[filtered_df['Diet'] == 'Healthy']

            print("Doing aesthetic check")
            # Filter restaurants based on aesthetics
            k = min(5, len(filtered_df))
            filtered_df['Aesthetics'] = pd.to_numeric(filtered_df['Aesthetics'])
            aesthetic_data = filtered_df[['Aesthetics']]
            knn = NearestNeighbors(n_neighbors=k)
            knn.fit(aesthetic_data)
            indices = knn.kneighbors([[aes]])[1][0]  # Extract the first row of indices
            filtered_df = filtered_df.iloc[indices]
           
            print("aesthetic check done")

            user_location=None
            #print(filtered_df.head())
            if 'latitude' in request.form and 'longitude' in request.form:
                user_location = (float(request.form['latitude']), float(request.form['longitude']))
                print("user location recieved")
            if user_location:
                filtered_df['distance'] = filtered_df.apply(
                    lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).kilometers, axis=1)
                #print("location check done")
                #print(filtered_df.head())
                filtered_df= filtered_df.sort_values(by='distance')
                #print("after correction with location")
                #print(filtered_df.head())
            if type == 'Veg':
                if filtered_df[(filtered_df['Type'] == 'Veg')].empty:
                    filtered_df=filtered_df[(filtered_df['Type'] == 'Both')]
                else:
                    filtered_df=filtered_df[(filtered_df['Type'] == 'Veg')]     

            
            recommendations = []
            for _, row in filtered_df.iterrows():
                restaurant_data = {
                    "Restaurant": row['Restaurant'],
                    "Rating": row['Rating'],
                    "URL": row['url'],
                    "ImageURL": row['pic'],
                    "Address":row['address']

                }
                recommendations.append(restaurant_data)

            #print(recommendations)

            if len(recommendations)==0:
                return jsonify(None)
            if len(recommendations) > 3:
                return jsonify(recommendations[:3])
            else:
                return jsonify(recommendations)
            
        except:
            return jsonify({"something went wrong :/"})

    return render_template('index.html', recommendations=[])

@app.route('/Ads.txt')
def static_from_root():
 return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

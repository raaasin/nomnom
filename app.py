from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            mood = (request.form['mood'])
            budget = (request.form['budget'])
            aesthetics = (request.form['aesthetics'])
            type = (request.form['type'])
            diet = (request.form['diet'])
            df = pd.read_csv('vizag.csv')
            spicy_cuisines = ['Asian', 'Mexican', 'Indian']
            sweet_cuisines = ['Bakery', 'Cafe']
            print(type,mood,budget,aesthetics,diet)
            
            #filtering veg/nonveg
            if type == 'Nonveg':
                filtered_df = df[(df['Type'] == 'Both') | (df['Type'] == 'Non-vegetarian')]
            else:
                filtered_df = df[df['Type'] == 'Vegetarian']

            #filtering emotions

            if mood == 'Happy':
                mood_cuisines = spicy_cuisines
            elif mood == 'Sad':
                mood_cuisines = sweet_cuisines
            else:
                mood_cuisines = spicy_cuisines + sweet_cuisines
            
        
            filtered_df = filtered_df[filtered_df['Cuisine'].isin(mood_cuisines)]
            filtered_df = filtered_df[filtered_df['Budget'] == budget]

            #filtering with diet
            if diet == 'Moderate':
                filtered_df = filtered_df
            elif diet == 'Fast Food':
                filtered_df = filtered_df[filtered_df['Diet'] == 'Fast Food']
            else:
                filtered_df = filtered_df[filtered_df['Diet'] == 'Healthy']

            # Filter restaurants based on aesthetics
            if aesthetics == 'Normal':
                filtered_df = filtered_df
            elif aesthetics == 'Good':
                filtered_df = filtered_df[(filtered_df['Aesthetics'] == 'Normal') | (filtered_df['Aesthetics'] == 'Good')]
            else:
                filtered_df = filtered_df[filtered_df['Aesthetics'] == 'Aesthetic']

            #sort using rating
            #print(filtered_df.head())
            sorted_df = filtered_df.sample(frac=1, random_state=random.seed())
            sorted_df = sorted_df.reset_index(drop=True)

            recommendations = []
            for _, row in sorted_df.iterrows():
                restaurant_data = {
                    "Restaurant": row['Restaurant'],
                    "Rating": row['Rating'],
                    "URL": row['url'],
                    "ImageURL": row['pic']
                }
                recommendations.append(restaurant_data)

            print(recommendations)

            if len(recommendations)==0:
                return jsonify(None)
            if len(recommendations) > 3:
                return jsonify(recommendations[:3])
            else:
                return jsonify(recommendations)
            
        except:
            return jsonify({"something went wrong :/"})

            
            

            
            
            

    return render_template('index.html', recommendations=[])

if __name__ == '__main__':
    app.run(debug=True)

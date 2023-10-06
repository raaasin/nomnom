import pandas as pd

df = pd.read_csv('vizag.csv')
spicy_cuisines = ['Asian', 'Mexican', 'Indian']
sweet_cuisines = ['Bakery', 'Cafe']
def recommend_restaurants(dietary_preference, mood, budget, aesthetics, diet):
    # Filter restaurants based on dietary preference
    if dietary_preference == 'Nonveg':
        filtered_df = df[(df['Type'] == 'Both') | (df['Type'] == 'Non-vegetarian')]
    elif dietary_preference == 'Veg':
        filtered_df = df[df['Type'] == 'Vegetarian']
    else:
        return {"error": "Invalid dietary preference. Use 'Nonveg' or 'Veg'."}

    # Filter restaurants based on mood
    if mood == 'Happy':
        mood_cuisines = spicy_cuisines
    elif mood == 'Sad':
        mood_cuisines = sweet_cuisines
    elif mood == 'Unsure':
        # When unsure, recommend both spicy and sweet cuisines
        mood_cuisines = spicy_cuisines + sweet_cuisines
    else:
        return {"error": "Invalid mood. Use 'Happy', 'Sad', or 'Unsure'."}

    filtered_df = filtered_df[filtered_df['Cuisine'].isin(mood_cuisines)]

    # Filter restaurants based on budget
    filtered_df = filtered_df[filtered_df['Budget'] == budget]

    # Filter restaurants based on diet preference
    if diet == 'Moderate':
        filtered_df = filtered_df
    elif diet == 'Fast Food':
        filtered_df = filtered_df[filtered_df['Diet'] == 'Fast Food']
    elif diet == 'Healthy':
        filtered_df = filtered_df[filtered_df['Diet'] == 'Healthy']
    else:
        return {"error": "Invalid diet preference. Use 'Moderate', 'Fast Food', or 'Healthy'."}

    # Filter restaurants based on aesthetics
    if aesthetics == 'Normal':
        filtered_df = filtered_df
    elif aesthetics == 'Good':
        filtered_df = filtered_df[(filtered_df['Aesthetics'] == 'Normal') | (filtered_df['Aesthetics'] == 'Good')]
    elif aesthetics == 'Aesthetic':
        filtered_df = filtered_df[filtered_df['Aesthetics'] == 'Aesthetic']
    else:
        return {"error": "Invalid aesthetics preference. Use 'Normal', 'Good', or 'Aesthetic'."}

    # Sort restaurants by rating in descending order
    sorted_df = filtered_df.sort_values(by='Rating', ascending=False)

    # Extract and return top 3 rated restaurant details
    recommendations = []
    for _, row in sorted_df.iterrows():
        restaurant_data = {
            "Restaurant": row['Restaurant'],
            "Rating": row['Rating'],
            "URL": row['url'],
            "ImageURL": row['pic']
        }
        recommendations.append(restaurant_data)

    if len(recommendations) > 3:
        return recommendations[:3]
    else:
        return recommendations
    
params = {
    'dietary_preference': 'Veg', # 'Nonveg' or 'Veg'
    'mood': 'Unsure',  # 'Happy', 'Sad', or 'Unsure'
    'budget': 'Medium', # 'Cheap', 'Medium', or 'Expensive'
    'aesthetics': 'Good', # 'Normal', 'Good', or 'Aesthetic'
    'diet': 'Moderate'  # 'Moderate', 'Fast Food', or 'Healthy'
}
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

model = joblib.load("model/recommendation.joblib")

data = pd.read_csv("movies_music_recommendation_100.csv")

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        category = request.form.get("category")
        mood = request.form.get("mood")

        if not category or not mood:
            return render_template("index.html", 
                       recommendations=["Please select both Category and Mood!"],
                       selected_category=category, 
                       selected_mood=mood)

        filtered_data = data[(data['type'] == category) & (data['mood'] == mood)]
        
        if len(filtered_data) > 0:
            recommendations = filtered_data.sort_values(by=['rating', 'popularity'], ascending=False).head(5)
            recommendation_list = recommendations['title'].tolist()
            return render_template("index.html", 
                       recommendations=recommendation_list,
                       selected_category=category, 
                       selected_mood=mood)
        else:
            
            input_data = pd.DataFrame({
                "id": [0],
                "title": [""],
                "type": [category],
                "mood": [mood],
                "language": ["English"],
                "rating": [0.0],
                "popularity": [0]
            })
            
            
            input_data = input_data[["id", "title", "type", "mood", "language", "rating", "popularity"]]
            
            predicted_genre = model.predict(input_data)[0]
            
            
            filtered_data = data[(data['type'] == category) & (data['mood'] == predicted_mood)]
            
            if len(filtered_data) > 0:
                recommendations = filtered_data.sort_values(by=['rating', 'popularity'], ascending=False).head(5)
                recommendation_list = recommendations['title'].tolist()
            else:
                recommendation_list = ["Not Found"]
            
            return render_template("index.html", 
                               recommendations=recommendation_list,
                               selected_category=category, 
                               selected_mood=mood)

    except Exception as e:
        return render_template("index.html", 
                               recommendations=["Not Found"],
                               selected_category=None, 
                               selected_mood=None)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

# Load trained model and encoders
model = joblib.load("cricket_score_model.pkl")
model_features = joblib.load("model_features.pkl")
encoders = joblib.load("Labelencoder.pkl")

app = Flask(__name__)

@app.route('/index')
def home():
    return render_template("index.html")   # your HTML form

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        over_number = float(request.form['over_number'])
        runs = float(request.form['runs'])
        wickets = float(request.form['wickets'])
        runsLast5overs = float(request.form['runsLast5overs'])
        wicketsLast5overs = float(request.form['wicketsLast5overs'])

        # Encode categorical inputs
        batting_team_encoded = encoders['Batting Team'].transform([batting_team])[0]
        bowling_team_encoded = encoders['Bowling Team'].transform([bowling_team])[0]


        input_data = pd.DataFrame([[batting_team_encoded, bowling_team_encoded, over_number, runs, wickets,
                                    runsLast5overs,wicketsLast5overs]],
                                  columns=['Batting Team', 'Bowling Team', 'Over Number', 'Runs Scored till that over', 'Wickets Taken till that over',
                                           "Runs in Last 5 Overs","Wickets in Last 5 Overs"])

        print(model_features)
        input_data = input_data.reindex(columns=model_features, fill_value=0)

        # Prediction
        prediction = model.predict(input_data)[0]

        return render_template("result.html", prediction_text=f"Predicted Total Score: {round(prediction)}")

    except Exception as e:
        return render_template("result.html", prediction_text=f"⚠️ Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)

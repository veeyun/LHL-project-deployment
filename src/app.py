from flask import render_template, request, jsonify,Flask
import flask
import numpy as np
import traceback #allows you to send error to user
import pickle
import pandas as pd
import joblib

# App definition
app = Flask(__name__)

def calc_total_income(df):
    # display(df)
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    
    return df

def log_transform(df, columns):
    for col in columns:
        df[col] = np.log(df[col])
    
    return df

# importing models
regressor = joblib.load('../loan_pred_model.pkl')

#webpage

@app.route('/')
def welcome():
   return "Welcome! Use this Flask App for Loan Prediction"

@app.route('/predict', methods=['POST','GET'])
def predict():

   if flask.request.method == 'GET':
       return "Prediction page. Try using post with params to get specific prediction."

   if flask.request.method == 'POST':
       try:
           json_ = request.json # '_' since 'json' is a special word
           print(json_)
           query_ = pd.DataFrame(json_, index=[0])

           prediction = regressor.predict(query_)

           return jsonify({
               "prediction" : str(prediction)
           })

       except:
           return jsonify({
               "trace": traceback.format_exc()
               })



if __name__ == "__main__":
   app.run()
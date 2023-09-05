#!/usr/bin/env python
# coding: utf-8


from flask import Flask, request, render_template, flash, redirect
import pandas as pd
import pickle
import plotly.express as px
import plotly
import json


def append_rows(dict_new_responses):
    dataset = pd.read_csv("./Dataset/Processed Data.csv")
    df = pd.DataFrame({'Luddy or not?': dict_new_responses['q1'], 'luddy_department ': dict_new_responses['q2'],
                       'sense of belonging _1': dict_new_responses['q3'], 'sense of belonging _2': dict_new_responses['q4'],
                       'sense of belonging _3': dict_new_responses['q5'], 'sense of belonging _4': dict_new_responses['q6'],
                       'sense of belonging _5': dict_new_responses['q7'], 'sense of belonging _6': dict_new_responses['q8'],
                       'sense of belonging _7': dict_new_responses['q9'], 'sense of belonging _8': dict_new_responses['q10'],
                       'sense of belonging _9': dict_new_responses['q11'], 'sense of belonging _10': dict_new_responses['q12'],
                       'sense of belonging _11': dict_new_responses['q13'], 'sense of belonging _12': dict_new_responses['q14'], 
                       'sense of belonging _13': dict_new_responses['q15'], 'sense of belonging _14': dict_new_responses['q16'], 
                       'sense of belonging _15': dict_new_responses['q17'], 'sense of belonging _16': dict_new_responses['q18'],
                       'Q19': dict_new_responses['q19'], 'Q12': dict_new_responses['q20'], 'Q13': dict_new_responses['q21'], 
                       'Q15': dict_new_responses['q22'], 'Q16': dict_new_responses['q23'], 'Q17': dict_new_responses['q24'], 
                       'Q14': dict_new_responses['q25'], 'Q10': dict_new_responses['q26'], 'Q11': dict_new_responses['q27'],
                       'Q12.1': dict_new_responses['q28']}, index = [0])
    dataset = pd.concat([dataset, df], ignore_index = True)
    dataset.to_csv('./Dataset/Processed Data.csv', index = False)
    return dataset



def one_hot_encoder(df, col):
    one_hot_df = pd.get_dummies(df[col])
    one_hot_df.columns = [col + '_' + column for column in one_hot_df.columns]
    df = pd.concat([df, one_hot_df], axis = 1)
    return df


def make_prediction(responses):
    df = pd.DataFrame({'Luddy or not?': responses['q1'], 'luddy_department ': responses['q2'],
                       'sense of belonging _1': responses['q3'], 'sense of belonging _2': responses['q4'],
                       'sense of belonging _3': responses['q5'], 'sense of belonging _4': responses['q6'], 
                       'sense of belonging _5': responses['q7'], 'sense of belonging _6': responses['q8'], 
                       'sense of belonging _7': responses['q9'], 'sense of belonging _8': responses['q10'], 
                       'sense of belonging _9': responses['q11'], 'sense of belonging _10': responses['q12'], 
                       'sense of belonging _11': responses['q13'], 'sense of belonging _12': responses['q14'], 
                       'sense of belonging _13': responses['q15'], 'sense of belonging _15': responses['q16'], 
                       'sense of belonging _16': responses['q17'], 'Q19': responses['q18'], 'Q12': responses['q19'], 
                       'Q13': responses['q20'], 'Q15': responses['q21'], 'Q16': responses['q22'], 
                       'Q17': responses['q23'], 'Q14': responses['q24'], 'Q10': responses['q25'], 
                       'Q11': responses['q26'], 'Q12.1': responses['q27']}, index = [0])
    
    response_mapping = {'Strongly Disagree': 1, 'Somewhat disagree': 2, 'Neither agree nor disagree': 3, 
                'Somewhat agree': 4, 'Strongly agree': 5}

    binary_mapping = {'Yes': 1, 'No': 0}

    sob_cols = ['sense of belonging _' + str(i) for i in range(1, 17)]
    sob_cols.remove('sense of belonging _14')
    for sob_col in sob_cols:
        df[sob_col] = df[sob_col].map(lambda x: response_mapping[x])

    binary_cols = ['Luddy or not?', 'Q12', 'Q12.1', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17']
    for binary_col in binary_cols:
        df[binary_col] = df[binary_col].map(lambda x: binary_mapping[x])
        
    columns_to_one_hot_encode = ['luddy_department ', 'Q19', 'Q10', 'Q11']
    for column in columns_to_one_hot_encode:
        df = one_hot_encoder(df, column)
        
    df = df.drop(columns_to_one_hot_encode, axis = 1)
    
    zero_df = pd.DataFrame({'Luddy or not?': 0, 'sense of belonging _1': 0, 'sense of belonging _2': 0,
       'sense of belonging _3': 0, 'sense of belonging _4': 0,
       'sense of belonging _5': 0, 'sense of belonging _6': 0,
       'sense of belonging _7': 0, 'sense of belonging _8': 0,
       'sense of belonging _9': 0, 'sense of belonging _10':0,
       'sense of belonging _11': 0, 'sense of belonging _12': 0,
       'sense of belonging _13': 0, 'sense of belonging _15': 0, 'sense of belonging _16': 0, 
       'Q12': 0, 'Q13': 0, 'Q15': 0, 'Q16': 0, 'Q17': 0, 'Q14': 0, 'Q12.1': 0, 
       'luddy_department _Computer Science': 0, 'luddy_department _Data Science': 0, 
       'luddy_department _Informatics': 0, 'luddy_department _Not from luddy': 0, 'luddy_department _Other': 0,
       'Q19_four years': 0, 'Q19_more than four years': 0,
       'Q19_this is my first year': 0, 'Q19_three years': 0, 'Q19_two years': 0,
       'Q10_Female': 0, 'Q10_Male': 0, 'Q10_Non-binary / third gender': 0,
       'Q10_Prefer not to say': 0, 'Q11_Asian': 0, 'Q11_Black or African American': 0,
       'Q11_Other': 0, 'Q11_Prefer not to say': 0, 'Q11_White or Caucasian': 0}, index = [0])
    
    col_not_in_response = list(set(zero_df.columns).difference(df.columns))
    zero_df = zero_df.loc[:, col_not_in_response]
    
    df = pd.concat([df, zero_df], axis = 1)
    
    df = df[['Luddy or not?', 'sense of belonging _1', 'sense of belonging _2',
       'sense of belonging _3', 'sense of belonging _4',
       'sense of belonging _5', 'sense of belonging _6',
       'sense of belonging _7', 'sense of belonging _8',
       'sense of belonging _9', 'sense of belonging _10',
       'sense of belonging _11', 'sense of belonging _12',
       'sense of belonging _13',
       'sense of belonging _15', 'sense of belonging _16', 'Q12', 'Q13', 'Q15',
       'Q16', 'Q17', 'Q14', 'Q12.1', 'luddy_department _Computer Science',
       'luddy_department _Data Science', 'luddy_department _Informatics',
       'luddy_department _Not from luddy', 'luddy_department _Other',
       'Q19_four years', 'Q19_more than four years',
       'Q19_this is my first year', 'Q19_three years', 'Q19_two years',
       'Q10_Female', 'Q10_Male', 'Q10_Non-binary / third gender',
       'Q10_Prefer not to say', 'Q11_Asian', 'Q11_Black or African American',
       'Q11_Other', 'Q11_Prefer not to say', 'Q11_White or Caucasian']]
    
    
    pickled_model = pickle.load(open('./model/logistic_regression.pkl', 'rb'))
    X = df.iloc[0, :].values.reshape(1, -1)

    return pickled_model.predict(X)[0]


def create_app(test_config = None):

    app = Flask(__name__)
    app.secret_key = '12345'
    @app.route('/')
    def first_page():
        return render_template('index.html')

    @app.route('/form_page', methods = ['GET', 'POST'])
    def form_page():
        if request.method == "POST":

            num_rows = int(request.form.get('q1'))
            offset = int(request.form.get('q2'))
            columns = request.form.getlist('q3')
            df = pd.read_csv('./Dataset/Processed Data.csv')
            
            if offset > df.shape[0]:
                return f'Data has only {df.shape[0]} rows'
            
            elif num_rows + offset > df.shape[0]:
                data = df.loc[offset:df.shape[0], columns]
                data = data.reset_index()
                return render_template("data.html", column_names=data.columns.values, row_data=list(data.values.tolist()), 
                                zip = zip)
            elif num_rows + offset <= df.shape[0]:
                data = df.loc[offset: num_rows+offset - 1, columns]
                data = data.reset_index()
                return render_template("data.html", column_names=data.columns.values, row_data=list(data.values.tolist()), 
                                zip = zip)
        else:
            return render_template('form_page.html')

    @app.route('/predict', methods=['GET', 'POST'])
    def predict():
        
        # If a form is submitted
        if request.method == "POST":
            
            # Get values through input bars
            q1 = request.form.get("q1")
            q2 = request.form.get("q2")
            q3 = request.form.get("q3")
            q4 = request.form.get("q4")
            q5 = request.form.get("q5")
            q6 = request.form.get("q6")
            q7 = request.form.get("q7")
            q8 = request.form.get("q8")
            q9 = request.form.get("q9")
            q10 = request.form.get("q10")
            q11 = request.form.get("q11")
            q12 = request.form.get("q12")
            q13 = request.form.get("q13")
            q14 = request.form.get("q14")
            q15 = request.form.get("q15")
            q16 = request.form.get("q16")
            q17 = request.form.get("q17")
            q18 = request.form.get("q18")
            q19 = request.form.get("q19")
            q20 = request.form.get("q20")
            q21 = request.form.get("q21")
            q22 = request.form.get("q22")
            q23 = request.form.get("q23")
            q24 = request.form.get("q24")
            q25 = request.form.get("q25")
            q26 = request.form.get("q26")
            q27 = request.form.get("q27")
            
            dict_responses = {}
            for i in range(1, 28):
                expr = 'q' + str(i)
                dict_responses['q'+str(i)] = eval(expr)
            
            
            # Get prediction
            prediction = make_prediction(dict_responses)
            if prediction == 0:
                prediction = 'Based on the responses, the student is not proud to be a part of Luddy School'
                imp_df = pd.read_json('./Dataset/importance.json')
                fig = px.bar(imp_df, x='Features', y='Coefficients', height = 800, width = 1500, 
                            barmode='group')
                fig.update_xaxes(title='Features', visible=True, showticklabels=False)
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("failure_prediction.html", output = prediction, graphJSON = graphJSON)
            else:
                prediction = 'Based on the responses, the student is proud to be a part of Luddy School'
                imp_df = pd.read_json('./Dataset/importance.json')
                fig = px.bar(imp_df, x='Features', y='Coefficients', height = 800, width = 1500, 
                            barmode='group')
                fig.update_xaxes(title='Features', visible=True, showticklabels=False)
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("success_prediction.html", output = prediction, graphJSON = graphJSON)
            
        else:
            prediction = ""
            
            return render_template("predict.html")

    @app.route('/add_data', methods=['GET', 'POST'])
    def add_data():
        
        if request.method == 'POST':
            data = request.form
            q1 = data["q1"]
            q2 = data["q2"]
            q3 = data["q3"]
            q4 = data["q4"]
            q5 = data["q5"]
            q6 = data["q6"]
            q7 = data["q7"]
            q8 = data["q8"]
            q9 = data["q9"]
            q10 = data["q10"]
            q11 = data["q11"]
            q12 = data["q12"]
            q13 = data["q13"]
            q14 = data["q14"]
            q15 = data["q15"]
            q16 = data["q16"]
            q17 = data["q17"]
            q18 = data["q18"]
            q19 = data["q19"]
            q20 = data["q20"]
            q21 = data["q21"]
            q22 = data["q22"]
            q23 = data["q23"]
            q24 = data["q24"]
            q25 = data["q25"]
            q26 = data["q26"]
            q27 = data["q27"]
            q28 = data["q28"]

            dict_responses_new = {}
            for i in range(1, 29):
                expr = 'q' + str(i)
                dict_responses_new['q'+str(i)] = eval(expr)

            dataset = append_rows(dict_responses_new)
            return render_template('success.html')
            
        else:
            shape = ''
            return render_template("add_data.html", output = shape)
    
    return app







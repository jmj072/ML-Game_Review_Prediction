import os
from flask import Flask, render_template, request
import pandas as pd
#library(remotes) remotes::install_version("xgboost", "0.90")
import pickle

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api',methods=['GET','POST'])
def input ():
    return render_template('API.html')


@app.route('/api/prediction',methods=['GET','POST'])
def predict ():
    directort_path = os.path.dirname(os.path.realpath(__file__))
    file_name = 'model.pkl'
    model_path = os.path.join(directort_path, file_name)
    model = pickle.load(open(model_path,'rb'))
    f_names = model.get_booster().feature_names

    data1 = request.form['genre']
    data1 = int(data1)

    data2 = request.form['Korean']
    data2 = int(data2)

    data3 = request.form['indie']
    data3 = int(data3)

    data4 = request.form['discount']
    data4 = int(data4)

    data5 = request.form['price_group']
    data5 = int(data5)

    values  = [[data1,data2,data3,data4,data5]]
    df_values = pd.DataFrame(values, columns = f_names)
    result = model.predict(df_values)
    # features = ['genre', 'Korean', 'indie', 'discount', 'price_group']
    return render_template('prediction.html', data=result)


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

# @app.route('/aboutme')
# def introduce():
#     return "Hellow! My name is Minjin"
if __name__ == "__main__":
    app.run(debug=True)

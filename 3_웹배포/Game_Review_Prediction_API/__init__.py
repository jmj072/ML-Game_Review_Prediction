import os
from flask import Flask, render_template, request
import joblib
import numpy as np
import pickle
import xgboost
import lightgbm
import sklearn


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'), 200
    
@app.route('/api',methods=['GET','POST'])
def input ():
    return render_template('API.html'), 200


@app.route('/api/prediction',methods=['GET','POST'])
def predict ():
    directort_path = os.path.dirname(os.path.realpath(__file__))
    file_name = 'model.pickle'
    model_path = os.path.join(directort_path, file_name)
    model = pickle.load(open(model_path,'rb'))
    # model = joblib.load(model_path)
    #print(model.set_params)
    #f_names = model.get_booster().feature_names
    data1 = request.form['Genre']
    data1 = int(data1)
    data2 = request.form['Indie']
    data2 = int(data2)
    data3 = request.form['Multiplayer']
    data3 = int(data3)
    data4 = request.form['Co-op']
    data4 = int(data4)
    data5 = request.form['OpenWorld']
    data5 = int(data5)
    data6 = request.form['Horror']
    data6 = int(data6)
    data7 = request.form['Violent']
    data7 = int(data7)
    data8 = request.form['Sexual']
    data8 = int(data8)
    data9 = request.form['Korean']
    data9 = int(data9)
    data10 = request.form['discount']
    data10 = int(data10)
    data11 = request.form['Num_Language']
    data11 = int(data11)
    data12 = request.form['price_group']
    data12 = int(data12)
    values  = np.array([[data1,data2,data3,data4,data5,data6,
                data7,data8,data9,data10,data11,data12]])
    pred = model.predict(values)
    prob = round(model.predict_proba(values).max()*100)
    # features = ['Genre', 'Indie', 'Multiplayer', 'Co-op', 'OpenWorld', 'Horror', 'Violent', 'Sexual',
    # 'Korean', 'discount', 'Num_Language', 'price_group']
    return render_template('prediction.html', predict=pred, probaility=prob), 200

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html'), 200

#return app
if __name__ == "__main__":
    app.run(debug=True)

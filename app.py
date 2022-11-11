from flask import Flask, render_template, request ,url_for
import joblib
import numpy as np
import json


app = Flask(__name__)

__locations = None
__data_columns1 = None
__data_columns2 = None
model = joblib.load(open('apartmentunitpriceprediction.joblib','rb'))

f = open('columns1.json')
__data_columns1 = json.loads(f.read())['data_columns1']
__locations = __data_columns1[:]

f = open('columns2.json')
__data_columns2 = json.loads(f.read())['data_columns2']

def get_estimated_price(input_json):
    try:
        loc_index = __data_columns1.index(input_json['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns2))
    x[0] = input_json['Bedrooms']
    x[1] = input_json['sqft(Floor_Area)']
    x[2] = input_json['Attached_Bathrooms']
    x[3] = input_json['Balcony']
    x[4] = input_json['Pantry_and_Kitechen']
    x[5] = input_json['Living_area_Launch']
    x[6] = input_json['Made_s_room']
    x[7] = input_json['Washing_Room']
    x[8] = input_json['Store_Room']
    x[9] = input_json['A_C']
    x[10] = input_json['TwentyFour_hours_Security']
    x[11] = input_json['Swimming_pool']
    x[12] = input_json['Gym']
    x[13] = input_json['Roof_Terrace']
    x[14] = input_json['Car_parkings']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(model.predict([x])[0],14)
    return result

    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@app.route('/predict',methods=['GET','POST'])
def predict():

    if request.method == 'POST':
        input_json = {
            "location": request.form['location'],
            "Bedrooms": request.form['bedrooms'],
            "sqft(Floor_Area)": request.form['floor_area'],
            "Attached_Bathrooms": request.form['bathrooms'],
            "Balcony": request.form['balcony'],
            "Pantry_and_Kitechen": request.form['kitchen'],
            "Living_area_Launch": request.form['launch'],
            "Made_s_room": request.form['made_s'],
            "Washing_Room": request.form['washing'],
            "Store_Room": request.form['store'],
            "A_C": request.form['ac'],
            "TwentyFour_hours_Security": request.form['security'],
            "Swimming_pool": request.form['pool'],
            "Gym": request.form['gym'],
            "Roof_Terrace": request.form['roof'],
            "Car_parkings": request.form['car']
        }
        result1 = get_estimated_price(input_json)

        result = '%.2f' % result1


    return render_template('predict.html',result=result)


if __name__=='__main__':
    app.run(debug=True,port=5000)
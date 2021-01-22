from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()
from src.utils import *
import requests
import shutil

from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
PREDICTION_KEY = os.getenv("PREDICTION_KEY")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():
    open_waste_slot()
    waste = take_trash_picture()
    trash = os.path.join("./static/images", "test.jpg")
    shutil.copyfile(waste, trash)

    return render_template('insert.html')


@app.route('/waste/pick-type', methods=['POST'])    
def pick_type():

    if request.method == 'POST':  

        url = ENDPOINT
        headers = {
            'Prediction-Key': PREDICTION_KEY,
            'Content-Type': 'application/octet-stream'
        }

        with open(app.root_path + "/static/images/test.jpg", "rb") as image_contents:
            r = requests.post(url, headers=headers, data=image_contents.read())
            r_json = r.json()
            data = r_json['predictions']
            tagname = data[0]['tagName']
            result = "\t\t\n" + data[0]['tagName'] + " : {0:.2f}% ".format(data[0]['probability'] * 100)
    
    close_waste_slot()

    return render_template('type.html', tagname=tagname, result=result)


@app.route('/confirmation', methods=['POST'])
def confirmation():
    waste_type = request.form['type']

    process_waste(waste_type)
    return render_template('confirmation.html')


if __name__ == "__main__":
    app.run(debug=True)

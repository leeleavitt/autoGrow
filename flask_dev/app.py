from flask import Flask, render_template, request, jsonify
import json
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post_python_data_to_web', methods = ['GET', 'POST'])
def get_python_data_send():
    file = json.load(open('SETTINGS.json'))
    return json.dumps(file)

@app.route('/post_python_data_from_sever', methods = ['GET', 'POST'])
def post_python_data_collect():
    
    file = json.load(open('SETTINGS.json'))
    key, value = list(request.get_json().items())[0]
    file[key] = value
    
    with open('SETTINGS.json', 'w') as file_out:
        json.dump(file, file_out)

    return ('', 204)

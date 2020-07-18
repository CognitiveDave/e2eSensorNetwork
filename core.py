import flask
from flask import Flask, request, jsonify, render_template
from dbClass import DBHelper as DB
from redisDB import RedisHelper
from weather import Weather
from flask_cors import CORS

app = Flask(__name__)


CORS(app, resources={r'/*': {'origins': '*'}})

app.config['DEBUG'] = True
import json
import pandas as pd
from datetime import date
today = str(date.today())


@app.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404

#@app.route('/app')
@app.route('/app', defaults={'path': ''})
@app.route('/<path:path>')
#@requires_auth
def catch_all(path):
    return render_template("index.html")


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/api/v1/resources/hosts', methods=['GET'])
def api_all():
    dbr = RedisHelper()
    return jsonify(dbr.devices_read())

@app.route('/api/v1/resources/sensors', methods=['GET'])
def api_id():
    db = DB()
    return jsonify(db.day_summary())

@app.route('/api/v1/resources/current', methods=['GET'])
def api_cur():
    dbR = RedisHelper()
    current = dbR.read()
    return jsonify(current)

@app.route('/api/v1/resources/weather', methods=['GET'])
def api_weath():
    wR = Weather()
    current = wR.get_weather()
    return jsonify(current)

@app.route('/api/v1/resources/messages', methods=['GET'])
def api_msg():
    dbR = RedisHelper()
    current, msgC = dbR.messages()
    return jsonify(current)

if __name__ == "__main__": 
    app.run(port=5000)


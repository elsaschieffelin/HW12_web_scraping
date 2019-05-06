#imports
from flask_pymongo import PyMongo
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect
import mars

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index(): 
    mission = mongo.db.mission.find_one()
    return render_template('index.html', mission=mission)

@app.route('/scrape')
def scraper(): 
    mission = mongo.db.mission
    mars_data= mars.scrape()
    mongo.db.mission.update({}, mars_data, upsert=True)
    return redirect ('/', code = 302)


if __name__ == "__main__":
    app.run(debug=True)
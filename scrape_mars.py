#imports
from flask_pymongo import PyMongo
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect
import mission_to_mars

app = Flask(__name__)
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

@app.route('/')

@app.route('/scrape')
def scrape(): 
    mars_data= mission_to_mars.scrape_info()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect ('/', code = 302)
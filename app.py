from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
import scrape_mars
from pprint import pprint
import pymongo 

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/scrape_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars = mongo.db.mars_data.find_one()
    # Return template and data
    pprint(mars)
    return render_template("index.html", mars_data=mars)



# Route that will trigger the scrape function
@app.route("/scrape")

def runscrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['scrape_db']
    collection = mydb['mars_data']
    collection.update({}, mars_data, upsert=True)
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)
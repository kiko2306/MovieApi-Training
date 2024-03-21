from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# this stands for cross origin request
# allow us to send a request to this backend from a different url
from flask_cors import CORS

# initialize the aplication
app=Flask(__name__)
# wrap our app in cors
CORS(app)

# specifying the location of the local SQL
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydatabase.db"
# we're not going to track all the modifications we
# make to the database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# create a database instance which gives us access to the database
db=SQLAlchemy(app)

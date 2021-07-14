# Importing
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Loading the database

password = os.environ["mongopassword"] # getting 'mognopassword' from the .env file
mongo_url = "mongodb+srv://pw1924:" + password + "@appdb.ao3yl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" # The DB URL.
cluster = MongoClient(mongo_url) # Connecting to the cluster
db = cluster["PRC"] # Getting the 'PRC' database

# Collections

punishments = db["punishments"] # Where all the punishments are stored
settings = db["settings"] # Where the settings set are stored.

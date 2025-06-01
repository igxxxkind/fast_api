from pymongo import MongoClient

client = MongoClient()

database=client.mydatabase # create a database called mydatabase

# collections are equivalent to tables in SQL databases

user_collection = database["users"] # to reference a users collection in MOngoDB

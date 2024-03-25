###########
# Imports #
###########
# Used features
import pymongo
# Used errors
from pymongo.errors import ConnectionFailure

############
# DB setup #
############
# Client setup
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Test online
try:
    client.admin.command('ismaster')
except ConnectionFailure:
    print("Server not available")

# Get DB
database = client.get_database("database")

#########
# Tests #
#########
expenses = database.get_collection("expenses")
expenses.drop()
expenses = database.get_collection("expenses")

for x in range(0, 10):
    testExp = {"desc": "Test expense" + str(x), "value": (100 + x)}
    x = expenses.insert_one(testExp)
    print(x.inserted_id)

query = {"value": 101}
for x in expenses.find(query):
    print(x)
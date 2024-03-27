import json
from bson.json_util import dumps
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from expenses_manager.objects.expense import Expense
from expenses_manager.objects.income import Income


############
# DB setup #
############
def setup():
    # Client setup
    client = MongoClient("mongodb://localhost:27017/")

    # Test online
    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server not available")

    # Initialize DB
    database = client.get_database("database")
    expenses = database.get_collection("expenses")
    #expenses.drop()
    income = database.get_collection("income")
    #income.drop()

    return expenses, income


#############
# Edit data #
#############
def insertExpense(middleware, desc, amount, ts):
    newExp = Expense(desc, amount, ts)
    middleware.expenses.insert_one(newExp.to_dict())


def insertIncome(middleware, desc, amount, ts):
    newInc = Income(desc, amount, ts)
    middleware.income.insert_one(newInc.to_dict())


##################
# Access to data #
##################
def retrieveExpenses(middleware):
    return middleware.expenses.find({})


def retrieveIncomes(middleware):
    return middleware.income.find({})


def dumpDB(middleware):
    toDump = [middleware.expenses.find({}), middleware.income.find({})]
    with open('../dumps/expenses - ' + datetime.now().strftime("%Y-%m-%d-%H%M%S") + '.json', 'w') as file:
        json.dump(json.loads(dumps(toDump[0])), file)
    with open('../dumps/incomes - ' + datetime.now().strftime("%Y-%m-%d-%H%M%S") + '.json', 'w') as file:
        json.dump(json.loads(dumps(toDump[1])), file)

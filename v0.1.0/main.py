###########
# Imports #
###########
# Used features
from datetime import datetime
from pprint import pprint
from pymongo import MongoClient
from bson.json_util import dumps
import json
# Used errors
from pymongo.errors import ConnectionFailure

# Used objects
from expenses_manager.objects.expense import Expense


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
    expenses.drop()
    income = database.get_collection("income")
    income.drop()

    return expenses, income


# Main loop
def main(expenses, income):
    while True:
        print("----------------------------------------------------------")
        print("| 1: Register new expense                                |")
        print("| 2: Register new income                                 |")
        print("| 3: Get inserted expenses                               |")
        print("| 4: Get inserted incomes                                |")
        print("| 5: Dump JSON (visible when the application is closed)  |")
        print("| 6: Exit                                                |")
        print("----------------------------------------------------------")
        command = int(input("> "))
        match command:
            case 1:
                desc = input("Enter a description: ")
                amount = int(input("Enter an amount: "))
                ts = datetime.now()
                newExp = Expense(desc, amount, ts)
                expenses.insert_one(newExp.to_dict())
            case 2:
                desc = input("Enter a description: ")
                amount = int(input("Enter an amount: "))
                ts = datetime.now()
                newInc = Expense(desc, amount, ts)
                income.insert_one(newInc.to_dict())
            case 3:
                allExp = expenses.find({})
                for x in allExp:
                    pprint(x)
            case 4:
                allInc = income.find({})
                for x in allInc:
                    pprint(x)
            case 5:
                toDump = [expenses.find({}), income.find({})]
                with open('dumps/expenses - ' + datetime.now().strftime("%Y-%m-%d-%H%M%S") + '.json', 'w') as file:
                    json.dump(json.loads(dumps(toDump[0])), file)
                with open('dumps/income - ' + datetime.now().strftime("%Y-%mm-%d-%H%M%S") + '.json', 'w') as file:
                    json.dump(json.loads(dumps(toDump[1])), file)
            case 6:
                return

# Startup
if __name__ == "__main__":
    (exp, inc) = setup()
    main(inc, exp)

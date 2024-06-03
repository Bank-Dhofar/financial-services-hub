from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['bank']

user_data = [
    {'name': 'Alice', 'account_number': '123456789', 'balance': 1000},
    {'name': 'Bob', 'account_number': '987654321', 'balance': 2500},
    {'name': 'Charlie', 'account_number': '555555555', 'balance': 500},
    {'name': 'David', 'account_number': '777777777', 'balance': 1500}
]

def create_user(name, account_number, balance):
    user = {
        'name': name,
        'account_number': account_number,
        'balance': balance
    }
    db.users.insert_one(user)
    
for data in user_data:
    create_user(data['name'], data['account_number'], data['balance'])

def find_user(account_number):
    return db.users.find_one({'account_number': account_number})

def update_balance(account_number, new_balance):
    db.users.update_one({'account_number': account_number}, {'$set': {'balance': new_balance}})

def delete_user(account_number):
    db.users.delete_one({'account_number': account_number})
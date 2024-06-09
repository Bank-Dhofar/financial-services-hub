from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['bank']

# Drop the users collection if it exists
db.users.drop()

user_data = [
    {'name': 'Alice', 'account_number': '1', 'balance': 1000},
    {'name': 'Bob', 'account_number': '2', 'balance': 2500},
    {'name': 'Charlie', 'account_number': '3', 'balance': 500},
    {'name': 'David', 'account_number': '4', 'balance': 1500}
]

def create_user(name, account_number, balance):
    user = {
        'name': name,
        'account_number': account_number,
        'balance': balance,
        'transactions': []
    }
    db.users.insert_one(user)

for data in user_data:
    create_user(data['name'], data['account_number'], data['balance'])

# Function to add a transaction for a user
def add_transaction(account_number, transaction_type, amount):
    transaction = {
        'type': transaction_type,
        'amount': amount,
        'timestamp': datetime.utcnow()
    }
    db.users.update_one(
        {'account_number': account_number},
        {'$push': {'transactions': transaction}}
    )

# Example usage of adding transactions
add_transaction('1', 'deposit', 500)
add_transaction('2', 'withdrawal', 300)
add_transaction('3', 'deposit', 200)
add_transaction('4', 'withdrawal', 100)

# Query to find duplicate entries based on the account_number field
duplicate_accounts = db.users.aggregate([
    {"$group": {"_id": "$name", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
])

# Iterate over duplicate account numbers and remove duplicate entries
for account in duplicate_accounts:
    duplicate_entries = list(db.users.find({"name": account["_id"]}))
    for entry in duplicate_entries[1:]:
        db.users.delete_one({"_id": entry["_id"]})
        print(f"Deleted duplicate entry with _id: {entry['_id']}")

# Find and delete accounts with null name value
null_name_accounts = db.users.find({"name": {"$exists": False}})
for account in null_name_accounts:
    db.users.delete_one({"_id": account["_id"]})
    print(f"Deleted account with _id: {account['_id']}")

print("Duplicates removed successfully.")

def find_user(account_number):
    try:
        user = db.users.find_one({'account_number': account_number})
        if user:
            return user
        else:
            print("User not found.")
            return None
    except Exception as e:
        print(f"Error finding user: {e}")
        return None

def retrieve_user_info(account_number):
    try:
        user_info = db.users.find_one({'account_number': account_number})
        return user_info
    except Exception as e:
        print(f"Error retrieving user information: {e}")
        return None

def update_balance(account_number, new_balance):
    db.users.update_one({'account_number': account_number}, {'$set': {'balance': new_balance}})
    add_transaction(account_number, 'balance update', new_balance)

def delete_user(account_number):
    db.users.delete_one({'account_number': account_number})

# Example usage of the functions
update_balance('1', 1200)
delete_user('3')

# Print all users to verify
for user in db.users.find():
    print(user)

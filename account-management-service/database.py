from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['bank']

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
        'balance': balance
    }
    db.users.insert_one(user)
    
for data in user_data:
    create_user(data['name'], data['account_number'], data['balance'])
    
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


def update_balance(account_number, new_balance):
    db.users.update_one({'account_number': account_number}, {'$set': {'balance': new_balance}})

def delete_user(account_number):
    db.users.delete_one({'account_number': account_number})
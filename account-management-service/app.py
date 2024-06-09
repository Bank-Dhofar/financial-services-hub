from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
import os
import random
import logging
import requests
import traceback
from bson import ObjectId
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/bank')
print("MongoDB URI:", mongo_uri)
client = MongoClient(mongo_uri)
db = client.get_database()

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_account_number():
    return str(random.randint(100000, 999999))

@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user details from the request
        data = request.get_json()
        name = data.get('name')
        balance = data.get('balance')
        
        try:
            balance = int(balance)
        except ValueError:
            logger.error('Invalid balance format.')
            return jsonify({'success': False, 'message': 'Invalid balance format. Balance must be an integer.'}), 400


        # Generate a random account number
        account_number = generate_account_number()

        # Insert user details into the database
        db.users.insert_one({"name": name, "account_number": account_number, "balance": balance})

        # Return success response to the frontend
        return jsonify({'success': True, "name": name, "account_number": account_number, "balance": balance}), 201
    except Exception as e:
        logger.error(f'Error signing up: {e}')
        return jsonify({'success': False, 'message': 'Internal server error.'}), 500


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Parse JSON data
        account_number = data.get('account_number')
        
        try:
            user = db.users.find_one({"account_number": account_number})
        except Exception as e:
            logger.error(f'Error accessing the database: {e}')
            return jsonify({'success': False, 'message': 'Internal server error.'}), 500
    
        if user:
            return jsonify({'success': True, 'account_number': account_number}), 200
        else:
            logger.info('Invalid account number.')
            return jsonify({'success': False, 'message': 'Invalid account number. Please try again.'}), 401

    else:
        return jsonify({'success': False, 'message': 'Only POST method is supported for login.'}), 405

@app.route('/user-info', methods=['GET'])
def user_info():
    account_number = request.args.get('account_number')
    
    try:
        user = db.users.find_one({"account_number": account_number})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify({'success': True, 'user': user}), 200
        else:
            return jsonify({'success': False, 'message': 'User not found.'}), 404
    except Exception as e:
        logger.error(f'Error accessing the database: {e}')
        return jsonify({'success': False, 'message': 'Internal server error.'}), 500

@app.route('/transfer', methods=['POST'])
def transfer():
    from_account = request.json.get('from_account')
    to_account = request.json.get('to_account')
    amount = request.json.get('amount')

    if not from_account or not to_account or not amount:
        logger.error('All fields are required.')
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    try:
        amount = float(amount)
    except ValueError:
        logger.error('Invalid amount format.')
        return jsonify({'success': False, 'message': 'Invalid amount format.'}), 400

    try:
        from_user = db.users.find_one({"account_number": from_account})
        to_user = db.users.find_one({"account_number": to_account})
    except Exception as e:
        logger.error(f'Error accessing the database: {e}')
        return jsonify({'success': False, 'message': 'Internal server error.'}), 500

    if from_user and to_user and from_user['balance'] >= amount:
        try:
            db.users.update_one({"account_number": from_account}, {"$inc": {"balance": -amount}})
            db.users.update_one({"account_number": to_account}, {"$inc": {"balance": amount}})
        except Exception as e:
            logger.error(f'Error updating the database: {e}')
            return jsonify({'success': False, 'message': 'Internal server error.'}), 500

        return jsonify({'success': True, 'message': 'Transfer completed.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Transfer failed.'}), 400

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'User Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(user):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"User Report for {user['name']}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Account Number: {user['account_number']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Balance: ${user['balance']}", ln=True, align='L')
    pdf.cell(200, 10, txt="Transactions:", ln=True, align='L')

    for transaction in user.get('transactions', []):
        transaction_date = transaction['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, txt=f"{transaction_date} - {transaction['type']} - ${transaction['amount']}", ln=True, align='L')

    file_path = f"/tmp/{user['account_number']}_report.pdf"
    pdf.output(file_path)
    return file_path

@app.route('/generate-report', methods=['GET'])
def generate_report():
    try:
        account_number = request.args.get('account_number')
        if not account_number:
            return jsonify({'error': 'Account number is required'}), 400

        user = db.users.find_one({'account_number': account_number})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        file_path = generate_pdf(user)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print("Error generating report:", str(e))
        return jsonify({'error': 'Error generating report'}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
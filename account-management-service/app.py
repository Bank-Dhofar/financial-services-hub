from flask import Flask, request, jsonify, redirect, url_for, render_template
from database import create_user, find_user, update_balance, delete_user

app = Flask(__name__)

# Your database-related routes
@app.route('/api/user', methods=['POST'])
def create_new_user():
    data = request.json
    create_user(data['name'], data['account_number'], data['balance'])
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/user/<int:account_number>', methods=['GET'])
def get_user(account_number):
    user = find_user(account_number)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/user/<int:account_number>', methods=['PUT'])
def update_user_balance(account_number):
    data = request.json
    update_balance(account_number, data['balance'])
    return jsonify({'message': 'User balance updated successfully'}), 200

@app.route('/api/user/<int:account_number>', methods=['DELETE'])
def delete_existing_user(account_number):
    delete_user(account_number)
    return jsonify({'message': 'User deleted successfully'}), 200

# Your login and signup routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form['account_number']
        user = find_user(account_number)
        if user:
            # User exists, you can perform further validation here
            return redirect(url_for('success'))
        else:
            return render_template('login.html', message='Invalid account number. Please try again.')
    return render_template('login.html', message='')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        account_number = request.form['account_number']
        balance = request.form['balance']
        create_user(name, account_number, balance)
        return redirect(url_for('success'))
    return render_template('signup.html')

@app.route('/success')
def success():
    return 'Success!'

if __name__ == '__main__':
    app.run(debug=True)

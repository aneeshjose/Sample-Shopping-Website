from flask import Flask, redirect, url_for, request
from user import User
from databse import SQLHelper as Helper
app = Flask(__name__)

helper = Helper()


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            password = request.form['password']
            user = User()
            return user.createUser(email, password, name, phone, helper)
        except Exception:
            return {'status': 'failed', 'message': 'Unknown'}
    else:
        return {'status': 'failed', 'message': 'UnhandledRequest'}


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User()
            return user.loginUser(email, password, helper)
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'failed', 'message': 'UnhandledRequest'}


if __name__ == '__main__':
    app.run()

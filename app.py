from flask import Flask, redirect, url_for, request, render_template
from user import User
from database import SQLHelper as Helper
app = Flask(__name__)

helper = Helper()


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            password = request.form['password']
            user = User()
            return user.createUser(email, password, name, phone, helper)
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}
    else:
        return render_template('signup.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User()
            return user.loginUser(email, password, helper)
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}
    else:
        return render_template('signin.html', message=' '.join(list(request.args['message'].split())))


@app.route('/')
def indexPage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

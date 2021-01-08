from flask import Flask, redirect, url_for, request, render_template, session
from database import SQLHelper as Helper
from user import User
from homepage import HomePage
from cart import Cart
from search import Search
from account import Account

app = Flask(__name__)

helper = Helper()


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # redirect to homepage if user already signedin
    try:
        session['email']
        session['auth_key']
        return redirect('/')
    except:
        pass

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
    # redirect to homepage if user already signedin
    try:
        session['email']
        session['auth_key']
        return redirect('/')
    except:
        pass

    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User()
            return user.loginUser(email, password, helper)
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}
    else:
        try:
            return render_template('signin.html')
        except Exception as e:
            print(e)
            return 'return'

        # return render_template('signin.html', message=' '.join(list(request.args['message'].split())))


@app.route('/logout')
def logout():
    return User().logout(helper)


@app.route('/', methods=['GET'])
def indexPage():
    return HomePage().fetchHomePage(helper)


@app.route('/addtocart/<prodid>')
def addToCart(prodid):
    return Cart().addToCart(helper, prodid)


@app.route('/removefromcart/<prodid>')
def removeFromCart(prodid):
    return Cart().removeFromCart(helper, prodid)


@app.route('/subtractcart/<prodid>')
def subtractcart(prodid):
    return Cart().subtractcart(helper, prodid)


@app.route('/search', methods=['GET'])
def search():
    return Search().search(helper)


@app.route('/cart')
def cart():
    return Cart().displayCart(helper)


@app.route('/account')
def account():
    return Account(helper).sendAccountInfo()


@app.route('/subscribe')
def subscribe():
    return Account(helper).subscribe()


@app.route('/unsubscribe')
def unsubscribe():
    return Account(helper).unsubscribe()


if __name__ == '__main__':
    app.secret_key = "QWERTY"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

import mysql.connector as sql

from flask import render_template, redirect, url_for, session, request, make_response

import string
import random


class User:

    def createUser(self, email, password, name, phone, dbHelper):
        resp = make_response()
        resp.set_cookie('cart', '')
        try:
            # whether the user already exists
            currentUser = dbHelper.query(
                'select name from userauth where email=\'{}\' or phone={}'
                .format(email, phone))
            if(len(currentUser) > 0):
                return render_template('signup.html', message="User already exists")
        except:
            pass
        try:
            # add the new user to database
            if dbHelper.query('insert into userauth(name,phone,email,password) values(\'{}\',{},\'{}\',\'{}\')'
                              .format(name, phone, email, password)):
                return redirect(('signin?message=Registered+successfully'))
        except Exception as e:
            # error occured as a result of various reasons such as
            # database connection errors, format errors, etc.
            return render_template('signup.html', message=str(e))

    def loginUser(self, email, password, dbHelper):
        resp = make_response()
        resp.set_cookie('cart', '')
        try:
            # check whether entered email id is already in the db
            # if not, send back to login page with error message
            if(len(dbHelper.query('select * from userauth where email=\'{}\''.format(email))) == 0):
                return render_template('signin.html', message="Email id not yet registered")
            queryRes = dbHelper.query(
                'select * from userauth where email=\'{}\' and password=\'{}\''.format(email, password))
            if(len(queryRes) == 1):
                session.pop('email', None)
                session.pop('auth_key', None)
                # login successful add random session variables
                randomString = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=25))
                dbHelper.query('insert into user_sessions(email,sessionid) values(\'{}\',\'{}\')'
                               .format(email, randomString))
                session['email'] = email
                session['auth_key'] = randomString
                return redirect('/')

            else:
                return render_template('signin.html', message="Incorrect email id or password")

        except Exception as e:
            # unhandled exception
            return render_template('signin.html', message=str(e))

    def logout(self, dbHelper):
        # clear the session variables from local and db
        # pop cookies from local
        # and redirect back to sign in
        dbHelper.query('delete from user_sessions where email=\'{}\' and sessionid=\'{}\''
                       .format(session['email'], session['auth_key']))
        resp = make_response()
        resp.set_cookie('cart', '')
        session.pop('email', None)
        session.pop('auth_key', None)

        return redirect(url_for('signin'))

    def checkUser(self, dbHelper):
        try:
            email = session['email']
            auth_key = session['auth_key']
            if(email is None or auth_key is None):
                # user is not signed in
                raise Exception

            if len(dbHelper.query('select * from user_sessions where email=\'{}\' and sessionid=\'{}\''
                                  .format(email, auth_key))) == 0:
                # user credentials doesnot match
                raise Exception
        except:
            return redirect(url_for('signin'))

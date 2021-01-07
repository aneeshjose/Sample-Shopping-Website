import mysql.connector as sql

from flask import render_template, redirect, url_for


class User:

    def createUser(self, email, password, name, phone, dbHelper):
        try:
            # whether the user already exists
            if(len(dbHelper.query('select name from userauth where email=\'{}\' or phone={}'.format(email, phone))) > 0):
                return render_template('signup.html', error="User already exists")
        except:
            pass
        try:
            # add the new user to database
            return dbHelper.query('insert into userauth(name,phone,email,password) values(\'{}\',{},\'{}\',\'{}\')'.format(name, phone, email, password))
        except Exception as e:
            # error occured as a result of various reasons such as
            # database connection errors, format errors, etc.
            return render_template('signup', error=str(e))

    def loginUser(self, email, password, dbHelper):
        try:
            # check whether entered email id is already in the db
            # if not, send back to login page with error message

            if(len(dbHelper.query('select * from userauth where email=\'{}\''.format(email))) == 0):
                return render_template('signin.html', error="email id not yet registered")
            queryRes = dbHelper.query(
                'select * from userauth where email=\'{}\' and password=\'{}\''.format(email, password))
            if(len(queryRes) == 1):
                return redirect(url_for('homepage'))
            else:
                return render_template('login', error="Incorrect email id or password")

        except Exception as e:
            # unhandled exception
            return render_template('login', error=str(e))

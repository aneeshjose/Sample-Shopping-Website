from flask import redirect, request, session, render_template
from user import User


class Account:
    def __init__(self, dbHelper):
        try:
            self.email = session['email']
            self.auth_key = session['auth_key']
            self.dbHelper = dbHelper
        except:
            pass

    def sendAccountInfo(self):
        User().checkUser(self.dbHelper)
        subscribed = len(self.dbHelper.query(
            "select * from subscriptions where userid='{}'".format(self.email))) == 1
        return render_template('account.html', subscribed=subscribed)

    def subscribe(self):
        User().checkUser(self.dbHelper)
        self.dbHelper.query(
            'insert into subscriptions values(\'{}\')'.format(self.email))
        return 'True'

    def unsubscribe(self):
        User().checkUser(self.dbHelper)
        self.dbHelper.query(
            'delete from subscriptions where userid = \'{}\''.format(self.email))
        return 'True'

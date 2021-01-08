from flask import session, request, redirect, render_template
import random
import string
import time

from user import User


class Purchase:
    def __init__(self, dbHelper):
        self.dbHelper = dbHelper

    def checkout(self):
        if(request.method == 'POST'):
            User().checkUser(self.dbHelper)
            self.address = request.form['address']
            self.totalCost = request.form['totalcost']
            return render_template('checkout.html', address=self.address, totalCost=self.totalCost)

    def buy(self):
        if(request.method == 'POST'):
            User().checkUser(self.dbHelper)
            address = request.form['address']
            card = request.form['card']
            otp = request.form['otp']
            email = session['email']
            purchaseid = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=25))
            cart = self.dbHelper.query(
                "select * from cart where userid='{}'".format(email))
            totalCostServer = 0
            for items in cart:
                prod = self.dbHelper.query(
                    "select * from products where id='{}'".format(items[1]))
                cost = (prod[0][3] * items[2])
                totalCostServer += cost
                self.dbHelper.query('insert into purchasedproducts(purchaseid,user,product,count,individualcost) values(\'{}\',\'{}\',\'{}\',{},{})'
                                    .format(purchaseid, items[0], items[1], items[2], prod[0][3]))
            self.dbHelper.query(
                "insert into purchasehistory(userid,id,address,card,otp,time,totalcost) values('{}','{}','{}',{},{},{},{})"
                .format(email, purchaseid, address, int(card), int(otp), int(time.time()), int(totalCostServer)))
            self.dbHelper.query(
                'delete from cart where userid=\'{}\''.format(email))
            return redirect('/')

    def getHistory(self):
        purchases = self.dbHelper.query(
            "select * from purchasehistory where userid='{}'".format(session['email']))
        purchases = [list(x) for x in purchases]
        for p in purchases:
            p[5] = time.ctime(p[5])
        return render_template('history.html', purchases=purchases)

    def historyExtended(self):
        pass

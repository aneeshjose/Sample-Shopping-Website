from flask import session, redirect, render_template, request


class Purchase:
    def __init__(self, dbHelper):
        self.dbHelper = dbHelper

    def checkout(self):
        if(request.method == 'POST'):
            self.address = request.form['address']
            self.totalCost = request.form['totalcost']
            return render_template('checkout.html', address=self.address, totalCost=self.totalCost)

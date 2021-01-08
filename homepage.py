from flask import render_template, session, request


class HomePage:
    def __init__(self):
        self.email = session['email']
        self.auth_key = session['auth_key']
        self.userSignedIn = False

    def fetchHomePage(self, dbHelper):
        if session['email'] is not None:
            self.userSignedIn = True
        try:
            category = dict(request.args)['category']
            outCategories = dbHelper.query(
                'select distinct category from products')
            outProducts = dbHelper.query(
                'select * from products where category = \'{}\''.format(category))

            return render_template('index.html',
                                   categories=outCategories,
                                   products=outProducts,
                                   userSignedIn=self.userSignedIn)
        except Exception:
            return render_template('index.html',
                                   categories=dbHelper.query(
                                       'select distinct category from products'),
                                   userSignedIn=self.userSignedIn)

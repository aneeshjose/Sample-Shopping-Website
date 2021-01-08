from flask import render_template, session, request


class HomePage:
    def __init__(self):
        self.email = session['email']
        self.auth_key = session['auth_key']

    def fetchHomePage(self, dbHelper):
        # try:
        category = dict(request.args)['category']
        outCategories = dbHelper.query(
            'select distinct category from products')
        outProducts = dbHelper.query(
            'select * from products where category = \'{}\''.format(category))

        return render_template('index.html', categories=outCategories, products=outProducts)
        # except Exception as e:
        #     print(e)
        #     return render_template('index.html', categories=dbHelper.query(
        #         'select distinct category from products'))

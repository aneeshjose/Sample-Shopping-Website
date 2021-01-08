from flask import session, make_response, request, render_template
from user import User
from json import dumps, loads


class Cart:
    def addToCart(self, dbHelper, prodId):

        try:
            email = session['email']
            # since the email is nol null, check the user session
            # also matches the user session auth_key
            User().checkUser(dbHelper)
            # check whether the product is already added to cart by the user
            # if not added, insert the values
            #  if added, increment the count by 1
            count = dbHelper.query(
                'select count(*) from cart where userid=\'{}\' and productid=\'{}\''
                            .format(email, prodId))
            if count[0][0] == 0:
                dbHelper.query('insert into cart values(\'{}\',\'{}\',{})'
                               .format(email, prodId, 1))
                return 'success'
            dbHelper.query(
                'update cart set count=count+1 where userid=\'{}\' and productid=\'{}\''
                .format(email, prodId))
            return 'success'
        except:
            # The user has not signed in yet.
            # So add the product id to the cookie in comma seperated format
            # if there are no available cookies for this, creating a new one
            available = request.cookies.get('cart')
            # creating local cart datastructure in the format {productid:count}
            prods = loads(available)
            try:
                prods[prodId] += 1
            except:
                prods[prodId] = 1
            resp = make_response()
            resp.set_cookie('cart', dumps(prods))
            return resp

    def subtractcart(self, dbHelper, id):
        try:
            email = session['email']
            if dbHelper.query(
                    "select * from cart where userid='{}' and productid='{}'".format(email, id))[0][0] == 1:
                return False
            dbHelper.query("update cart set count=count-1 where userid='{}' and productid='{}'"
                           .format(email, id))
            return True
        except:
            available = request.cookies.get('cart')
            # creating local cart datastructure in the format {productid:count}
            prods = loads(available)
            try:
                if prods[id] == 1:
                    return True
                prods[id] -= 1
            except:
                pass
            resp = make_response()
            resp.set_cookie('cart', dumps(prods))
            return resp
        return 'success'

    def removeFromCart(self, dbHelper, id):
        try:
            dbHelper.query("delete from cart where userid='{}' and productid='{}'"
                           .format(session['email'], id))
        except:
            available = request.cookies.get('cart')
            prods = loads(available)
            del prods[id]
            resp = make_response()
            resp.set_cookie('cart', dumps(prods))
            return resp
        return 'success'

    def displayCart(self, dbHelper):
        try:
            email = session['email']

            self.cartProducts = dbHelper.query('select productid,count from cart where userid=\'{}\''
                                               .format(email))
        except:
            cart = request.cookies.get('cart')
            try:
                self.prods = loads(cart)
            except:
                self.prods = {}
            self.cartProducts = [(id, count)
                                 for id, count in self.prods.items()]
            # self.cartProducts =
        prodEnlarged = []
        for id in self.cartProducts:
            prodEnlarged.append({'item': dbHelper.query(
                "select * from products where id='{}'".format(id[0])), 'count': id[1]})
        return render_template('cart.html', products=prodEnlarged)

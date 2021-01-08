from flask import session, make_response, request, render_template
from user import User


class Cart:
    def addToCart(self, dbHelper, prodId):

        if session['email'] is not None:
            # since the email is nol null, check the user session
            # also matches the user session auth_key
            User().checkUser(dbHelper)
            # check whether the product is already added to cart by the user
            # if not added, insert the values
            #  if added, increment the count by 1
            count = dbHelper.query(
                'select count(*) from cart where userid=\'{}\' and productid=\'{}\''
                            .format(session['email'], prodId))
            if count[0][0] == 0:
                dbHelper.query('insert into cart values(\'{}\',\'{}\',{})'
                               .format(session['email'], prodId, 1))
                return 'success'
            dbHelper.query(
                'update cart set count=count+1 where userid=\'{}\' and productid=\'{}\''
                .format(session['email'], prodId))
            return 'success'
        else:
            # The user has not signed in yet.
            # So add the product id to the cookie in comma seperated format
            # if there are no available cookies for this, creating a new one
            available = request.cookies.get('cart')
            if available == None:
                available = ''
            resp = make_response()
            resp.set_cookie('cart', available+','+prodId)
            return 'success'

    def displayCart(self, dbHelper):
        email = session['email']
        cartProducts = dbHelper.query('select productid from cart where userid=\'{}\''
                                      .format(email))
        prodEnlarged = []
        for id in cartProducts:
            prodEnlarged.append(dbHelper.query(
                "select * from products where id='{}'".format(id[0])))
        return render_template('cart.html', products=prodEnlarged)

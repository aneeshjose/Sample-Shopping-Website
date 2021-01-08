from flask import request, render_template


class Search:
    def search(self, dbHelper):
        query = (dict(request.args)['q']).lower()

        result = dbHelper.query(
            'select * from products where lower(name) like \'%{}%\''.format(query))
        return render_template('search.html', query=query, result=result)

import mysql.connector as sql


class User:

    def createUser(self, email, password, name, phone, dbHelper):
        try:
            return dbHelper.query('insert into userauth(name,phone,email,password) values(\'{}\',{},\'{}\',\'{}\')'.format(name, phone, email, password))
        except Exception:
            return {'status': 'failed', 'message': 'UserAlreadyExists'}

    def loginUser(self, email, password, dbHelper):
        try:
            if(len(dbHelper.query('select * from userauth where email=\'{}\''.format(email))) == 0):
                return {'status': 'failed', 'message': 'UserNotFound'}
            queryRes = dbHelper.query(
                'select * from userauth where email=\'{}\' and password=\'{}\''.format(email, password))
            if(len(queryRes) == 1):
                return {'status': 'success'}
            else:
                return {'status': 'failed', 'message': 'PasswordError,{},{}'.format(len(queryRes), queryRes)}

        except Exception as e:
            return {'status': 'failed', 'message': str(e)}

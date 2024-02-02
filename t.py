# from unittest import result
# import mysql.connector
# from flask import Flask, render_template, request, redirect, url_for, session
# import mysql.connector

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'


# queries = ['easy'] #, 'hard', 'harder1', 'harder2', 'harder3'
# # Define a function to execute a query and fetch results
# # def execute_query(query):
# #     query = 'SELECT * FROM currencymarket'

# #     conn = mysql.connector.connect(
# #         host="localhost",
# #         user="usermanager",
# #         password="usermanager",
# #         database="projSchema"
# #     )
# #     cursor = conn.cursor(dictionary=True)

# #     try:
# #         cursor.execute(query)
# #         data = cursor.fetchall()
# #         return data
# #     except mysql.connector.Error as error:
# #         print(f"Error executing query: {error}")
# #         return None
# #     finally:
# #         cursor.close()
# #         conn.close()

# @app.route('/')
# def index():
#     return render_template('login3.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     # Check user role and authenticate against the MySQL server
#     try:
#         conn = mysql.connector.connect(
#             user=username,
#             password=password,
#             host='localhost',
#             database='projSchema'
#         )
#        # cursor = conn.cursor()
#         # If connection is successful, the user is valid
#         session['user_role'] = username
#         print (f'{username}_dashboard')
#         return redirect(url_for(f'{username}_dashboard'))

#     except mysql.connector.Error as e:
#         print(f"Error: {e}")
#         return render_template('login3.html', error='Invalid credentials')

    
#             #conn.close()
# @app.route('/admin/dashboard')
# def admin_dashboard():
#     return render_template('dashboard3.html', role='admin', queries=queries)

# @app.route('/report/dashboard')
# def report_dashboard():
#     return render_template('dashboard3.html', role='report', queries=queries)

# @app.route('/usermanager/dashboard')
# def usermanager_dashboard():
#     return render_template('dashboard3.html', role='usermanager', queries=queries)


# # Define a route that takes a query parameter
# @app.route('/easy')
# def easy():
#     query = 'SELECT userID, userName, dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance FROM projschema.wallet w, projschema.user u WHERE u.userID = w.user_userID'
#     # Execute the provided query
#     user = session.get('user_role')
#     try:
#         # conn = mysql.connector.connect(
#         #     user=user,
#         #     password=user,
#         #     host='localhost',
#         #     database='projSchema'
#         # )

#         cursor = conn.cursor()
#         cursor.execute(query)
#         data = cursor.fetchall()
#         return render_template('query_results.html', result=data)
#     except mysql.connector.Error as error:
#         print(f"Error executing query: {error}")
#         #return None
#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == '__main__':
#     app.run(port = 3000, debug=True)




# from flask import Flask, render_template
# import mysql.connector

# app = Flask(__name__)

# # Function to execute the query and fetch data
# def fetch_data_from_db(query):
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="your_username",
#         password="your_password",
#         database="your_database"
#     )
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return data

# # Flask route to render the HTML template
# @app.route('/query_results')
# def query_results():
#     # Replace this query with your actual query
#     query = "SELECT userID, userName FROM projSchema.user"
   
#     # Fetch data from the database
#     data = fetch_data_from_db(query)
   
#     # Render the HTML template with the fetched data
#     return render_template('query_results.html', data=data)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
queries = ['easy', 'hard', 'harder1', 'harder2', 'harder3']

# Define a decorator to check user roles
def login_required(roles=[]):
    def decorator(view_func):
        def wrapper(*args, **kwargs):
            user_role = session.get('user_role')
            if user_role not in roles:
                return render_template('unauthorized.html')
            return view_func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def index():
    return render_template('login3.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(
                user=username,
                password=password,
                host='localhost',
                database='projSchema'
            )
            # Check user role and authenticate
            session['user_role'] = username
            return redirect(url_for(f'{username}_dashboard'))
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return render_template('login3.html', error='Invalid credentials')
        finally:
            conn.close()
    else:
        return render_template('login3.html')
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard3.html', role='admin', queries=queries)

@app.route('/report/dashboard')
def report_dashboard():
    return render_template('dashboard3.html', role='report', queries=queries)

@app.route('/usermanager/dashboard')
def usermanager_dashboard():
    return render_template('dashboard3.html', role='usermanager', queries=queries)

@app.route('/easy', methods=['GET','POST'])
#@login_required(roles=['admin', 'usermanager', 'report'])
def easy():
    print("executing easy")
    if request.method == 'POST':
        query = 'SELECT userID, userName, dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance FROM projschema.wallet w, projschema.user u WHERE u.userID = w.user_userID;'
        print('query: ', query)
        user = session.get('user_role')
        try:
            conn = mysql.connector.connect(
                user=user,
                password=user,
                host='localhost',
                database='projSchema'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            if data:
                return render_template('query_results.html', data=data)
            else:
                return render_template('query_results.html', error='no results found')
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
            return render_template('error.html', error='Error executing the query.')
        finally:
            cursor.close()
            conn.close()
            print("conn closed")


@app.route('/hard', methods=['GET','POST'])
#@login_required(roles=['admin', 'usermanager', 'report'])
def hard():
    print("executing hard")
    if request.method == 'POST':
        query = '''SELECT 
                        transactionID,
                        u1.userName AS Seller,
                        u2.userName AS Buyer,
                        c1.name AS BaseCurrency,
                        c2.name AS TargetCurrency
                    FROM 
                        projschema.transaction t 
                    JOIN 
                        projschema.user u1 ON t.user_sellerID = u1.userID
                    JOIN 
                        projschema.user u2 ON t.user_buyerID1 = u2.userID
                    JOIN 
                        projschema.currencyMarket c1 ON c1.currencyID = t.currency_fromID
                    JOIN
                        projschema.currencyMarket c2 ON c2.currencyID = t.currency_toID
                    WHERE
                        (t.date >'2009-01-01' AND t.date <'2010-01-01') AND 
                        ((c1.name = 'toman' AND c2.name = 'dollar') OR (c1.name = 'dollar' AND c2.name = 'toman'));'''
        print('query: ', query)
        user = session.get('user_role')
        try:
            conn = mysql.connector.connect(
                user=user,
                password=user,
                host='localhost',
                database='projSchema'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            if data:
                return render_template('query_results.html', data=data)
            else:
                return render_template('query_results.html', error='no results found')
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
            return render_template('error.html', error='Error executing the query.')
        finally:
            cursor.close()
            conn.close()
            print("conn closed")


@app.route('/harder1', methods=['GET','POST'])
#@login_required(roles=['admin', 'usermanager', 'report'])
def harder1():
    print("executing harder1")
    if request.method == 'POST':
        query = '''SELECT currency, monthNumber, buy, sell, buy+sell AS total FROM
                        (
                        SELECT
                            m.name AS currency,
                            EXTRACT(MONTH FROM t.date) AS monthNumber,
                            COALESCE(SUM(t2.amount), 0) AS buy,
                            COALESCE(SUM(t3.amount2), 0) AS sell,
                            COUNT(t2.amount) AS c1,
                            COUNT(t3.amount2) AS c2
                        FROM
                            projschema.currencyMarket m
                        JOIN
                            projschema.transaction t ON m.currencyID = t.currency_fromID
                        LEFT JOIN
                            (SELECT user_buyerID1, amount, currency_fromID FROM projschema.transaction WHERE EXTRACT(YEAR FROM date) = 2009) AS t2
                            ON m.currencyID = t2.currency_fromID
                        LEFT JOIN
                            (SELECT user_sellerID, amount2, currency_toID FROM projschema.transaction WHERE EXTRACT(YEAR FROM date) = 2009) AS t3
                            ON m.currencyID = t3.currency_toID
                        WHERE
                            EXTRACT(YEAR FROM t.date) = 2009
                        GROUP BY
                            currency, monthNumber
                            ) AS returned 
                        ORDER BY
                            currency, monthNumber;'''
        #print('query: ', query)
        user = session.get('user_role')
        try:
            conn = mysql.connector.connect(
                user=user,
                password=user,
                host='localhost',
                database='projSchema'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            #print(data)
            if data:
                return render_template('query_results.html', data=data)
            else:
                return render_template('query_results.html', error='no results found')
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
            return render_template('error.html', error='Error executing the query.')
        finally:
            cursor.close()
            conn.close()
            #print("conn closed")

@app.route('/harder2', methods=['GET','POST'])
#@login_required(roles=['admin', 'usermanager', 'report'])
def harder2():
    print("executing harder2")
    if request.method == 'POST':
        query = '''SELECT
                        userID,
                        userName,
                        a1 + a2 AS `total in dollars`
                    FROM
                        (
                            SELECT
                                u.userID,
                                u.userName,
                                SUM(t1.amount) AS a1,
                                SUM(t2.amount2) AS a2
                            FROM
                                projschema.user u
                            JOIN
                                (SELECT * FROM projschema.transaction WHERE currency_fromID = 0 AND currency_toID = 1) AS t1
                                ON (u.userID = t1.user_buyerID1 OR u.userID = t1.user_sellerID)
                            INNER JOIN
                                (SELECT * FROM projschema.transaction WHERE currency_fromID = 1 AND currency_toID = 0) AS t2
                                ON (u.userID = t2.user_buyerID1 OR u.userID = t2.user_sellerID)
                            GROUP BY
                                u.userID, u.userName
                        ) AS returned
                    ORDER BY 
                        `total in dollars` DESC
                    LIMIT 5;'''
        #print('query: ', query)
        user = session.get('user_role')
        try:
            conn = mysql.connector.connect(
                user=user,
                password=user,
                host='localhost',
                database='projSchema'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            #print(data)
            if data:
                return render_template('query_results.html', data=data)
            else:
                return render_template('query_results.html', error='no results found')
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
            return render_template('error.html', error='Error executing the query.')
        finally:
            cursor.close()
            conn.close()
            #print("conn closed")

@app.route('/harder3', methods=['GET','POST'])
#@login_required(roles=['admin', 'usermanager', 'report'])
def harder3():
    print("executing harder3")
    if request.method == 'POST':
        query = '''SELECT 
                        sq1.curr1 AS 'currency 1', 
                        sq1.curr2 AS 'currency 2', 
                        count(t1.transactionID) AS 'number of transactions',
                        SUM(amount) AS 'amount in dollors',
                        FLOOR(SUM(amount) / NULLIF(count(t1.transactionID),0)) AS average
                    FROM ( SELECT transactionID, date, amount * cm1.buyRate / cm2.buyrate AS amount, currency_fromID, currency_toID 
                        FROM projschema.transaction
                        JOIN projschema.currencymarket cm1 ON currency_fromID = cm1.currencyID
                        JOIN projschema.currencymarket cm2 ON cm2.currencyID = 0
                            WHERE date>'2009-01-01' AND date<'2011-01-01' ) AS t1
                    JOIN
                        (SELECT m1.currencyID AS currency1, m2.currencyID AS currency2, m1.name AS curr1, m2.name AS curr2
                        FROM projschema.currencymarket m1 INNER JOIN projschema.currencymarket m2 ON m1.currencyID < m2.currencyID) AS sq1
                    ON ((sq1.currency1 = t1.currency_toID AND sq1.currency2 = t1.currency_fromID)OR (sq1.currency2 = t1.currency_toID AND sq1.currency1 = t1.currency_fromID)) 
                    GROUP BY sq1.currency1, sq1.currency2;'''
        #print('query: ', query)
        user = session.get('user_role')
        try:
            conn = mysql.connector.connect(
                user=user,
                password=user,
                host='localhost',
                database='projSchema'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            #print(data)
            if data:
                return render_template('query_results.html', data=data)
            else:
                return render_template('query_results.html', error='no results found')
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
            return render_template('error.html', error='Error executing the query.')
        finally:
            cursor.close()
            conn.close()
            #print("conn closed")




if __name__ == '__main__':
    app.run(port=3000, debug=True)

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
queries = ['easy', 'hard']

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

if __name__ == '__main__':
    app.run(port=3000, debug=True)




@app.route('/hard', methods=['GET','POST'])
#@login_required(roles=['admin', 'usermanager', 'report'])
def hard():
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

if __name__ == '__main__':
    app.run(port=3000, debug=True)
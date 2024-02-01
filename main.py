import mysql.connector
import random
from datetime import timedelta
import json
from flask import Flask, jsonify, request
f = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="project"
)
@f.route('/createUser/', methods=['GET'])
def createUser():
    cursor = mydb.cursor(dictionary=True)
    name = request.args['userName']
    password = request.args['userPassword']
    email = request.args['userEmail']
    cursor.execute("INSERT INTO user (userName, userPassword, userEmail) VALUES (%s, %s)", (name, password, email))
    mydb.commit()
@f.route('/createWallet/', methods=['GET'])
def createWallet():
    cursor = mydb.cursor(dictionary=True)
    dollarBalance = request.args['dollarBalance']
    tomanBalance = request.args['tomanBalance']
    lireBalance = request.args['lireBalance']
    poundBalance = request.args['poundBalance']
    euroBalance = request.args['euroBalance']
    user_userID = request.args['user_userID']
    cursor.execute("INSERT INTO wallet (dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance, user_userID) VALUES (%s, %s, %s, %s, %s, %s)",
                   (dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance, user_userID))
    mydb.commit()

@f.route('/createCurrencymarket/', methods=['GET'])
def createCurrencymarket():
    cursor = mydb.cursor(dictionary=True)
    name = request.args['name']
    buyRate = request.args['buyRate']
    sellRate = request.args['sellRate']
    cursor.execute("INSERT INTO currencymarket (name, buyRate, sellRate) VALUES (%s, %s, %s)", (name, buyRate, sellRate))
    mydb.commit()
@f.route('/createTransaction/', methods=['GET'])
def createTransaction():
    cursor = mydb.cursor(dictionary=True)
    amount = request.args['amount']
    user_sellerID = request.args['user_sellerID']
    user_buyerID1 = request.args['user_buyerID1']
    currency_fromID = request.args['currency_fromID']
    currency_toID = request.args['currency_toID']
    amount2 = request.args['amount2']
    cursor.execute("INSERT INTO transaction (amount, user_sellerID, user_buyerID1, currency_fromID, currency_toID, amount2) VALUES (%s, %s, %s, %s, %s, %s, %s)", (amount, user_sellerID, user_buyerID1, currency_fromID, currency_toID, amount2))
    mydb.commit()

@f.route('/readUser/<id>', methods=['GET'])
def readUser(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE userID = %s", (id,))
    result = cursor.fetchall()
    return result
@f.route('/readWallet/<id>', methods=['GET'])
def readWallet(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM wallet WHERE walletID = %s", (id,));
    result = cursor.fetchall()
    return result
@f.route('/readCurrencymarket/<id>', methods=['GET'])
def readCurrencymarket(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM currencymarket WHERE currencyID  = %s", (id,))
    return cursor.fetchall()
@f.route('/readTransaction/<id>', methods=['GET'])
def readTransaction(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transaction WHERE transactionID  = %s", (id,))
    return cursor.fetchall()
@f.route('/updateUser/<id>', methods=['GET'])
def updateUser(id):
    cursor = mydb.cursor(dictionary=True)
    name = request.args['userName']
    password = request.args['userPassword']
    email = request.args['userEmail']
    cursor.execute("UPDATE user SET userName = %s, userPassword = %s, userEmail = %s WHERE userID = %s", (name, password, email, id))
    mydb.commit()
@f.route('/updateWallet/<id>', methods=['GET'])
def updateWallet(id):
    cursor = mydb.cursor(dictionary=True)
    dollarBalance = request.args['dollarBalance']
    tomanBalance = request.args['tomanBalance']
    lireBalance = request.args['lireBalance']
    poundBalance = request.args['poundBalance']
    euroBalance = request.args['euroBalance']
    user_userID = request.args['user_userID']
    cursor.execute("UPDATE wallet SET dollarBalance = %s, tomanBalance = %s, lireBalance = %s, poundBalance = %s, euroBalance = %s, user_userID = %s WHERE walletID = %s",
                   (dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance, user_userID, id))
    mydb.commit()

@f.route('/updateCurrencymarket/<id>', methods=['GET'])
def updateCurrencymarket(id):
    cursor = mydb.cursor(dictionary=True)
    name = request.args['name']
    buyRate = request.args['buyRate']
    sellRate = request.args['sellRate']
    cursor.execute("UPDATE currencymarket SET name = %s, buyRate = %s, sellRate = %s WHERE currencyID = %s", (name, buyRate, sellRate, id))
    mydb.commit()
@f.route('/updateTransaction/<id>', methods=['GET'])
def updateTransaction(id):
    cursor = mydb.cursor(dictionary=True)
    amount = request.args['amount']
    user_sellerID = request.args['user_sellerID']
    user_buyerID1 = request.args['user_buyerID1']
    currency_fromID = request.args['currency_fromID']
    currency_toID = request.args['currency_toID']
    amount2 = request.args['amount2']
    cursor.execute("UPDATE transaction SET amount = %s, user_sellerID = %s, user_buyerID1 = %s, currency_fromID = %s, currency_toID = %s, amount2 = %s WHERE transactionID = %s", (amount, user_sellerID, user_buyerID1, currency_fromID, currency_toID, amount2, id))
    mydb.commit()
@f.route('/deleteUser/<id>', methods=['GET'])
def deleteUser(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("DELETE FROM user WHERE userID = %s", (id,))
    mydb.commit()
@f.route('/deleteWallet/<id>', methods=['GET'])
def deleteWallet(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("DELETE FROM wallet WHERE walletID = %s", (id,));
    mydb.commit()
@f.route('/deleteCurrencymarket/<id>', methods=['GET'])
def deleteCurrencymarket(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("DELETE FROM currencymarket WHERE currencyID  = %s", (id,))
    mydb.commit()
@f.route('/deleteTransaction/<id>', methods=['GET'])
def deleteTransaction(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("DELETE FROM transaction WHERE transactionID  = %s", (id,))
    mydb.commit()
if __name__ == '__main__':
    f.run(port=3000,debug=True)
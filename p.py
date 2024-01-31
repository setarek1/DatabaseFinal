from locale import currency
import traceback
import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user",
    database="projSchema"
)

cursor = conn.cursor()


try:
    tables_to_reset = ['user', 'transaction', 'wallet', 'currencyMarket']
    for t in tables_to_reset:
        delete_query = f"DELETE FROM {t};"
        cursor.execute(delete_query)
        
    auto_inc_tables = ['user', 'transaction', 'wallet']
    for t in auto_inc_tables:
        reset_auto_inc_query = f"ALTER Table {t} AUTO_INCREMENT = 1;"
        cursor.execute(reset_auto_inc_query)
    

        
    insert_user_query = "INSERT INTO user (userID, userName, userPassword, userEmail) VALUES (%s, %s, %s, %s)"
    insert_transaction_query = "INSERT INTO transaction(transactionID, date, amount, user_sellerID, user_buyerID1, currency_fromID, currency_toID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_wallet_query = "INSERT INTO wallet (walletID, dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance, user_userID) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for i in range(10000):
        user_data = (i, fake.user_name()[:45], fake.password()[:45], fake.email())
        cursor.execute(insert_user_query, user_data)
    conn.commit()
    cursor.execute("INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(0, 'dollar', 10, 10)")
    cursor.execute("INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(1, 'toman', 10, 10)")
    cursor.execute("INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(2, 'lire', 10, 10)")
    cursor.execute("INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(3, 'pound', 10, 10)")
    cursor.execute("INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(4, 'euro', 10, 10)")
    
    conn.commit()
    for i in range(10000):
        currency1 = random.randint(0,4)
        currency2 = random.randint(0,4)
        while currency1 == currency2:
            currency2 = random.randint(0,4)
        user1 = random.randint(0, 9999)
        user2 = random.randint(0, 9999)
        while user1 == user2:
            user2 = random.randint(0, 1000)
        transaction_data = (i, fake.date_time(), random.uniform(0, 1000), user1, user2, currency1, currency2)
        #print(i, user1, user2, currency1, currency2)
        cursor.execute(insert_transaction_query, transaction_data)
    for i in range(10000):
        wallet_data = (i, random.uniform(0,1000),random.uniform(0,1000),random.uniform(0,1000),random.uniform(0,1000),random.uniform(0,1000), i) 
        cursor.execute(insert_wallet_query, wallet_data)
    conn.commit()
except mysql.connector.Error as error:
    print(f"main error: {error}")
    traceback.print_exc()

finally:
    cursor.close()
    conn.close() 

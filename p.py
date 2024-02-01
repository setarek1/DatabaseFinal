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
    password="",
    database="project"
)

cursor = conn.cursor()


try:
    tables_to_reset = ['user', 'transaction', 'wallet']
    for t in tables_to_reset:
        delete_query = f"DELETE FROM {t};"
        # cursor.execute(delete_query)
        
    # auto_inc_tables = ['User', 'book']
    # for t in auto_inc_tables:
    #     reset_auto_inc_query = f"ALTER Table {t} AUTO_INCREMENT = 1;"
    #     cursor.execute(reset_auto_inc_query)
        
    insert_user_query = "INSERT INTO user ( userName, userPassword, userEmail) VALUES (%s, %s, %s)"
    insert_transaction_query = "INSERT INTO transaction(date, amount, user_sellerID, user_buyerID1, currency_fromID, currency_toID) VALUES ( %s, %s, %s, %s, %s, %s)"
    insert_wallet_query = "INSERT INTO wallet ( dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance, user_userID) VALUES (%s, %s, %s, %s, %s, %s)"

    for i in range(10000):
        user_data = (fake.user_name()[:45], fake.password()[:45], fake.email())
        # cursor.execute(insert_user_query, user_data)
        #print("user table")
        currency1 = random.randint(1,5)
        currency2 = random.randint(1,5)
        while currency1 == currency2:
            currency2 = random.randint(1,5)
        transaction_data = (fake.date_time(), random.randint(1, 1000), random.randint(1,10000), random.randint(1,10000), currency1, currency2 )
        cursor.execute(insert_transaction_query, transaction_data)
        # wallet_data = (random.randint(1,1000),random.randint(1,1000),random.randint(1,1000),random.randint(1,1000),random.randint(1,1000),random.randint(1,10000))
        # cursor.execute(insert_wallet_query, wallet_data)
    conn.commit()
except mysql.connector.Error as error:
    print(f"main error: {error}")
    traceback.print_exc()

finally:
    cursor.close()
    conn.close() 
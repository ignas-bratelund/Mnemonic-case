import mysql.connector
from mysql.connector import Error


# query1 = "SELECT * FROM mnemonic.account;"
# query2 = "Insert into mnemonic.account(name, availableCash) values('test3',100);"
            

def dbQuery(query):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='mnemonic',
                                            user='root',
                                            password='was_plaintext_so_removed')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(query)
            result = []
            result = cursor.fetchall()
            connection.commit()
    except Error as e:
        result = e
        print("Mysql Error:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return result

def dbQueryList(query_list):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='mnemonic',
                                            user='root',
                                            password='was_plaintext_so_remove')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            result = []
            for query in query_list:
                cursor.execute(query)
                #Return last result
                result = cursor.fetchall()
            connection.commit()
    except Error as e:
        result = e
        print("Mysql Error:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return result

if __name__ == '__main__':
    result = dbQueryList(["Insert into account(name, availableCash) values('test5',100);", "SELECT * FROM mnemonic.account;"])
    print(result)
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)
    print(db)
    

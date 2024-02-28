from flask import Flask
from Website import app
import mysql.connector
from db_config import *



def testmysqlconnection():
    try:
        connection = mysql.connector.connect(db_config)
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        return 'Database connection successful!'
    except mysql.connector.Error as e:
        return f'Database connection failed. Error: {str(e)}'
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/test-db-connection')
def test_db_connection():
    return test_db_connection()

if __name__ == '__main':
    app.run(debug=True)
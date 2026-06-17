import mysql.connector

def create_database():
    from config import Config
    if "localhost" not in Config.SQLALCHEMY_DATABASE_URI and "127.0.0.1" not in Config.SQLALCHEMY_DATABASE_URI:
        print("Production database detected. Skipping database creation script.")
        return

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tejasvi123"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS agrocare_db")
        print("Database 'agrocare_db' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()

if __name__ == "__main__":
    create_database()

import mysql.connector
from mysql.connector import Error

class DBMS_Connection:
    def __init__(self, host="localhost", user="root", password="", database="airline"):
        self.conn = None
        self.cursor = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(prepared=True)
            print(f"Connected to {self.database} database successfully.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def close_connection(self):
        try:
            if self.cursor and not getattr(self.cursor, '_closed', True):
                self.cursor.close()
            if self.conn and self.conn.is_connected():
                self.conn.close()
            print("Database connection closed.")
        except Error as e:
            print(f"Error closing connection: {e}")

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.close_connection()

    def reconnect(self):
        if not self.conn or not self.conn.is_connected():
            print("Connection lost. Reconnecting...")
            self.close_connection()
            self.connect()

    def execute_query(self, query, params=None):
        try:
            self.reconnect()
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except Error as e:
            print(f"Database query failed: {e}")
            return False

    def fetch_query(self, query, params=None):
        try:
            self.reconnect()
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Database fetch failed: {e}")
            return None

    def get_flight_details(self, plan_id):
        query = "SELECT name, departure, destination, time, landing_time, general, business FROM plan WHERE id = %s"
        self.cursor.execute(query, (plan_id,))
        return self.cursor.fetchone()
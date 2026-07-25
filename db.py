import sqlite3
from datetime import datetime 

DB_NAME = "lister.db"

class Database: 
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT  NULL, 
            descriptions TEXT NOT NULL, 
            time TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_item(self, title, descriptions):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO lists (title, descriptions, time)
        VALUES (?, ?, ?)
        """
        self.conn.execute(query, (title, descriptions, time_now))
        self.conn.commit()

    def get_all_items(self):
        query = """
        SELECT * 
        FROM lists
        ORDER BY id DESC
        """
        return self.conn.execute(query).fetchall()

    def delete_all_items(self):
        query = """
        DELETE FROM lists
        """
        self.conn.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()
import sqlite3

# connects directly to the database
def get_db_connection():
    conn = sqlite3.connect("database.db")
      # Makes rows in database behave like dictionaries
    conn.row_factory = sqlite3.Row
    return conn
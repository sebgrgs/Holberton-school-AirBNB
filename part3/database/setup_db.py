import sqlite3
import os

def execute_sql_file(cursor, filename):
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)

def setup_database():
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect('development.db')
    cursor = conn.cursor()
    
    try:
        # Execute schema creation
        execute_sql_file(cursor, 'schema.sql')
        
        # Execute initial data insertion
        execute_sql_file(cursor, 'initial_data.sql')
        
        # Commit changes
        conn.commit()
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
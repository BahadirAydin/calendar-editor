import sqlite3
import sys

def print_table_description(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    if not columns:
        print(f"Table {table_name} does not exist.")
        return False
    print(f"\nDescription of table '{table_name}':")
    for col in columns:
        print(f"Column: {col[1]}, Type: {col[2]}")
    return True

def print_table_contents(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    if not rows:
        print(f"Table {table_name} is empty.")
        return
    print(f"\nContents of table '{table_name}':")
    for row in rows:
        print(row)

def print_all_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        if print_table_description(cursor, table[0]):
            print_table_contents(cursor, table[0])

def main():
    database = "project.sql3"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    if len(sys.argv) > 1:
        table_name = sys.argv[1]
        if print_table_description(cursor, table_name):
            print_table_contents(cursor, table_name)
    else:
        print_all_tables(cursor)

    conn.close()

if __name__ == "__main__":
    main()

import sqlite3
import argparse

def delete_rows(db_path, table_name=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if table_name:
            print(f"Deleting rows in table: {table_name}")
            cursor.execute(f"DELETE FROM {table_name}")
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                print(f"Deleting rows in table: {table[0]}")
                cursor.execute(f"DELETE FROM {table[0]}")

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete rows from a SQLite table")
    parser.add_argument('--db', required=True, help='Path to SQLite database file')
    parser.add_argument('--table', help='Name of the table to delete rows from (optional)')
    args = parser.parse_args()

    delete_rows(args.db, args.table)

import sqlite3 as lite


def main():
    conn = lite.connect('E-App.db')
    conn.cursor()

    f = open('db_schema.sql', 'r')
    schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

import config
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return e


def migration():
    create_tables = {
        'create_user_table': """
        CREATE TABLE IF NOT EXISTS user (
        id integer PRIMARY KEY,
        tg_code text NOT NULL,
        name text NOT NULL,
        register_at date,
        time_zone text
    );""",
        'create_med_table': """
        CREATE TABLE IF NOT EXISTS med (
        id integer PRIMARY KEY,
        name text NOT NULL,
        value_in_full FLOAT NOT NULL,
        valid_before date
    );""",
        'create_aid_kit_table': """
            CREATE TABLE IF NOT EXISTS aid_kit (
            id integer PRIMARY KEY,
            med_id REFERENCES med(id),
            user_id REFERENCES user(id),
            value_now FLOAT NOT NULL
        );""",
        'create_duration_table': """
            CREATE TABLE IF NOT EXISTS duration (
            id integer PRIMARY KEY,
            start_date date NOT NULL,
            end_date date NOT NULL
        );""",
        'create_period_table': """
            CREATE TABLE IF NOT EXISTS period (
            id integer PRIMARY KEY,
            name text NOT NULL,
            per text NOT NULL
        );""",
        'create_med_in_use_table': """
            CREATE TABLE IF NOT EXISTS med_in_use (
            id integer PRIMARY KEY,
            aid_kit_id REFERENCES aid_kit(id),
            duration_id REFERENCES duration(id),
            period_id REFERENCES period(id),                
            period_val integer NOT NULL,
            med_per_use FLOAT NOT NULL
        );""",
    }
    try:
        connect = create_connection(config.db)
        c = connect.cursor()
        for sql in create_tables:
            c.execute(create_tables[sql])
    except Error as e:
        print(e)

#TODO вынести в классы

def existor(table, statement, value):
    sql = """
    SELECT COUNT(%s)
    FROM %s WHERE %s = "%s";
    """ % (statement, table, statement, value)
    print(sql)
    count = []
    try:
        result = executor(sql)[0]
        if result is not None:
            for row in result:
                count += row
            if count[0]:
                return False
            else:
                return True
        else:
            return False
    except Error as e:
        print(e)
        return True


def executor(code):
    connection = create_connection(config.db)
    cursor = connection.cursor()
    cursor.execute(code)
    last_id = cursor.lastrowid
    rows = cursor.fetchall()
    connection.commit()
    return [rows, last_id]


if __name__ == '__main__':
    migration()

from db_engine import *


#create table decorator
def create_tables(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for sql in query():
                cur.execute(sql)
            conn.commit()
            msg = cur.statusmessage
            print msg
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                print('Database connection ended.')
    return connect_run_close


#table query
@create_tables
def create_db():
    query = ["""
        CREATE TABLE budget(
            budget_id SERIAL PRIMARY KEY NOT NULL,
            budget_title VARCHAR(100) NOT NULL,
            budget_total INTEGER NOT NULL
        )
    ""","""
        CREATE TABLE expenses(
            budget_id INTEGER PRIMARY KEY,
            expense_title VARCHAR(200) NOT NULL,
            expense_cost INTEGER NOT NULL,
            FOREIGN KEY (budget_id)
            REFERENCES budget (budget_id)
        )
    """]
    return query

create_db()
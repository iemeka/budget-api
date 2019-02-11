import psycopg2
import functools
from db_helper.config import *


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
            #print msg
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection ended.')
    return connect_run_close


#table query
@create_tables
def create_tables():
    query = ["""
            CREATE TABLE budget(
            budget_id SERIAL PRIMARY KEY,
            budget_title VARCHAR(100) NOT NULL
            )
    ""","""
            CREATE TABLE expenses(
            budget_id INTEGER REFERENCES budget
            ON UPDATE CASCADE
            ON DELETE CASCADE
            NOT NULL,
            expense_title VARCHAR(200) NOT NULL,
            expense_cost INTEGER NOT NULL,
            expense_id SERIAL PRIMARY KEY
            )
            """]
    return query


# ------- test database setup -----------------

def create_test_tables(query):
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
            #print msg
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection ended.')
    return connect_run_close

#drop table
@create_test_tables
def drop_tables():
    query = ["""
    DROP TABLE budget CASCADE
    ""","""
    DROP TABLE expenses
    """]
    return query


#table query
@create_test_tables
def make_tables():
    query = ["""
            CREATE TABLE budget(
            budget_id SERIAL PRIMARY KEY,
            budget_title VARCHAR(100) NOT NULL
            )
    ""","""
            CREATE TABLE expenses(
            budget_id INTEGER REFERENCES budget
            ON UPDATE CASCADE
            ON DELETE CASCADE
            NOT NULL,
            expense_title VARCHAR(200) NOT NULL,
            expense_cost INTEGER NOT NULL,
            expense_id SERIAL PRIMARY KEY
            )
            ""","""
            INSERT INTO budget (budget_title) VALUES('january') RETURNING budget_id
            ""","""
            INSERT INTO budget (budget_title) VALUES('febuary') RETURNING budget_id
            ""","""
            INSERT INTO budget (budget_title) VALUES('march') RETURNING budget_id
            ""","""
            INSERT INTO expenses(budget_id,expense_title,expense_cost)
            VALUES(1,'first',10000) RETURNING expense_id;
            ""","""
            INSERT INTO expenses(budget_id,expense_title,expense_cost)
            VALUES(2,'second',20000) RETURNING expense_id;
            """
            ]
    return query





if __name__ == '__main__':
    create_tables()
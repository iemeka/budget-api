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
            CREATE TABLE user_info(
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            pw_hash VARCHAR(300) NOT NULL
            )
    ""","""
            CREATE TABLE budget(
            budget_id SERIAL PRIMARY KEY,
            budget_title VARCHAR(100) NOT NULL,
            user_id INTEGER REFERENCES user_info
            ON UPDATE CASCADE
            ON DELETE CASCADE
            NOT NULL
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
    DROP TABLE user_info CASCADE
    ""","""
    DROP TABLE budget CASCADE
    ""","""
    DROP TABLE expenses
    """]
    return query


@create_test_tables
def add_fixtures():
    query = ["""
            INSERT INTO budget (budget_title,user_id) VALUES('january',1) RETURNING budget_id
            ""","""
            INSERT INTO budget (budget_title,user_id) VALUES('febuary',1) RETURNING budget_id
            ""","""
            INSERT INTO budget (budget_title,user_id) VALUES('march',1) RETURNING budget_id
            ""","""
            INSERT INTO expenses(budget_id,expense_title,expense_cost)
            VALUES(1,'first',10000) RETURNING expense_id;
            ""","""
            INSERT INTO expenses(budget_id,expense_title,expense_cost)
            VALUES(2,'second',20000) RETURNING expense_id;
            """]
    return query

####------test queries



if __name__ == '__main__':
    create_tables()
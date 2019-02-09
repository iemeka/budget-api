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
            user_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password_hash VARCHAR(300) NOT NULL
            )
    """,]
    return query
    #userid on budget is functionally dependent on userid

if __name__ == '__main__':
    create_tables()
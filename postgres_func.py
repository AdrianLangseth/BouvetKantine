import psycopg2
from psycopg2 import sql

from user_secrets import HOST_ADDRESS, POSTGRES_PASSWORD, POSTGRES_USERNAME


# Database connection parameters


class Postgres:

    def __init__(self) -> None:
        self.db_params = {
                            'host': HOST_ADDRESS,
                            'port': '5432',
                            'database': 'tsdb',
                            'user': POSTGRES_USERNAME,
                            'password': POSTGRES_PASSWORD
                        }
        
        self.conn = psycopg2.connect(**self.db_params)
        self.cursor = self.conn.cursor()
        self.errors = 0

    def insert_data(self, data_to_insert, query):
        try:
            
            if self.cursor.closed:
                self.cursor = self.conn.cursor()

            # Define the SQL query to insert data into the hypertable
            insert_query = sql.SQL(query)
            
            # Loop through the data and insert each row
            for row in data_to_insert:
                self.cursor.execute(insert_query, row)
            
            # Commit the changes to the database
            self.conn.commit()
            
            # Close the cursor and the connection
            self.cursor.close()


        except psycopg2.Error as e:
            print(f"Error: {e}")
            self.errors += 1
            if self.errors > 10:
                AssertionError("Too many errors")

    def insert_data_passings(self, data_to_insert):

            # Define the SQL query to insert data into the hypertable
            query = """
                INSERT INTO passings (time, direction, sensor_name, last_5min_sum)
                VALUES (%s, %s, %s, %s)
            """
                
            self.insert_data(data_to_insert, query)
            
    def insert_data_passings_5min(self, data_to_insert):

            # Define the SQL query to insert data into the hypertable
            query = """
                INSERT INTO passings_5min (time, direction, sensor_name, visits)
                VALUES (%s, %s, %s, %s)
            """
            
            self.insert_data(data_to_insert, query)


    def create_cursor(self):
        return self.conn.cursor()
    
    def close_cursor(self):
        self.cursor.close()

    def close_connection(self):
        self.conn.close()

    def __del__(self):
        self.close_cursor()
        self.close_connection()
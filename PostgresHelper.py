import psycopg2
class PostgresHelper:
    def __init__(self, database_name):
        self.conn = psycopg2.connect(
            host="localhost",
            database=database_name,
            user="postgres",
            password="admin")
        self.conn.autocommit = True

    def get_all_data_in_table(self, table_name, attribute_list):
        cursor = self.conn.cursor()
        attributes = ",".join(attribute_list)
        cursor.execute(f"SELECT {attributes} from {table_name}")
        return cursor.fetchall()

    def update_one_row(self, table_name, id, id_attribute_name, change_attribute_value, change_attribute_name):
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE {table_name} set {change_attribute_name} = {change_attribute_value} where {id_attribute_name} = {id}")
        self.conn.commit()

    def insert_one_row(self, table_name, id, name, surname, age, gender, occupation):
        cursor = self.conn.cursor()
        cursor.execute(f'''INSERT INTO {table_name} (\"id\", \"name\", \"surname\", \"age\", \"gender\", \"occupation\") VALUES '''
                       f'''('{id}', '{name}', '{surname}', '{age}', '{gender}', '{occupation}');''')
        self.conn.commit()

    def create_table(self, table_name, attribute_dic):
        cursor = self.conn.cursor()
        keys = list(attribute_dic.keys())
        values = list(attribute_dic.values())
        attributes = ""
        for i in range(len(keys)):
            if i == 0:
                attributes += keys[i] + "   " + values[i] + "   " + "PRIMARY KEY,"
                continue
            if i == len(keys) - 1:
                attributes += keys[i] + "   " + values[i]
                continue
            attributes += keys[i] + "   " + values[i] + ","
        cursor.execute(f'''CREATE TABLE {table_name} ({attributes});''')
        self.conn.commit()
        #print("Create Table Successfully")

    def create_database(self, database):
        cursor = self.conn.cursor()
        cursor.execute(
            f"CREATE DATABASE {database};")
        self.conn.commit()

    def delete_database(self, database):
        cursor = self.conn.cursor()
        cursor.execute(
            f"DROP DATABASE {database};")
        self.conn.commit()

    def check_existence_of_database(self, database):
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT datname FROM pg_catalog.pg_database WHERE datname={database}")
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def close(self):
        self.conn.close()
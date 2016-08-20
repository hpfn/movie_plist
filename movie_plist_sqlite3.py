import sqlite3
import sys


# http://stackoverflow.com/questions/21360271/pythons-sqlite3-module-exceptions-where-is-the-documentation
# https://www.python.org/dev/peps/pep-0249/#exceptions
# http://pythoncentral.io/introduction-to-sqlite-in-python/
# http://zetcode.com/db/sqlitepythontutorial/
class DataStorage:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('movie_plist_sqlite3.db')
            self.c = self.conn.cursor()
            self.c.execute('''create table if not exists movie_plist (url UNIQUE,
                           title_year TEXT, director, writers_list, actors_list,
                           snps_txt TEXT, path, moviefile, watch INTEGER)''')
            self.conn.commit()
        except sqlite3.Error as err:
            if self.conn:
                self.conn.rollback()
            raise err
            sys.exit(1)

    def insert_data(self, data_s):
        """ data_s will have seven itens """
        try:
            with self.conn:
                self.conn.execute('insert into movie_plist values (?,?,?,?,?,?,?,?,?)', data_s)
                self.conn.commit()
        except sqlite3.IntegrityError:
            if self.conn:
                self.conn.rollback()
            print("Record already exists")

    def show_data(self):
        self.c.execute('select * from movie_plist')
        return list(self.c.fetchall())

    def check_movie(self):
        self.c.execute('select url from movie_plist')
        return str(self.c.fetchall())

    def exit_from_db(self):
        self.conn.close()

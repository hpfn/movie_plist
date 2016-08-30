import sqlite3
# import sys
import pimdbdata
import urllib.request


# http://stackoverflow.com/questions/21360271/pythons-sqlite3-module-exceptions-where-is-the-documentation
# https://www.python.org/dev/peps/pep-0249/#exceptions
# http://pythoncentral.io/introduction-to-sqlite-in-python/
# http://zetcode.com/db/sqlitepythontutorial/
class DataStorage:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('./info_in_db/movie_plist_sqlite3.db')
            self.c = self.conn.cursor()
            self.c.execute('''create table if not exists movie_plist (url UNIQUE,
                           title_year TEXT, director, writers_list, actors_list,
                           snps_txt TEXT, path, moviefile, watch INTEGER)''')
            self.conn.commit()
        except sqlite3.Error as err:
            if self.conn:
                self.conn.rollback()
            raise err

    def insert_data(self, url, path, moviefile):
        """ data does not exist in database """
        try:
            with self.conn:
                html = urllib.request.urlopen(url).read()
                movie = pimdbdata.ParseImdbData(html)
                m_data = [url, movie.title_year(), movie.director(), ' '.join(movie.creator_writers()),
                          ' '.join(movie.actors()), movie.synopsis(), path, moviefile, 0]
                self.conn.execute('insert into movie_plist values (?,?,?,?,?,?,?,?,?)', m_data)
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

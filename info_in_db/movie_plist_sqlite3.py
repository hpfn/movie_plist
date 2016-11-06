import sqlite3
import urllib.request

from data import pimdbdata


# http://stackoverflow.com/questions/21360271/pythons-sqlite3-module-exceptions-where-is-the-documentation
# https://www.python.org/dev/peps/pep-0249/#exceptions
# http://pythoncentral.io/introduction-to-sqlite-in-python/
# http://zetcode.com/db/sqlitepythontutorial/
class DataStorage(object):
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
        """
            data does not exist in database
            return the data inserted to .html file. This
            avoid query the db more than needed
         """
        try:
            with self.conn:
                html = urllib.request.urlopen(url).read()
                movie = pimdbdata.ParseImdbData(html)
                m_data = [url, movie.title_year(), movie.director(), ' '.join(movie.creator_writers()),
                          ' '.join(movie.actors()), movie.synopsis(), path, moviefile, 0]
                self.conn.execute('insert into movie_plist values (?,?,?,?,?,?,?,?,?)', m_data)
                self.conn.commit()
                return m_data
        except sqlite3.IntegrityError:
            if self.conn:
                self.conn.rollback()
            print("Record already exists")

    def show_data(self):
        self.c.execute('select * from movie_plist')
        return self.c.fetchall()
        #return list(self.c.fetchall())

    def movie_list_title(self):
        self.c.execute('select title_year from movie_plist')
        return self.c.fetchall()
        # return list(self.c.fetchall())

    def movie_seen(self):
        self.c.execute('select title_year from movie_plist where watch="1"')
        return  self.c.fetchall()

    def movie_to_watchagain(self, title):
        print(type(title))
        self.c.execute('select path, moviefile from movie_plist where title_year=? ', (title,))
        return self.c.fetchone()

    def no_movie_yet(self):
        self.c.execute('select title_year from movie_plist where moviefile="No_movie_file_yet"')
        return self.c.fetchall()
        # return list(self.c.fetchall())

    def check_movie(self):
        self.c.execute("select url from movie_plist")  # where url=?", url)
        return str(self.c.fetchall())

    def exit_from_db(self):
        self.conn.close()

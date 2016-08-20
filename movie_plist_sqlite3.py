import sqlite3

# http://stackoverflow.com/questions/21360271/pythons-sqlite3-module-exceptions-where-is-the-documentation
class DataStorage:
    def __init__(self):
        self.conn = sqlite3.connect('movie_plist_sqlite3.db')
        self.c = self.conn.cursor()
        self.c.execute('''create table if not exists movie_plist (url UNIQUE,
                        title_year TEXT, director, writers_list, actors_list,
                        snps_txt TEXT, path, moviefile, watch INTEGER)''')
        self.conn.commit()

    def insert_data(self, data_s):
        """ data_s will have seven itens """
        self.c.execute('insert into movie_plist values (?,?,?,?,?,?,?,?,?)', data_s)
        self.conn.commit()

    def show_data(self):
        self.c.execute('select * from movie_plist')
        return list(self.c.fetchall())

    def check_movie(self):
        self.c.execute('select url from movie_plist')
        return str(self.c.fetchall())

    def exit_from_db(self):
        self.conn.close()

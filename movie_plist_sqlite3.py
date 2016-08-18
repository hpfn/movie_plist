import sqlite3
import os

class DataStorage:
    def __init__(self):
        self.conn = sqlite3.connect('movie_plist_sqlite3.db')
        self.c = self.conn.cursor()

        if os.path.getsize('movie_plist_sqlite3.db') is 0:
            print("zero size. building a .db file")
            self.c.execute('''create table movie_plist (url UNIQUE,
                           title_year TEXT, director,
                           writers_list, actors_list,
                           snps_txt TEXT, watch INTEGER)''')
            self.conn.commit()


    def insert_data(self, data_s):
        """ data_s will have seven itens """
        self.c.execute('insert into movie_plist values (?,?,?,?,?,?,?)', data_s) #[0], data_s[1], data_s[2],
                                                                          #data_s[3], data_s[4], data_s[5],
                                                                          #data_s[6]))
        self.conn.commit()

    def show_data(self):
        self.c.execute('select * from movie_plist')
        for row in self.c.fetchall():
            print(row)

    def check_movie(self):
        self.c.execute('select url from movie_plist')
        #movie_list = list()
        # for chck in self.c.fetchall():
        #    print(chck)
        return str(self.c.fetchall())




    def exit_from_db(self):
        self.c.close()
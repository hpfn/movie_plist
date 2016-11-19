from .combo_box_build import Combo

class InteractBox(Combo):
    """ remove item and update combo box list """
    def __init__(self, index_number, movie_choice):
        self.index = index_number
        self.movie_selected = movie_choice
        self.stored_data = DataStorage()

    def insert_movie_file_action(self):
        """
            use self.index to update combo box list
            recreate the .html file with a new movie file
            reload the page
        """
        p_file = self.stored_data.movie_path(self.movie_selected)
        # scan selected movie dir
        scan_dir = PyScan(p_file[0])
        scan_dir = scan_dir.dir_to_scan()
        # file name
        file_n = scan_dir[0][2]
        self.stored_data.update_movie_file(file_n, self.movie_selected)
        # update list
        self.removeItem(self.index)
        # Regrex edit .html file ? re-create by now. First get the movies
        # then rm the html file and re-create.
        # This can be better
        unseen_movies = self.stored_data.movie_unseen()
        html_f = self.path_html
        call(['/bin/rm', html_f])
        html_file.create_page.generate_html(self.path_html, unseen_movies)
        self.browser_reload.reload()

    def movie_remove(self):
        """
            remove a movie on combo box list
            and  on db.
            from the hd too ?
        """
        db_seen_movie = self.stored_data.movie_select_one(self.movie_selected, '0')
        if db_seen_movie:
            self.removeItem(self.index)
            count = self.up_date.insert_movie_file_list.index(self.movie_selected)
            self.up_date.insert_movie_file_list.remove(self.movie_selected)
            self.up_date.removeItem(count)
            print("{} must be removed from the .html file and db".format(self.movie_selected))
        else:
            self.removeItem(self.index)
            count = self.watch_again.watch_again_list.index(self.movie_selected)
        self.watch_again.watch_again_list.remove(self.movie_selected)
        self.watch_again.removeItem(count)
        print("{} must be removed from db".format(self.movie_selected))

    def watch_movie(self):
        """
            call vlc to watch a movie
        """
        path = self.stored_data.movie_to_watchagain(self.movie_selected)
        to_watch = str(path[0]) + '/' + str(path[1])
        call(['/usr/bin/vlc', to_watch])


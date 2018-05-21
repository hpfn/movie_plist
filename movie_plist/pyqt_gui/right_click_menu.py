from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox


class RightClickMenu:
    def __init__(self, current_dict, qt_list, m_seen, m_unseen):
        self.current_item = qt_list.currentItem().text()
        # self.current_list = current_list
        self.current_dict = current_dict
        self.url = current_dict[self.current_item][0]
        self.qt_list = qt_list
        self.s_list = m_seen
        self.us_list = m_unseen
        # self.stored_data = DataStorage()
        self.menu = QMenu()

        self.right_click()

    def right_click(self):
        m_seen_action = QAction('Mark as Seen', self.menu)
        # unseenAction.setShortcut()
        m_seen_action.setStatusTip('Mark as Seen')
        m_seen_action.triggered.connect(self.m_seen_movies)

        m_rm_action = QAction('Remove from movie_plist', self.menu)
        # unseenAction.setShortcut()
        m_rm_action.setStatusTip('Remove from movie_plist')
        m_rm_action.triggered.connect(self.m_rm_from_db)

        self.menu.addAction(m_seen_action)
        self.menu.addAction(m_rm_action)

        self.menu.exec_(QCursor.pos())

    def m_seen_movies(self):
        """
        mark a movie as seen.
        check unseen list and seen list
        check on db if it is already a seen movie
        """

        # if self.stored_data.movie_isregistered(self.url):
        #    pass
        # else:
        # us_list_set = set(self.us_list)
        if self.current_item in self.us_list:
            title_year = self.current_item
            # self.current_list.remove(title_year)
            self.qt_list.takeItem(self.qt_list.currentRow())
            self.s_list[title_year] = self.us_list[title_year]
            del self.us_list[title_year]
            # self.stored_data.insert_data(self.url)

        # self.stored_data.exit_from_db()

    def m_rm_from_db(self):
        """
        remove from current list and from db
        the user remove from HD
        """

        # if self.stored_data.movie_isregistered(self.url):
        # if self.current_item not in self.us_list:
        #    self.stored_data.movie_delete(self.url)
        # self.stored_data.exit_from_db()

        title_year = self.current_item
        # self.current_list.remove(title_year)
        self.qt_list.takeItem(self.qt_list.currentRow())
        # if self.us_list.get(title_year):
        #    del self.us_list[title_year]
        # else:
        #    del self.s_list[title_year]
        del self.current_dict[title_year]

        msg = QMessageBox()
        msg.setText(title_year + " removed from movie_plist.\n\n"
                                 "Remove from HD yourself.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

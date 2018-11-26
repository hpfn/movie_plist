#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

from PyQt5.QtWidgets import QAction, QMainWindow  # pylint: disable-msg=E0611

from movie_plist.conf.global_conf import MOVIE_SEEN, MOVIE_UNSEEN

from . import splitter


class Window(QMainWindow):
    def __init__(self):  # , m_seen, m_unseen):  # m_seen, m_unseen):
        super().__init__()
        self.two_lines = splitter.TwoLines()
        # self.seen_list = MOVIE_SEEN
        # self.unseen_list = MOVIE_UNSEEN

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.two_lines)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        # exit_action.setStatusTip('Exit app')
        exit_action.triggered.connect(self.close)

        unseen_action = QAction('Unseen', self)
        # unseenAction.setShortcut()
        # unseen_action.setStatusTip('Unseen movies: ' + count_unseen)
        unseen_action.triggered.connect(self.unseenmovies)

        seen_action = QAction('Seen', self)
        # unseenAction.setShortcut()
        # seen_action.setStatusTip('Seen movies: ' + count_seen)
        seen_action.triggered.connect(self.seenmovies)

        # self.statusBar().showMessage('Unseen: ' + count_unseen + ' | Seen: ' + count_seen)
        self.update_statusbar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_action)
        toolbar.addAction(unseen_action)
        toolbar.addAction(seen_action)

        self.setGeometry(100, 100, 800, 650)
        self.setWindowTitle('movie_plist')
        self.show()

    def unseenmovies(self):
        # botão 'unseen'
        self.two_lines.top.clear()
        self.two_lines.current_dict = MOVIE_UNSEEN
        self.two_lines.top.addItems(sorted(MOVIE_UNSEEN.keys()))
        self.two_lines.top.setCurrentRow(0)
        self.update_statusbar()

    def seenmovies(self):
        # botão 'seen'
        if MOVIE_SEEN:
            self.two_lines.top.clear()
            self.two_lines.current_dict = MOVIE_SEEN
            self.two_lines.top.addItems(sorted(MOVIE_SEEN.keys()))
            self.two_lines.top.setCurrentRow(0)
            self.update_statusbar()

    def update_statusbar(self):
        self.statusBar().clearMessage()
        self.statusBar().showMessage('Unseen: ' + str(len(MOVIE_UNSEEN)) +
                                     ' | Seen: ' + str(len(MOVIE_SEEN)))

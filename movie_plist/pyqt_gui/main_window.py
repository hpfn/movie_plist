#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

from PyQt5.QtWidgets import QAction, QMainWindow

from . import splitter


class Window(QMainWindow):
    def __init__(self, m_seen, m_unseen):  # m_seen, m_unseen):
        super().__init__()
        self.two_lines = splitter.TwoLines(m_seen, m_unseen)
        self.seen_list = m_seen
        self.unseen_list = m_unseen

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
        self.two_lines.current_dict = self.unseen_list
        self.two_lines.top.addItems(sorted(self.unseen_list.keys()))
        self.two_lines.top.setCurrentRow(0)
        self.update_statusbar()

    def seenmovies(self):
        # botão 'seen'
        if self.seen_list:
            self.two_lines.top.clear()
            self.two_lines.current_dict = self.seen_list
            self.two_lines.top.addItems(sorted(self.seen_list.keys()))
            self.two_lines.top.setCurrentRow(0)
            self.update_statusbar()

    def update_statusbar(self):
        self.statusBar().clearMessage()
        self.statusBar().showMessage('Unseen: ' + str(len(self.unseen_list)) +
                                     ' | Seen: ' + str(len(self.seen_list)))

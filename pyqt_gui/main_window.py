#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

from PyQt5.QtWidgets import (QMainWindow, QAction)

# from PyQt5.QtCore import QIcon
from pyqt_gui import splitter


class Window(QMainWindow):
    def __init__(self, s_list, us_list, all_movies):  # m_seen, m_unseen):
        super().__init__()
        self.two_lines = splitter.TwoLines(s_list, us_list, all_movies)
        self.seen_list = s_list
        self.unseen_list = us_list
        # self.seen_dict = m_seen
        # self.unseen_dict = m_unseen

        self.init_ui()

    def init_ui(self):
        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)
        # self.two_lines = splitter.TwoLines()
        self.setCentralWidget(self.two_lines)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit app')
        exit_action.triggered.connect(self.close)

        count_unseen = str(len(self.unseen_list))
        unseen_action = QAction('Unseen', self)
        # unseenAction.setShortcut()
        unseen_action.setStatusTip('Unseen movies: ' + count_unseen)
        unseen_action.triggered.connect(self.unseenmovies)

        count_seen = str(len(self.seen_list))
        seen_action = QAction('Seen', self)
        # unseenAction.setShortcut()
        seen_action.setStatusTip('Seen movies: ' + count_seen)
        seen_action.triggered.connect(self.seenmovies)

        self.statusBar()

        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_action)
        toolbar.addAction(unseen_action)
        toolbar.addAction(seen_action)

        self.setGeometry(100, 100, 800, 650)
        self.setWindowTitle('Main Window')
        self.show()

    def unseenmovies(self):
        # botão 'unseen'
        self.two_lines.top.clear()
        self.two_lines.current_list = self.unseen_list
        self.two_lines.top.addItems(self.unseen_list)
        self.two_lines.top.setCurrentRow(0)
        # self.two_lines.current_dict = self.unseen_dict

    def seenmovies(self):
        # botão 'seen'
        if len(self.seen_list) > 0:
            self.two_lines.top.clear()
            self.two_lines.current_list = self.seen_list
            self.two_lines.top.addItems(self.seen_list)
            self.two_lines.top.setCurrentRow(0)
            # self.two_lines.current_dict = self.seen_dict

# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = Window()
#    sys.exit(app.exec_())

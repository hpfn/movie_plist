#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction)
# from PyQt5.QtCore import QIcon
import splitter


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.two_lines = splitter.TwoLines()

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

        unseen_action = QAction('Unseen', self)
        # unseenAction.setShortcut()
        unseen_action.setStatusTip('Unseen movies')
        unseen_action.triggered.connect(self.unseenmovies)

        seen_action = QAction('Seen', self)
        # unseenAction.setShortcut()
        seen_action.setStatusTip('Seen movies')
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
        self.two_lines.top.addItem('unseen')
        self.two_lines.top.setCurrentRow(0)

    def seenmovies(self):
        # botão 'seen'
        self.two_lines.top.clear()
        self.two_lines.top.addItem('already seen')
        self.two_lines.top.setCurrentRow(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

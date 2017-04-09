#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

# import sys
# import time
import urllib.request
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSplitter, QListWidget, QTabWidget, QFileSystemModel, QTreeView)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import urllib.request
from data import pimdbdata


class TwoLines(QWidget):
    def __init__(self, first_list, unseen_d):  # , unseen_d):
        super().__init__()
        self.top = QListWidget()
        self.first_list = first_list
        # self.seen_d = seen_d
        # self.unseen_d = unseen_d
        self. current_dict = unseen_d
        self.tabs = QTabWidget()
        # movie info
        self.tab_synopsys = QWidget()
        # ls dir
        self.tab_ls_dir = QWidget()
        # layout
        self.synopsys_vbox = QVBoxLayout()
        self.lsdir_vbox = QVBoxLayout()
        # movie info 
        self.bottom = QLabel()
        # ls content of the current dir
        self.lsdir = QFileSystemModel()
        self.tree = QTreeView()

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        # will be the scan result (unseen)
        # list_items = ['unseen 1', 'unseen 2', 'unseen 3']
        self.top.addItems(self.first_list)
        self.top.setCurrentRow(0)
        # self.top.itemClicked.connect(self.top.Clicked)
        # self.bottom.setText(self.top.currentItem().text())

        # TAB movie infor
        self.data_to_show()
        # TAB ls dir
        self.ls_current_dir()
        # TABS
        self.set_tabs()

        def changed_item():
            if self.top.currentItem():
                self.data_to_show()
                self.ls_current_dir()

        self.top.currentItemChanged.connect(changed_item)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.top)
        splitter1.addWidget(self.tabs)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    def set_tabs(self):
        """ 
        movie info on one tab
        ls dir on other tab
        """
        # tab one
        self.synopsys_vbox.addWidget(self.bottom)
        self.tab_synopsys.setLayout(self.synopsys_vbox)
        self.tabs.addTab(self.tab_synopsys, "Movie Info")
        # tab two
        self.lsdir_vbox.addWidget(self.tree)
        self.tab_ls_dir.setLayout(self.lsdir_vbox)
        self.tabs.addTab(self.tab_ls_dir, "ls dir")

    def data_to_show(self):
        """ get data from a dict or named_tupla """
        url = self.current_dict[self.top.currentItem().text()][0]
        html = urllib.request.urlopen(url).read()
        movie = pimdbdata.ParseImdbData(html)
        poster = movie.movie_poster()
        synopsis = movie.synopsis()
        # print(poster)
        # if no internet, commented
        img = QImage()  # (8,10,4)
        data = urllib.request.urlopen(poster).read()
        #        "https://images-na.ssl-images-amazon.com/images/M/MV5BMTc5Mzg3NjI4OF5BMl5BanBnXkFtZTgwNzA3Mzg4MDI@._V1_UX182_CR0,0,182,268_AL_.jpg").read()
        img.loadFromData(data)
        img.save('picture.png')
        texto = '<html><table><td><img src="picture.png"></td><td>' + synopsis + '</td></table></html>'
        self.bottom.setText(texto)

    def ls_current_dir(self):
        dir_to_path = self.current_dict[self.top.currentItem().text()][1]
        # dir_to_path = "/tmp"
        self.lsdir.setRootPath(dir_to_path)
        self.tree.setModel(self.lsdir)
        self.tree.setRootIndex(self.lsdir.index(dir_to_path))
        # self.tree.resizeColumnToContents(100)
        # self.tree.AdjustToContents = 2
        self.tree.setAnimated(True)
        self.tree.setIndentation(30)

    def on_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

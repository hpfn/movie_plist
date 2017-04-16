#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

from subprocess import call
# import sys
# import time
import urllib.request
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenu, QAction,
                             QSplitter, QListWidget, QTabWidget, QFileSystemModel, QTreeView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QImage
import urllib.request
from data import pimdbdata
from html_file.htmltags import HtmlTags
from info_in_db.movie_plist_sqlite3 import DataStorage


class TwoLines(QWidget):
    def __init__(self, s_list, us_list, all_movies):
        super().__init__()
        self.top = QListWidget()
        self.current_list = us_list
        self.us_list = us_list
        self.s_list = s_list
        # self.seen_d = seen_d
        # self.unseen_d = unseen_d
        self.current_dict = all_movies
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
        # ls content of the current dirQt.CustomContextMenu
        self.lsdir = QFileSystemModel()
        self.tree = QTreeView()

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        # will be the scan result (unseen)
        # list_items = ['unseen 1', 'unseen 2', 'unseen 3']
        self.top.addItems(self.current_list)
        self.top.setCurrentRow(0)
        self.top.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.top.itemClicked.connect(self.top.Clicked)
        # self.bottom.setText(self.top.currentItem().text())

        # TAB movie infor
        self.data_to_show()
        # TAB ls dir
        self.ls_current_dir()
        # TABS
        self.set_tabs()

        def right_click():
            menu = QMenu()

            m_seen_action = QAction('Mark as Seen', self)
            # unseenAction.setShortcut()
            m_seen_action.setStatusTip('Mark as Seen')
            m_seen_action.triggered.connect(self.m_seen_movies)

            m_rm_action = QAction('Remove from Database', self)
            # unseenAction.setShortcut()
            m_rm_action.setStatusTip('Remove from Database')
            m_rm_action.triggered.connect(self.m_rm_from_db)

            menu.addAction(m_seen_action)
            menu.addAction(m_rm_action)

            # posição do menu na tela
            menu.exec_(QCursor.pos())

        def clicked_movie():
            item = self.tree.selectedIndexes()[0]
            file_to_play = item.model().filePath(item)
            if file_to_play.endswith(('.avi', 'mp4', '.mkv')):
                call(['/usr/bin/mpv', file_to_play])

        def changed_item():
            if self.top.currentItem():
                self.data_to_show()
                self.ls_current_dir()

        self.top.currentItemChanged.connect(changed_item)
        self.top.customContextMenuRequested.connect(right_click)
        self.tree.doubleClicked.connect(clicked_movie)

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
        """ 
        call HtmlTags to build html with
        a poster and a synopsis and put
        the result on 'bottom'
        obs: must lines should go to HtmlTags
        """
        url = self.current_dict[self.top.currentItem().text()][0]
        html = urllib.request.urlopen(url).read()
        movie = pimdbdata.ParseImdbData(html)
        poster = movie.movie_poster()
        synopsis = movie.synopsis()
        img = QImage()  # (8,10,4)
        data = urllib.request.urlopen(poster).read()
        img.loadFromData(data)
        img.save('/tmp/picture.png')
        context = HtmlTags(url, synopsis)
        self.bottom.setText(context.context)

    def ls_current_dir(self):
        dir_to_path = self.current_dict[self.top.currentItem().text()][1]
        # dir_to_path = "/tmp"
        self.lsdir.setRootPath(dir_to_path)
        self.tree.setModel(self.lsdir)
        self.tree.setRootIndex(self.lsdir.index(dir_to_path))
        self.tree.setColumnWidth(0, 450)
        # self.tree.AdjustToContents = 2
        self.tree.setAnimated(True)
        self.tree.setIndentation(30)

    def m_seen_movies(self):
        """
        mark a movie as seen. 
        check unseen list and seen list
        check on db if it is already a seen movie
        """
        title_year = self.top.currentItem().text()
        url = self.current_dict[title_year][0]
        stored_data = DataStorage()
        if stored_data.movie_isregistered(url):
            pass
        else:
            item = self.top.currentItem().text()
            self.current_list.remove(item)
            self.top.takeItem(self.top.currentRow())
            self.s_list.append(item)
            stored_data.insert_data(url)
            #print('mark as seem {}' .format(self.top.currentItem().text()))

    def m_rm_from_db(self):
        """
        remove from current list and from db
        the user remove from HD
        """
        print('remove from db : {}' .format(self.top.currentItem().text()))

    def on_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
most from zetcode tutorial
"""

from subprocess import call

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileSystemModel, QHBoxLayout, QLabel, QListWidget, QSplitter, QTabWidget,
    QTreeView, QVBoxLayout, QWidget
)

from movie_plist.html_file.htmltags import HtmlTags
from movie_plist.pyqt_gui.right_click_menu import RightClickMenu


class TwoLines(QWidget):
    def __init__(self, m_seen, m_unseen):
        super().__init__()
        self.top = QListWidget()
        if len(m_unseen) < 1:
            self.current_dict = m_seen
            self.current_list = sorted(m_seen.keys())
        else:
            self.current_dict = m_unseen
            self.current_list = sorted(m_unseen.keys())

        self.us_list = m_unseen
        self.s_list = m_seen
        # self.current_dict = all_movies
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

        self.top.addItems(self.current_list)
        self.top.setCurrentRow(0)
        self.top.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.top.itemClicked.connect(self.top.Clicked)
        # self.bottom.setText(self.top.currentItem().text())

        # TAB movie info
        self.data_to_show()
        # TAB ls dir
        self.ls_current_dir()
        # TABS
        self.set_tabs()

        # must be here because of QBasicTimer red msg
        # QBasicTimer can only be used with threads started with QThread
        def changed_item():
            if self.top.currentItem():
                self.data_to_show()
                self.ls_current_dir()

        self.top.currentItemChanged.connect(changed_item)
        self.top.customContextMenuRequested.connect(self.right_click)
        self.tree.doubleClicked.connect(self.clicked_movie)

        # to choose a browser
        # self.labelOnlineHelp.linkActivated.connect(self.link_handler)
        self.bottom.setOpenExternalLinks(True)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.top)
        splitter1.addWidget(self.tabs)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    def set_tabs(self):
        """
        movie info on one tab
        ls dir on the other tab
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
        call HtmlTags to build html with a poster and a synopsis
        and put the result on self.bottom
        """
        title = self.top.currentItem().text()
        url = self.current_dict[title][0]
        # if url in 'bad url':
        #    self.bottom.setText('bad url')
        # else:
        context = HtmlTags(url, title)
        self.bottom.setText(context.context)

    def ls_current_dir(self):
        path_to_dir = self.current_dict[self.top.currentItem().text()][1]
        self.lsdir.setRootPath(path_to_dir)
        self.tree.setModel(self.lsdir)
        self.tree.setRootIndex(self.lsdir.index(path_to_dir))
        self.tree.setColumnWidth(0, 450)

    def right_click(self):
        RightClickMenu(self.current_dict, self.top,
                       self.s_list, self.us_list)

    def clicked_movie(self):
        item = self.tree.selectedIndexes()[0]
        file_to_play = item.model().filePath(item)
        if file_to_play.endswith(('.avi', 'mp4', '.mkv')):
            call(['/usr/bin/mpv', file_to_play])

    def on_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

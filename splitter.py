#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

# import sys
# import time
import urllib.request
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSplitter, QTabWidget, QListWidget, 
                             QFileSystemModel, QTreeView)
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# class MyListWidget(QListWidget):
#
#    def Clicked(self, item):
#        print(self.currentItem().text())
#        QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())


class TwoLines(QWidget):
    def __init__(self):
        super().__init__()
        self.top = QListWidget()
        self.bottom = QLabel()
        self.tabs = QTabWidget()

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        self.top.addItem("item 1")
        self.top.addItem("item 2")
        self.top.addItem("item 3")
        self.top.addItem("item 4")
        self.top.setCurrentRow(0)
        # self.top.itemClicked.connect(self.top.Clicked)

        # bottom = QFrame(self)
        # bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setText(self.top.currentItem().text())

        # ls dir 
        dir_path = '/tmp'
        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir_path))
        self.tree.setAnimated(True)
        self.tree.setIndentation(30)
        self.tree.setSortingEnabled(True)
        
        # TABS
        tab_synopsys = QWidget()
        tab_lsdir = QWidget()

        vbox_0 = QVBoxLayout()
        vbox_0.addWidget(self.bottom)
        tab_synopsys.setLayout(vbox_0)
        
        vbox_1 = QVBoxLayout()
        vbox_1.addWidget(self.tree)
        tab_lsdir.setLayout(vbox_1)

        self.tabs.addTab(tab_synopsys, "Info")
        self.tabs.addTab(tab_lsdir, "lst dir")

        def changed_item():
            if self.top.currentItem():
                img = QImage()  # (8,10,4)
                data = urllib.request.urlopen(
                    "https://images-na.ssl-images-amazon.com/images/M/MV5BMTc5Mzg3NjI4OF5BMl5BanBnXkFtZTgwNzA3Mzg4MDI@._V1_UX182_CR0,0,182,268_AL_.jpg").read()
                img.loadFromData(data)
                img.save('picture.png')
                texto = '<html><table><td><img src="picture.png"></td><td>' + self.top.currentItem().text() + '</td></table></html>'
                # self.bottom.setText(self.top.currentItem().text())
                # self.bottom.setOpenExternalLinks(True)
                self.bottom.setText(texto)
                # self.bottom.setPixmap(QPixmap(img))

        self.top.currentItemChanged.connect(changed_item)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.top)
        splitter1.addWidget(self.tabs)
        # splitter1.addWidget(self.bottom)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    #        self.setGeometry(300, 300, 300, 200)
    #        self.setWindowTitle('QSplitter')
    #        self.show()

    def on_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

# if __name__ == '__main__':
#
#    app = QApplication(sys.argv)
#    ex = TwoLines()
#    sys.exit(app.exec_())

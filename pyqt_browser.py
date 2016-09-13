#!/usr/bin/python3

"""
   this will be the first gui.
   only a browser.
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from subprocess import call
import sys


# from PyQt5 import QtCore


def call_vlc(link):
    # print(link)
    if 'No_movie_file_yet' not in link:
        call(['/usr/bin/vlc', link])
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('You do not have this movie file.')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        msg.exec_()


def qt_browser(path_to_file):
    app = QApplication(sys.argv)
    # scene = QGraphicsScene()
    # view = QGraphicsView()
    # grid = QGridLayout()
    browser = QWebView()  # QTextBrowser()
    browser.setContextMenuPolicy(Qt.ActionsContextMenu)  # quitAction
    # browser.setFixedSize(700, 600)
    # browser.setContent(mimeType='text/html')
    browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    browser.page().linkClicked.connect(lambda link: call_vlc(link.toString()))
    # browser.page().linkClicked.connect(call_vlc(link.toString()))

    # browser.page
    # browser.setSource(QUrl("pymovieinfo.html")
    url = "file://" + path_to_file + "/pymovieinfo.html"
    # browser.setUrl(QUrl.fromLocalFile(url))
    browser.setUrl(QUrl(url))
    browser.setWindowTitle('QWebView HTML File Input')
    browser.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#    main()

#!/usr/bin/python3

"""
   this will be the first gui.
   only a browser.
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *


def main():
    app = QApplication(sys.argv)
    # scene = QGraphicsScene()
    # view = QGraphicsView()
    # grid = QGridLayout()
    browser = QWebView()  # QTextBrowser()

    browser.setFixedSize(700, 600)
    # browser.setContent(mimeType='text/html')
    browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    # browser.page
    # browser.setSource(QUrl("pymovieinfo.html"))
    browser.setUrl(QUrl.fromLocalFile('/home/zaza/Documentos/Programacao/python/ret_movie_info/pymovieinfo.html'))
    browser.setWindowTitle('QTextBrowser HTML File Input')
    browser.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

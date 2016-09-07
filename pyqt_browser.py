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
from subprocess import call

def call_vlc():
    call('/usr/bin/vlc')


def qt_browser(path_to_file):
    app = QApplication(sys.argv)
    # scene = QGraphicsScene()
    # view = QGraphicsView()
    # grid = QGridLayout()
    browser = QWebView()  # QTextBrowser()
    browser.setContextMenuPolicy(Qt.ActionsContextMenu)
    quitAction = QAction("VLC", None)
    quitAction.triggered.connect(call_vlc)  # funcionando !!!
    # funciona quitAction.triggered.connect(qApp.quit)
    browser.addAction(quitAction)
#    browser.setContextMenuPolicy(Qt.CustomContextMenu)
#    browser.customContextMenuRequested.connect(openMenu)

    # browser.setFixedSize(700, 600)
    # browser.setContent(mimeType='text/html')
    browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

    browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)

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

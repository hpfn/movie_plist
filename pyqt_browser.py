#!/usr/bin/python3

"""
   this will be the first gui.
   only a browser.
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
# from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from subprocess import call
# from PyQt5 import QtCore


def call_vlc(link):
    call(['/usr/bin/vlc', link])


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
    browser.page().linkClicked.connect(lambda link: call(['/usr/bin/vlc', link.toString()]))  # call_vlc(link.toString()))

    # browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)
    # QT4 - QtCore.QObject.connect(browser, QtCore.SIGNAL("linkClicked (const QUrl&)"), call_vlc)

    # browser.linkClicked(const QUrl &)
    # quitAction = QAction("VLC", None)
    # quitAction.triggered.connect(call_vlc)  # funcionando !!!
    # funciona quitAction.triggered.connect(qApp.quit)
    # browser.addAction(quitAction)

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

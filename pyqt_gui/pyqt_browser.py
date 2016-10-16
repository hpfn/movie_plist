#!/usr/bin/python3

"""
   It will be a class for web browser.
"""
import sys
from subprocess import call
# from PyQt5.QtGui import
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox


#class Browser(object):
#    def __init__(self):
#        super().__init__()
#        # self.scan_dir_final = scan_dir
#
#        #self.qt_browser()

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

def qt_browser(scan_dir):
    app = QApplication(sys.argv)
    # scene = QGraphicsScene()
    # view = QGraphicsView()
    # grid = QGridLayout()

    browser = QWebView()  # QTextBrowser()
    # browser.setContextMenuPolicy(Qt.ActionsContextMenu)  # quitAction
    # browser.setFixedSize(700, 600)
    # browser.setContent(mimeType='text/html')
    browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    browser.page().linkClicked.connect(lambda link: self.call_vlc(link.toString()))
    # browser.page().linkClicked.connect(call_vlc(link.toString()))

    # browser.setSource(QUrl("pymovieinfo.html")
    url = "file://" + scan_dir + "/pymovieinfo.html"
    # browser.setUrl(QUrl.fromLocalFile(url))
    browser.setUrl(QUrl(url))
    # browser.setWindowTitle('QWebView HTML File Input')
    #browser.show()
    #sys.exit(app.exec_())


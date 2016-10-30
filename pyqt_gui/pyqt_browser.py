#!/usr/bin/python3

"""
   It will be a class for web browser.
   I do not know how to do it yet. So
   I call QWebView by qt_browser function
   and return the object
"""

from subprocess import call
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QMessageBox


# class Browser(QWebView):
#    def __init__(self, scan_dir):
#        super().__init__()
#        self.browser = QWebView()
#        self.scan_dir_final = scan_dir
#
#        self.qt_browser()

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


def qt_browser(path):
    browser = QWebView()
    browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    browser.page().linkClicked.connect(lambda link: call_vlc(link.toString()))
    url = "file://" + path + "/pymovieinfo.html"
    browser.setUrl(QUrl(url))
    return browser
#!/usr/bin/python3
# -*-coding-utf8-*
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
import conf.global_conf

def call_vlc(link):
    # print(link)
    if 'No_movie_file_yet' not in link:
        # ugly fix to remove the
        # http://localhost:8080 part
        # of the 'link'. cgi fault
        call(['/usr/bin/vlc', link[21:]])
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('You do not have this movie file.')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()


def qt_browser(path_html):
    browser = QWebView()
    browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    browser.page().linkClicked.connect(lambda link: call_vlc(link.toString()))
    # url = "file://" + path_html
    url = 'http://localhost:' + str(conf.global_conf.PORT)
    browser.setUrl(QUrl(url))
    return browser

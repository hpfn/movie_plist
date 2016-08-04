#!/usr/bin/python3

"""
   this will be the first gui.
   only a browser.
"""
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import sys

def main():
    app = QApplication (sys.argv)
    #scene = QGraphicsScene()
    #view = QGraphicsView()
    #grid = QGridLayout()
    browser = QTextBrowser()

    browser.setFixedSize(200,100)
    browser.setSource(QUrl("teste.html"))
    browser.setWindowTitle("QTextBrowser HTML File Input")
    browser.show()

    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

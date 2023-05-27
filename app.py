import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import urllib.parse

class BrowserWindow(QMainWindow):
    def __init__(self):
        super(BrowserWindow, self).__init__()
        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 800, 600)

        self.webview = QWebEngineView()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.webview, "New Tab")
        self.tab_widget.tabBar().setExpanding(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.navigate_back)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #222222;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #555555;
            }
        """)

        self.forward_button = QPushButton("Forward") # Forward button that allows the user to navigate between webpages
        self.forward_button.clicked.connect(self.navigate_forward)
        self.forward_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #222222;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #555555;
            }
        """)

        self.home_button = QPushButton("Home") # Home button that allows the user to go back to the homepage
        self.home_button.clicked.connect(self.load_homepage)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #222222;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #555555;
            }
        """)

        self.refresh_button = QPushButton("Refresh") # Refreshes the page
        self.refresh_button.clicked.connect(self.refresh_page)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #222222;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #555555;
            }
        """)

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        """)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(self.back_button)
        self.toolbar.addWidget(self.forward_button)
        self.toolbar.addWidget(self.home_button)
        self.toolbar.addWidget(self.refresh_button)
        self.toolbar.addWidget(self.search_bar)

        self.statusbar = QStatusBar()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.statusbar)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.webview.loadFinished.connect(self.update_url_bar)
        self.webview.loadProgress.connect(self.update_progress)

        self.load_homepage()  # Load the homepage initially

    def load_url(self): # Uses google.com/search to open the search results
        text = self.search_bar.text()
        if "http://" in text or "https://" in text:
            url = text
        else:
            url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(text)
        self.webview.load(QUrl(url))

    def load_homepage(self): # Homepage, you can change the html howver you like!
        html_content = """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #F6F6F6;
                    margin: 0;
                }
                .homepage-container {
                    padding: 30px;
                    text-align: center;
                }
                h1 {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333333;
                }
                p {
                    font-size: 16px;
                    color: #666666;
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <div class="homepage-container">
                <h1>Welcome to My Homepage</h1>
                <p>This is a custom homepage created with Python and PyQt.</p>
                <p>You can modify the content and style according to your needs.</p>
            </div>
        </body>
        </html>
        """
        self.webview.setHtml(html_content)
        self.search_bar.clear()

    def navigate_back(self):
        self.webview.back()

    def navigate_forward(self):
        self.webview.forward()

    def refresh_page(self):
        self.webview.reload()

    def search(self):
        self.load_url()

    def update_url_bar(self):
        url = self.webview.url().toString()
        self.search_bar.setText(url)

    def update_progress(self, progress):
        self.statusbar.showMessage(f"Loading... {progress}%")

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def tab_changed(self, index):
        if index >= 0:
            self.webview = self.tab_widget.widget(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_()) 

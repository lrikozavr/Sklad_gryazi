from PySide6.QtGui import QAction
from PySide6.QtWidgets import ( QMainWindow, QToolBar, QListWidget, QListWidgetItem,
                               QPushButton, QMessageBox, QDialog, QFileDialog)

from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtCore import Qt, QSize, QFile, QDir, QTextStream, QStringConverter



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        toolBar = QToolBar()
        self.addToolBar(toolBar)
        fileMenu = self.menuBar().addMenu("&File")
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        fileMenu.addAction(loadAction)
        toolBar.addAction(loadAction)
        exitAction = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAct)
        self.axWidget = QAxWidget()
        self.setCentralWidget(self.axWidget)

        self.list = QListWidget()
        self.setCentralWidget(self.list)
        for i in range(10):
            item = QListWidgetItem(f"Item {i}")
            item.setTextAlignment(Qt.AlignCenter)
            self.list.addItem(item)
        
        #list.resize()

        #self.button = QPushButton("My Button", self)
        #self.button.clicked.connect(self.handleButton)
    
    def load(self):
        axSelect = QAxSelect(self)
        if axSelect.exec() == QDialog.Accepted:
            clsid = axSelect.clsid()
            if not self.axWidget.setControl(clsid):
                QMessageBox.warning(self, "AxViewer", f"Unable to load {clsid}.")
    
    def open(self):
        file_name = QFileDialog.getOpenFileName(self,
                "Open File", QDir.currentPath(),
                "Files (*.*)")[0]

        if not file_name:
            QMessageBox.warning(self, "File", f"File don't exist")
        
        in_file = QFile(file_name)
        if not in_file.open(QFile.ReadOnly | QFile.Text):
            reason = in_file.errorString()
            QMessageBox.warning(self, "DOM Bookmarks",
                    f"Cannot read file {file_name}:\n{reason}.")
            return
        
        for line in open(file_name):
            try:
                self.list.addItem(QListWidgetItem(line))
            except:
                print()

        
        #QStringConverter(QStringConverter.System)
        #line in_file.readLine()


    def handleButton(self):
        self.button.setText("Ready")


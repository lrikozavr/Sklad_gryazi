from PySide6.QtGui import (QAction, QCursor, QDesktopServices, QGuiApplication, QIcon,
                           QKeySequence, QShortcut, QStandardItem,
                           QStandardItemModel)
from PySide6.QtWidgets import (QMainWindow, QToolBar, QListWidget, QListWidgetItem,
                               QPushButton, QMessageBox, QFileDialog, QProgressBar,
                               QApplication, QCheckBox, QComboBox,
                               QCommandLinkButton, QDateTimeEdit, QDial,
                               QDialog, QDialogButtonBox, QFileSystemModel,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QListView, QMenu, QPlainTextEdit,
                               QProgressBar, QPushButton, QRadioButton,
                               QScrollBar, QSizePolicy, QSlider, QSpinBox,
                               QStyleFactory, QTableWidget, QTabWidget,
                               QTextBrowser, QTextEdit, QToolBox, QToolButton,
                               QTreeView, QVBoxLayout, QWidget)

from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtCore import Qt, QSize, QFile, QDir, QTextStream, QStringConverter, QTimer, Slot

def class_name(o):
    return o.metaObject().className()

def init_widget(w, name):
    """Init a widget for the gallery, give it a tooltip showing the
       class name"""
    w.setObjectName(name)
    w.setToolTip(class_name(w))

def embed_into_hbox_layout(w, margin=5):
    """Embed a widget into a layout to give it a frame"""
    result = QWidget()
    layout = QHBoxLayout(result)
    layout.setContentsMargins(margin, margin, margin, margin)
    layout.addWidget(w)
    return result

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        #set icon
        #self.setWindowIcon(QIcon(':/qt-project.org/logos/pysidelogo.png'))
        '''
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
        #self.setCentralWidget(self.axWidget)
        '''

        self.list = QListWidget()
        #self.setCentralWidget(self.list)
        for i in range(10):
            item = QListWidgetItem(f"Item {i}")
            item.setTextAlignment(Qt.AlignCenter)
            self.list.addItem(item)

        text_edit = QTextEdit("rich_text")        

        button = QPushButton("Open File", self)
        button.clicked.connect(self.handleButton)

        itemview_tabwidget = self.create_itemview_tabwidget()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.list)

        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 11, 7, 5)
        main_layout.addWidget(itemview_tabwidget, 0, 0, 7, 7)
        main_layout.addWidget(text_edit,7,0,2,16)
        main_layout.addWidget(button,0,7,4,4)
        #list.resize()
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)      
        self.setCentralWidget(main_widget)
        #self.button = QPushButton("My Button", self)
        #self.button.clicked.connect(self.handleButton)
        #
        


    def create_itemview_tabwidget(self):
        result = QTabWidget()
        init_widget(result, "bottomLeftTabWidget")
        result.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tree_view = QTreeView()
        init_widget(tree_view, "treeView")
        filesystem_model = QFileSystemModel(tree_view)
        filesystem_model.setRootPath(QDir.rootPath())
        tree_view.setModel(filesystem_model)

        table_widget = QTableWidget()
        init_widget(table_widget, "tableWidget")
        table_widget.setRowCount(10)
        table_widget.setColumnCount(10)

        list_model = QStandardItemModel(0, 1, result)

        #list_model.appendRow(QStandardItem(QIcon(DIR_OPEN_ICON), "Directory"))
        #list_model.appendRow(QStandardItem(QIcon(COMPUTER_ICON), "Computer"))

        list_view = QListView()
        init_widget(list_view, "listView")
        list_view.setModel(list_model)

        icon_mode_listview = QListView()
        init_widget(icon_mode_listview, "iconModeListView")

        icon_mode_listview.setViewMode(QListView.IconMode)
        icon_mode_listview.setModel(list_model)

        result.addTab(embed_into_hbox_layout(tree_view), "Tree View")
        result.addTab(embed_into_hbox_layout(table_widget), "Table")
        result.addTab(embed_into_hbox_layout(list_view), "List")
        result.addTab(embed_into_hbox_layout(icon_mode_listview),
                      "Icon Mode List")
        return result
    
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
        self.list.clear()
        for line in open(file_name):
            try:
                self.list.addItem(QListWidgetItem(line))
            except:
                print()

        
        #QStringConverter(QStringConverter.System)
        #line in_file.readLine()


    def handleButton(self):
        self.open()

class PreprocessingWindow():

    def __init__(self):

        self._progress_bar = self.create_progress_bar()

    #зміна значення _progress_bar
    @Slot()
    def advance_progressbar(self):
        cur_val = self._progress_bar.value()
        max_val = self._progress_bar.maximum()
        self._progress_bar.setValue(cur_val + (max_val - cur_val) / 100)

    def create_progress_bar(self):
        result = QProgressBar()
        init_widget(result, "progressBar")
        result.setRange(0, 10000)
        result.setValue(1000)

        timer = QTimer(self)
        timer.timeout.connect(self.advance_progressbar)
        timer.start(1000)
        return result
    
class Plan_CU(QDialog):
    
    def __init__(self):
        #?
        super().__init__()

        textedit_layout = self.create_textedit_layout()
        check_layout = self.create_check_layout()
        button_layout = self.create_button()

        self.file_tree_view = QTreeView()
        init_widget(self.file_tree_view, "file_treeview")
        filesystem_model = QFileSystemModel(self.file_tree_view)
        filesystem_model.setRootPath(QDir.rootPath())
        self.file_tree_view.setModel(filesystem_model)
        
        self.button_open_file.toggled.connect(self.Start)

        main_layout = QGridLayout(self)
        main_layout.addLayout(textedit_layout,0,0,7,5)
        main_layout.addLayout(check_layout,7,0,4,5)
        main_layout.addLayout(button_layout,7,5,4,5)
        main_layout.addWidget(self.file_tree_view,0,5,7,5)

    def create_textedit_layout(self):
        #result = QGroupBox("textedit")
        #init_widget(result, "textedit_groupbox")
        self.edit_text_1 = QSpinBox()
        init_widget(self.edit_text_1, "edit_text_1")
        self.edit_text_1.setValue(0)

        self.edit_text_2 = QSpinBox()
        init_widget(self.edit_text_2, "edit_text_2")
        self.edit_text_2.setValue(0)

        self.edit_text_3 = QSpinBox()
        init_widget(self.edit_text_3, "edit_text_3")
        self.edit_text_3.setValue(0)

        self.edit_text_4 = QSpinBox()
        init_widget(self.edit_text_4, "edit_text_4")
        self.edit_text_4.setValue(0)

        self.edit_text_5 = QSpinBox()
        init_widget(self.edit_text_5, "edit_text_5")
        self.edit_text_5.setValue(0)

        self.edit_text_6 = QSpinBox()
        init_widget(self.edit_text_6, "edit_text_6")
        self.edit_text_6.setValue(0)

        self.edit_text_7 = QSpinBox()
        init_widget(self.edit_text_7, "edit_text_7")
        self.edit_text_7.setValue(0)

        self.label_1 = QLabel("_sadawdawd")
        init_widget(self.label_1, "label_1")

        label_2 = QLabel("_")
        init_widget(label_2, "label_1")

        label_3 = QLabel("_")
        init_widget(label_3, "label_1")

        label_4 = QLabel("_")
        init_widget(label_4, "label_1")

        label_5 = QLabel("_")
        init_widget(label_5, "label_1")

        label_6 = QLabel("_")
        init_widget(label_6, "label_1")

        label_7 = QLabel("_")
        init_widget(label_7, "label_1")

        edit_text_layout_1 = QHBoxLayout()
        edit_text_layout_1.addWidget(self.label_1)
        edit_text_layout_1.addWidget(self.edit_text_1)
        edit_text_layout_1.addStretch(1)

        edit_text_layout_2 = QHBoxLayout()
        edit_text_layout_2.addWidget(label_2)
        edit_text_layout_2.addWidget(self.edit_text_2)
        edit_text_layout_2.addStretch(1)

        edit_text_layout_3 = QHBoxLayout()
        edit_text_layout_3.addWidget(label_3)
        edit_text_layout_3.addWidget(self.edit_text_3)
        edit_text_layout_3.addStretch(1)

        edit_text_layout_4 = QHBoxLayout()
        edit_text_layout_4.addWidget(label_4)
        edit_text_layout_4.addWidget(self.edit_text_4)
        edit_text_layout_4.addStretch(1)

        edit_text_layout_5 = QHBoxLayout()
        edit_text_layout_5.addWidget(label_5)
        edit_text_layout_5.addWidget(self.edit_text_5)
        edit_text_layout_5.addStretch(1)

        edit_text_layout_6 = QHBoxLayout()
        edit_text_layout_6.addWidget(label_6)
        edit_text_layout_6.addWidget(self.edit_text_6)
        edit_text_layout_6.addStretch(1)

        edit_text_layout_7 = QHBoxLayout()
        edit_text_layout_7.addWidget(label_7)
        edit_text_layout_7.addWidget(self.edit_text_7)
        edit_text_layout_7.addStretch(1)

        #main_layout = QHBoxLayout(result)
        main_layout = QVBoxLayout()
        main_layout.addLayout(edit_text_layout_1)
        main_layout.addLayout(edit_text_layout_2)
        main_layout.addLayout(edit_text_layout_3)
        main_layout.addLayout(edit_text_layout_4)
        main_layout.addLayout(edit_text_layout_5)
        main_layout.addLayout(edit_text_layout_6)
        main_layout.addLayout(edit_text_layout_7)
        main_layout.addStretch(1)

        #return result
        return main_layout

    def create_check_layout(self):

        self.radiobutton_1 = QRadioButton("Radio button 1")
        init_widget(self.radiobutton_1, "radioButton1")
        self.radiobutton_2 = QRadioButton("Radio button 2")
        init_widget(self.radiobutton_2, "radioButton2")
        self.radiobutton_3 = QRadioButton("Radio button 3")
        init_widget(self.radiobutton_3, "radioButton3")
        self.radiobutton_1.setChecked(True)        

        checkable_layout = QVBoxLayout()
        checkable_layout.addWidget(self.radiobutton_1)
        checkable_layout.addWidget(self.radiobutton_2)
        checkable_layout.addWidget(self.radiobutton_3)

        checkable_layout.addStretch(1)

        return checkable_layout

    def create_button(self):

        self.button_open_file = QPushButton("Open File")
        init_widget(self.button_open_file, "button_open_file")
        self.button_open_file.setCheckable(True)
        self.button_open_file.setChecked(True)
        
        self.button_start = QPushButton("Start")
        init_widget(self.button_start, "button_start")
        self.button_start.setDefault(True)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.button_open_file)
        button_layout.addWidget(self.button_start)
        button_layout.addStretch(50)

        return button_layout

    def getFullPath(self):
        def FullPath(index):
            try:
                path = index.model().itemData(index)[0]
                temp = index.parent()
                #print(path)
                parent_path = FullPath(temp)            
            except:
                return ""
            if " " in path:
                path = f"\"{path}\""
            return f"{parent_path}/{path}"
        
        index = self.file_tree_view.selectedIndexes()
        return f"{FullPath(index[0])}"

    def Start(self):

        self.edit_text_1.setValue(1)

        #отримує посилання на файл обраний через вікно treeview
        print(self.getFullPath())
        #self.label_1.setText()
        



    
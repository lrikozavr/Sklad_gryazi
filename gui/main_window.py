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
                               QStyleFactory, QTableWidget, QTabWidget, QMenuBar,
                               QTextBrowser, QTextEdit, QToolBox, QToolButton,
                               QTreeView, QVBoxLayout, QWidget, QTableWidgetItem, QLayout)

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

class ProgressBar(QDialog):

    def __init__(self,name):
        super().__init__()
        
        self._current_index_process = 0
        self._max_index_process = 1
        self._progress_bar = self.create_progress_bar(name)
    
    def create_progress_bar(self, name):
        result = QProgressBar()
        init_widget(result, f"{name}_progressBar")
        result.setRange(0, 10000)
        result.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advance_progressbar)
        timer.start(0)
        return result

    @Slot()
    #зміна значення _progress_bar при кожній зміні значень таймера (це треба буде прибрати)
    def advance_progressbar(self):
        max_val = self._progress_bar.maximum()
        #self. cur і max значення індексів проробленої роботи
        self._progress_bar.setValue(max_val*self._current_index_process / self._max_index_process)

def open_file(widget):
    file_name = QFileDialog.getOpenFileName(widget,
            "Open File", QDir.currentPath(),
            "Files (*.*)")[0]

    if not file_name:
        QMessageBox.warning(widget, "File", f"File don't exist")
    
    in_file = QFile(file_name)
    if not in_file.open(QFile.ReadOnly | QFile.Text):
        reason = in_file.errorString()
        QMessageBox.warning(widget, "DOM Bookmarks",
                f"Cannot read file {file_name}:\n{reason}.")
        return
    return file_name



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        #set icon
        #self.setWindowIcon(QIcon(':/qt-project.org/logos/pysidelogo.png'))
        
        toolBar = QToolBar()
        self.addToolBar(toolBar)
        fileMenu = self.menuBar().addMenu("&File")
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        fileMenu.addAction(loadAction)
        toolBar.addAction(loadAction)
        exitAction = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        preprocessMenu = self.menuBar().addMenu("&Preprocess")
        plancu = QAction("Plan_CU", self, triggered = self.Plan_CU)
        preprocessMenu.addAction(plancu)
        control = QAction("Control", self, triggered = self.Control)
        preprocessMenu.addAction(control)

        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAct)
        self.axWidget = QAxWidget()
        #self.setCentralWidget(self.axWidget)
        

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
    
    def create_video_view_layout(self):
        result = QHBoxLayout()
        init_widget(result, "vide_view_layout")
        

        return


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
        file_name = open_file(self)
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

    def Plan_CU(self):
        self.widget = Plan_CU()
        self.widget.show()
        #del widget

    def Control(self):
        self.widget = Control()
        self.widget.show()

class Control(QDialog):

    def __init__(self):
        super().__init__()
        self.probarwidget = ProgressBar("plan_cu")

        menubar = QMenuBar(self)
        fileMenu = menubar.addMenu("&File")
        openAction = QAction("Open file", self, shortcut = "Ctrl+O", triggered=self.open_fcu_file)
        fileMenu.addAction(openAction)
        saveAction = QAction("Save file", self, shortcut = "Ctrl+S", triggered=self.save_observ_file)
        fileMenu.addAction(saveAction)

        settingsMenu = menubar.addMenu("&Settings")
        #цей синтаксис працює. треба додати можливість відмічати конкретний обраний об'єкт
        settingsModeMenu = settingsMenu.addMenu("&Mode")

        generalsettings = QAction("General", self, shortcut = "Ctrl+G", triggered=self.setgeneralsettings)
        settingsMenu.addAction(generalsettings)

        #buttons_layout = self.create_buttons_layout()
        #lists_layout = self.create_lists_layout()

        self.main_layout = QGridLayout(self)
        #self.main_layout.addLayout(buttons_layout,0,0,4,20)
        #self.main_layout.addLayout(lists_layout,4,0,15,20)
        self.main_layout.addWidget(self.probarwidget._progress_bar,19,0,1,20)
        
    def create_buttons_layout(self):
        pass

    def create_lists_layout(self):
        pass

    def open_fcu_file(self):
        file_name = open_file(self)
        self.list_fcu.clear()
        
        #потрібен специфічний парсинг
        #нижче наведений код до нього не відноситься
        for line in open(file_name):
            try:
                self.list.addItem(QListWidgetItem(line))
            except:
                print()

    def save_observ_file(self):
        pass

    def setgeneralsettings():
        pass

class Plan_CU(QDialog):
    
    #Треба додати деструктор

    def __init__(self):
        #?
        super().__init__()
        
        #створюємо об'єкт класу меню загрузки
        self.probarwidget = ProgressBar("plan_cu")
        
        textedit_layout = self.create_textedit_layout()
        check_layout = self.create_check_layout()
        button_layout = self.create_button()

        """
        self.file_tree_view = QTreeView()
        init_widget(self.file_tree_view, "file_treeview")
        self.filesystem_model = QFileSystemModel(self.file_tree_view)
        self.filesystem_model.setRootPath("")
        self.file_tree_view.setModel(self.filesystem_model)
        """

        self.table_widget = QTableWidget()
        init_widget(self.table_widget, "tableWidget")
        
        self.button_start.toggled.connect(self.Start)
        self.button_open_file.toggled.connect(self.local_open_file)

        #розбиття на 4 сектори з віджетами
        self.main_layout = QGridLayout(self)
        self.main_layout.addLayout(textedit_layout,0,0,7,5)
        self.main_layout.addLayout(check_layout,7,0,4,5)
        self.main_layout.addLayout(button_layout,7,5,4,5)
        self.main_layout.addWidget(self.table_widget,0,5,7,5)
        self.main_layout.addWidget(self.probarwidget._progress_bar,11,0,2,10)
        
        #фіксуємо розмір вікна
        self.setFixedSize(QSize(400,300))

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
        self.button_start.setCheckable(True)

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

    def local_open_file(self):
        #отримуємо посилання на файл з TLE
        self.file_name = open_file(self)

        self.mass = []
        #читаємо файл та заносимо значення всіх даних до масиву mass
        for line in open(self.file_name):
            m_line = line.split(" ")
            self.mass.append(m_line)
        
        self.table_widget.setRowCount(len(self.mass[0]))
        self.table_widget.setColumnCount(len(self.mass))
        
        self.table_widget.resizeColumnsToContents()
        #self.table_widget.setColumnWidth(1,20)
        #self.probarwidget._max_index_process = self.table_widget.rowCount()
        
        #можна зробити так, щоб воно виводило тільки певну кількість елементів
        for i in range(self.table_widget.rowCount()):
            #self.probarwidget._current_index_process = i + 1
            for j in range(self.table_widget.columnCount()):
                item = QTableWidgetItem(self.mass[i][j])
                self.table_widget.setItem(i,j,item)
        
        

    def Start(self):

        self.edit_text_1.setValue(1)          
        #отримує посилання на файл обраний через вікно treeview
        #print(self.getFullPath())
    



    
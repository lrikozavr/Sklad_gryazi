from PySide6.QtGui import (QAction, QCloseEvent, QCursor, QDesktopServices, QGuiApplication, QIcon,
                           QKeySequence, QShortcut, QStandardItem,
                           QStandardItemModel)
from PySide6.QtWidgets import (QMainWindow, QToolBar, QListWidget, QListWidgetItem,
                               QPushButton, QMessageBox, QFileDialog, QProgressBar,
                               QApplication, QCheckBox, QComboBox, QCommonStyle,
                               QCommandLinkButton, QDateEdit, QDial, QDoubleSpinBox,
                               QDialog, QDialogButtonBox, QFileSystemModel,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QListView, QMenu, QPlainTextEdit,
                               QProgressBar, QPushButton, QRadioButton, QTimeEdit,
                               QScrollBar, QSizePolicy, QSlider, QSpinBox, QStyle,
                               QStyleFactory, QTableWidget, QTabWidget, QMenuBar,
                               QTextBrowser, QTextEdit, QToolBox, QToolButton,
                               QTreeView, QVBoxLayout, QWidget, QTableWidgetItem, QLayout)

from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtCore import Qt, QSize, QFile, QDir, QTextStream, QStringConverter, QTimer, Slot, QDate, QTime

from header import *

from types import SimpleNamespace
import time

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
    layout.addLayout(w)
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
        timer.start(100)
        return result

    @Slot()
    #зміна значення _progress_bar при кожній зміні значень таймера (це треба буде прибрати)
    def advance_progressbar(self):
        max_val = self._progress_bar.maximum()
        #self. cur і max значення індексів проробленої роботи
        self._progress_bar.setValue(max_val*self._current_index_process / self._max_index_process)

#fuction that open window for select file
#return path to file
#можна додати "запам'ятовування" останнього відування, якщо замінити QDir.currentPath() на вхідну змінну
def open_file(widget, filters = "*.*"):
    file_name = QFileDialog.getOpenFileName(widget,
            "Open File", QDir.currentPath(),
            f"Files {filters}")[0]

    if not file_name:
        QMessageBox.warning(widget, "File", f"File don't exist")
        raise Exception(f"{widget}. File don't exist")
    
    #не вигадав додаткову умову
    '''
    in_file = QFile(file_name)
    if not in_file.open(QFile.ReadOnly | QFile.Text):
        reason = in_file.errorString()
        QMessageBox.warning(widget, "DOM Bookmarks",
                f"Cannot read file {file_name}:\n{reason}.")
        return
    '''

    return file_name

#add text to "log" variable
def write_to_log(log = QWidget, text = str):
    temp_text = log.toPlainText()
    temp_text += f"\n[{QTime.currentTime().toPython()}]: {text}"
    log.setText(temp_text)
    

#Клас який описує Головне вікно
class MainWindow(QMainWindow):


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        #set icon
        #self.setWindowIcon(QIcon(':/qt-project.org/logos/pysidelogo.png'))
        self.settings = SettingsWindow(self)
        #
        fileMenu = self.menuBar().addMenu("&File")
        settings = QAction("Settings", self, triggered = self.Settings)
        fileMenu.addAction(settings)
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
        
        #create mainwindow general widget
        itemview_tabwidget = self.create_itemview_tabwidget()

        main_layout = QGridLayout()
        main_layout.addWidget(itemview_tabwidget, 0, 0, 7, 16)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        write_to_log(self._observation_log,"Start!")
    
    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.quit()

    def create_itemview_tabwidget(self):
        result = QTabWidget()
        init_widget(result, "bottomLeftTabWidget")
        result.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        
        '''
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
        '''
        video_layout = self.create_video_layout()
        result.addTab(embed_into_hbox_layout(video_layout), "Camera")
        return result
    
    def create_image_layout(self):
        result = QGridLayout()
        
        tree_view = QTreeView()
        init_widget(tree_view, "treeView")
        filesystem_model = QFileSystemModel(tree_view)
        filesystem_model.setRootPath(QDir.rootPath())
        tree_view.setModel(filesystem_model)


        return result

    #video layout
    def create_video_layout(self):
        result = QGridLayout()

        #Button panel layout
        ####################################################################
        #X
        X_label = QLabel("X:\t")
        self.X_value_label = QLabel("_")
        #Y
        Y_label = QLabel("Y:\t")
        self.Y_value_label = QLabel("_")
        #combine X&Y
        xy_text_layout = QHBoxLayout()
        xy_text_layout.addWidget(X_label,1)
        xy_text_layout.addWidget(self.X_value_label,3)
        xy_text_layout.addWidget(Y_label,1)
        xy_text_layout.addWidget(self.Y_value_label,3)
        
        #Az
        Az_label = QLabel("Az:\t")
        self.Az_value_label = QLabel("_")
        #H
        H_label = QLabel("H:\t")
        self.H_value_label = QLabel("_")
        #combine Az&H
        AzH_text_layout = QHBoxLayout()
        AzH_text_layout.addWidget(Az_label,1)
        AzH_text_layout.addWidget(self.Az_value_label,3)
        AzH_text_layout.addWidget(H_label,1)
        AzH_text_layout.addWidget(self.H_value_label,3)

        #dAz
        dAz_label = QLabel("dAz:\t")
        self.dAz_value_label = QLabel("_")
        #dh
        dH_label = QLabel("dH:\t")
        self.dH_value_label = QLabel("_")
        #combine dAz&dH
        dAzH_text_layout = QHBoxLayout()
        dAzH_text_layout.addWidget(dAz_label,1)
        dAzH_text_layout.addWidget(self.dAz_value_label,3)
        dAzH_text_layout.addWidget(dH_label,1)
        dAzH_text_layout.addWidget(self.dH_value_label,3)
        
        #CurrentTimeValue line
        self.CurrentTimeValueEdit = QTextBrowser()
        self.CurrentTimeValueEdit.setText(str(QTime.currentTime().toPython()))
        self.CurrentTimeValueEdit.setFixedSize(QSize(93,28))

        self.timer = QTimer(self)
        #self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateCurrentTime)
        self.timer.start(100)

        #ArrowButtonBlock
        style = QStyleFactory.create("Fusion")
        left_arrow_button = QPushButton()
        left_arrow_button.setIcon(style.standardIcon(style.StandardPixmap(52)))
        left_arrow_button.clicked.connect(self.left_arrow_button)

        right_arrow_button = QPushButton()
        right_arrow_button.setIcon(style.standardIcon(style.StandardPixmap(53)))
        right_arrow_button.clicked.connect(self.right_arrow_button)
        
        up_arrow_button = QPushButton()
        up_arrow_button.setIcon(style.standardIcon(style.StandardPixmap(50)))
        up_arrow_button.clicked.connect(self.up_arrow_button)

        down_arrow_button = QPushButton()
        down_arrow_button.setIcon(style.standardIcon(style.StandardPixmap(51)))
        down_arrow_button.clicked.connect(self.down_arrow_button)
        
        #combine ArrowButton
        arrow_buttons_layout = QGridLayout()
        arrow_buttons_layout.addWidget(left_arrow_button, 4, 0, 4, 4)
        arrow_buttons_layout.addWidget(right_arrow_button, 4, 8, 4, 4)
        arrow_buttons_layout.addWidget(up_arrow_button, 0, 4, 4, 4)
        arrow_buttons_layout.addWidget(down_arrow_button, 8, 4, 4, 4)

        #Start button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.camera_start)

        #Stop button
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.camera_stop)

        #Continue/Next button
        continue_button = QPushButton("Continue/Next")
        continue_button.clicked.connect(self.camera_continue)

        #view CheckBox: grid, star, trajectory
        self.camera_grid_check_box = QCheckBox("add Grid")
        self.camera_grid_check_box.setChecked(False)
        self.camera_grid_check_box.clicked.connect(self.paint_camera_grid)

        self.camera_star_check_box = QCheckBox("add Star")
        self.camera_star_check_box.setChecked(False)
        self.camera_star_check_box.clicked.connect(self.paint_camera_star)
        
        self.camera_trajectory_check_box = QCheckBox("add Trajectory")
        self.camera_trajectory_check_box.setChecked(False)
        self.camera_trajectory_check_box.clicked.connect(self.paint_camera_trajectory)

        #combine all of windets above
        buttons_layout = QVBoxLayout()
        buttons_layout.addLayout(xy_text_layout, 1)
        buttons_layout.addLayout(AzH_text_layout, 1)
        buttons_layout.addLayout(dAzH_text_layout, 1)
        buttons_layout.addWidget(self.CurrentTimeValueEdit, 1)
        buttons_layout.addLayout(arrow_buttons_layout, 3)
        buttons_layout.addWidget(start_button, 1)
        buttons_layout.addWidget(stop_button, 1)
        buttons_layout.addWidget(continue_button, 1)
        buttons_layout.addWidget(self.camera_grid_check_box, 1)
        buttons_layout.addWidget(self.camera_star_check_box, 1)
        buttons_layout.addWidget(self.camera_trajectory_check_box, 1)
        ####################################################################
        #Log
        self._observation_log = QTextBrowser()
        init_widget(self._observation_log, "observation_error_logTextBrowser")
        
        #Table of observation list
        self.table_list_observations = QTableWidget()
        init_widget(self.table_list_observations, "table_list_observationsTableWidget")

        #Camera view
        self.camera_view = QWidget()
        init_widget(self.camera_view, "camera_view")
        
        #Combine all widget and layout above
        result.addWidget(self.camera_view, 0, 0, 7, 7)
        result.addLayout(buttons_layout, 0, 7, 7, 3)
        result.addWidget(self.table_list_observations, 0, 10, 7, 6)
        result.addWidget(self._observation_log, 7, 0, 2, 16)

        return result
    
    def create_image_processing_layout(self):
        main_layout = QGridLayout()

        
        
        self.image_tree_view = QTreeView()

        self.image_view = QWidget()
        init_widget(self.image_view, "image_view")

        

    
    def left_arrow_button(self):
        pass

    def right_arrow_button(self):
        pass

    def up_arrow_button(self):
        pass

    def down_arrow_button(self):
        pass

    def camera_start(self):
        if(not self.timer.isActive()):
            self.timer.start()
            write_to_log(self._observation_log,"Timer start by StartPushButton")

    def camera_stop(self):
        if(self.timer.isActive()):
            self.timer.stop()
            write_to_log(self._observation_log,"Timer stop by StopPushButton")
        
    def camera_continue(self):
        pass

    def paint_camera_grid(self):
        pass

    def paint_camera_star(self):
        pass

    def paint_camera_trajectory(self):
        pass

    #як це можна винести в окремий потік?
    @Slot(QTimer)
    def updateCurrentTime(self):
        self.CurrentTimeValueEdit.setText(str(QTime.currentTime().toPython()))
        #write_to_log(self._observation_log,time.perf_counter())

    #Можна замість нього просто додати функцію яка б одразу після роботи Control виводила все     
    def open(self):
        file_name = open_file(self,"*.*")
        self.list.clear()
        for line in open(file_name):
            try:
                self.list.addItem(QListWidgetItem(line))
            except:
                print()

        
        #QStringConverter(QStringConverter.System)
        #line in_file.readLine()


#    def handleButton(self):
#        self.open()

    def Plan_CU(self):
        self.widget_Plan_CU = Plan_CU(self)
        self.widget_Plan_CU.show()
        #del widget

    def Control(self):
        self.widget_Control = Control(self)
        self.widget_Control.show()

    def Settings(self):
        self.settings.show()

class Control(QDialog):

    def __init__(self, main_window):
        super().__init__()
        #передаємо клас MainWindow у користування класу Control
        self.main_window = main_window
        
        #write_to_log(self.main_window._observation_log,"this shit works")

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

        buttons_layout = self.create_buttons_layout()
        lists_layout = self.create_lists_layout()

        self.main_layout = QGridLayout(self)
        self.main_layout.addLayout(buttons_layout,0,0,2,20)
        self.main_layout.addLayout(lists_layout,2,0,17,20)
        self.main_layout.addWidget(self.probarwidget._progress_bar,19,0,1,20)

        self.setFixedSize(QSize(1000,1000))
    
    def create_buttons_layout(self):
        self.date_edit_line = QDateEdit()
        init_widget(self.date_edit_line, "date_editDateTimeEdit")
        self.date_edit_line.setDate(QDate.currentDate())

        self.auto_select_button = QPushButton("Auto Select")
        init_widget(self.auto_select_button, "auto_selectPushButton")

        self.select_button = QPushButton("Select")
        init_widget(self.select_button, "selectPushButton")

        self.delete_button = QPushButton("Delete")
        init_widget(self.delete_button, "deletePushButton")

        local_layout = QHBoxLayout()
        local_layout.addWidget(self.date_edit_line,10)
        local_layout.addWidget(self.auto_select_button,10)
        local_layout.addWidget(self.select_button,10)
        local_layout.addWidget(self.delete_button,5)

        return local_layout

    def create_lists_layout(self):
        self.list_fcu = QListWidget()
        init_widget(self.list_fcu, "list_fcu_ListWidget")

        self.table_list = QTableWidget()
        init_widget(self.table_list, "table_list_TableWidget")

        local_layout = QHBoxLayout()
        local_layout.addWidget(self.list_fcu,20)
        local_layout.addStretch(1)
        local_layout.addWidget(self.table_list,15)
        
        return local_layout

    def open_fcu_file(self):
        file_name = open_file(self, "*.fcu")
        self.list_fcu.clear()
        
        #потрібен специфічний парсинг
        #нижче наведений код до нього не відноситься
        for line in open(file_name):
            try:
                self.list.addItem(QListWidgetItem(line))
            except:
                print()

    #https://doc.qt.io/qtforpython-6/examples/example_external_pandas.html

    def save_observ_file(self):
        pass

    def setgeneralsettings():
        pass


class Plan_CU(QDialog):
    
    #Треба додати деструктор

    def __init__(self, parent):
        #?
        super().__init__()
        
        #передаємо об'єкт класу вище, для взаємної взаємодії
        self.main_window = parent
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

        self.set_value_from_settings()

    def create_textedit_layout(self):
        #result = QGroupBox("textedit")
        #init_widget(result, "textedit_groupbox")
        
        type_label = QLabel("Type")
        init_widget(type_label, "label_1")
        self.type_edittext = QTextEdit()
        init_widget(self.type_edittext, "type_edit_text")
        self.type_edittext.setText("LEO")

        time_label = QLabel("Time")
        init_widget(time_label, "label_2")
        self.time_edittext = QTextEdit()
        init_widget(self.time_edittext, "time_edit_text")
        self.time_edittext.setText("UT")

        mag_label = QLabel("Magnitude")
        init_widget(mag_label, "mag_label")
        self.mag_edittext = QDoubleSpinBox()
        init_widget(self.mag_edittext, "mag_edit_text")
        self.mag_edittext.setValue(8.5)

        MaxSunElev_label = QLabel("MaxSunElev")
        init_widget(MaxSunElev_label, "MaxSunElev_label")
        self.MaxSunElev_edittext = QDoubleSpinBox()
        init_widget(self.MaxSunElev_edittext, "MaxSunElev_edit_text")
        self.MaxSunElev_edittext.setValue(-8.0)

        MinObsElev_label = QLabel("MinObsElev")
        init_widget(MinObsElev_label, "MinObsElev_label")
        self.MinObsElev_edittext = QDoubleSpinBox()
        init_widget(self.MinObsElev_edittext, "MinObsElev_edit_text")
        self.MinObsElev_edittext.setValue(15.0)

        MaxObsElev_label = QLabel("MaxObsElev")
        init_widget(MaxObsElev_label, "MaxObsElev_label")
        self.MaxObsElev_edittext = QDoubleSpinBox()
        init_widget(self.MaxObsElev_edittext, "MaxObsElev_edit_text")
        self.MaxObsElev_edittext.setValue(60.0)

        TimeStep_label = QLabel("TimeStep")
        init_widget(TimeStep_label, "TimeStep_label")
        self.TimeStep_edittext = QDoubleSpinBox()
        init_widget(self.TimeStep_edittext, "TimeStep_edit_text")
        self.TimeStep_edittext.setValue(10.0)

        type_layout = QHBoxLayout()
        type_layout.addWidget(type_label)
        type_layout.addStretch(1)
        type_layout.addWidget(self.type_edittext)

        time_layout = QHBoxLayout()
        time_layout.addWidget(time_label)
        time_layout.addStretch(1)
        time_layout.addWidget(self.time_edittext)

        mag_layout = QHBoxLayout()
        mag_layout.addWidget(mag_label)
        mag_layout.addStretch(1)
        mag_layout.addWidget(self.mag_edittext)

        MaxSunElev_layout = QHBoxLayout()
        MaxSunElev_layout.addWidget(MaxSunElev_label)
        MaxSunElev_layout.addStretch(1)
        MaxSunElev_layout.addWidget(self.MaxSunElev_edittext)

        MinObsElev_layout = QHBoxLayout()
        MinObsElev_layout.addWidget(MinObsElev_label)
        MinObsElev_layout.addStretch(1)
        MinObsElev_layout.addWidget(self.MinObsElev_edittext)

        MaxObsElev_layout = QHBoxLayout()
        MaxObsElev_layout.addWidget(MaxObsElev_label)
        MaxObsElev_layout.addStretch(1)
        MaxObsElev_layout.addWidget(self.MaxObsElev_edittext)
        
        TimeStep_layout = QHBoxLayout()
        TimeStep_layout.addWidget(TimeStep_label)
        TimeStep_layout.addStretch(1)
        TimeStep_layout.addWidget(self.TimeStep_edittext)

        #main_layout = QHBoxLayout(result)
        main_layout = QVBoxLayout()
        main_layout.addLayout(type_layout)
        main_layout.addLayout(time_layout)
        main_layout.addLayout(mag_layout)
        main_layout.addLayout(MaxSunElev_layout)
        main_layout.addLayout(MinObsElev_layout)
        main_layout.addLayout(MaxObsElev_layout)
        main_layout.addLayout(TimeStep_layout)
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
    '''
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
    '''
    def set_value_from_settings(self):
        try:
            self.type_edittext = self.main_window.settings.obs.type
            self.time_edittext = self.main_window.settings.obs.time
            self.mag_edittext = self.main_window.settings.obs.magnitude
            self.MaxSunElev_edittext = self.main_window.settings.obs.maxsunelev
            self.MinObsElev_edittext = self.main_window.settings.obs.minobselev
            self.MaxObsElev_edittext = self.main_window.settings.obs.maxobselev
            self.TimeStep_edittext = self.main_window.settings.obs.timestep
        except:
            write_to_log(self.main_window._observation_log, "Settings not downloaded from *.json")


    def local_open_file(self):
        #отримуємо посилання на файл з TLE
        self.file_name = open_file(self, "*.tle")

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
        
        #https://doc.qt.io/qtforpython-6/examples/example_external_pandas.html

    def Start(self):

        self.edit_text_1.setValue(1)          
        #отримує посилання на файл обраний через вікно treeview
        #print(self.getFullPath())
        
        msgbx = QMessageBox(self)
        msgbx.setText("Done!")
        msgbx.setWindowTitle("Processing...")
        #msgbx.setFixedSize(QSize(200,100))
        msgbx.show()
        #QMessageBox.done(self, 0)

    
class SettingsWindow(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.main_window = parent

        self.main_layout = QGridLayout(self)
        #через replace
        self.obs = SimpleNamespace()

        main_list = QListWidget()
        main_list.addItem(QListWidgetItem("Observer"))
        main_list.addItem(QListWidgetItem("Sattelite"))
        main_list.addItem(QListWidgetItem("Telescope"))

        main_list.itemClicked.connect(self.click_list_item)

        open_json_config_button = QPushButton("Open *.json config")
        open_json_config_button.clicked.connect(self.get_json_config)

        #Observer
        observer_lyout = QVBoxLayout()
        #Site
        site_label = QLabel("Site")
        self.site_edittext = QTextEdit("LA")
        
        site_layout = QHBoxLayout()
        site_layout.addWidget(site_label, 1)
        site_layout.addWidget(self.site_edittext, 3)
        #Code
        code_label = QLabel("Code")
        self.code_edittext = QTextEdit("LVIV")

        code_layout = QHBoxLayout()
        code_layout.addWidget(code_label, 1)
        code_layout.addWidget(self.code_edittext, 3)
        #LLH
        llh_label = QLabel("LLH")
        self.llh_edittext = QTextEdit("49.917573, 23.954415, 359.490000")

        llh_layout = QHBoxLayout()
        llh_layout.addWidget(llh_label, 1)
        llh_layout.addWidget(self.llh_edittext, 3)

        observer_lyout.addLayout(site_layout)
        observer_lyout.addLayout(code_layout)
        observer_lyout.addLayout(llh_layout)
        ##########################################
        
        self.observer_widget = QWidget()
        self.observer_widget.setLayout(observer_lyout)
        ##########################################
        
        
        #Sattelite list
        sattelite_layout = QVBoxLayout()
        #Table
        self.sattelite_table = QTableWidget()
        #Button
        button_layout = QHBoxLayout()
        #
        add_item_table = QPushButton("Add")
        add_item_table.clicked.connect(self.add_item_table)

        delete_item_table = QPushButton("Delete")
        delete_item_table.clicked.connect(self.delete_item_table)

        button_layout.addWidget(add_item_table)
        button_layout.addWidget(delete_item_table)
        #
        sattelite_layout.addWidget(self.sattelite_table)
        sattelite_layout.addLayout(button_layout)
        ##############################################

        self.sattelite_widget = QWidget()
        self.sattelite_widget.setLayout(sattelite_layout)
        ##########################################

        #Telescope
        telescope_layout = QVBoxLayout()
        
        #Name
        name_label = QLabel("Name")
        self.name_textedit = QTextEdit("Meade")

        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_textedit)
        
        #Mount
        mount_label = QLabel("Mount")
        self.mount_textedit = QTextEdit("A")

        mount_layout = QHBoxLayout()
        mount_layout.addWidget(mount_label)
        mount_layout.addWidget(self.mount_textedit)
        
        #Port
        port_name_label = QLabel("Port")
        self.port_name_textedit = QTextEdit("COM")

        port_name_layout = QVBoxLayout()
        port_name_layout.addWidget(port_name_label)
        port_name_layout.addWidget(self.port_name_textedit)

        #
        port_path_label = QLabel("Path")
        self.port_path_textedit = QTextEdit("")

        port_path_layout = QVBoxLayout()
        port_path_layout.addWidget(port_path_label)
        port_path_layout.addWidget(self.port_path_textedit)
        #
        port_speed_label = QLabel("Speed")
        #
        #замінити на випадаючий список
        self.port_speed_textedit = QTextEdit("19200")

        port_speed_layout = QVBoxLayout()
        port_speed_layout.addWidget(port_speed_label)
        port_speed_layout.addWidget(self.port_speed_textedit)
        
        #
        port_size_label = QLabel("Size")
        self.port_size_textedit = QTextEdit("200")

        port_size_layout = QVBoxLayout()
        port_size_layout.addWidget(port_size_label)
        port_size_layout.addWidget(self.port_size_textedit)
        #

        port_layout = QHBoxLayout()
        port_layout.addLayout(port_name_layout)
        port_layout.addLayout(port_path_layout)
        port_layout.addLayout(port_speed_layout)
        port_layout.addLayout(port_size_layout)
        #####################################################

        telescope_layout.addLayout(name_layout)
        telescope_layout.addLayout(mount_layout)
        telescope_layout.addLayout(port_layout)
        #####################################################

        self.telescope_widget = QWidget()
        self.telescope_widget.setLayout(telescope_layout)


        self.main_layout.addWidget(main_list,0,0,7,3)
        self.main_layout.addWidget(self.observer_widget,0,3,7,7)
        self.main_layout.addWidget(open_json_config_button,7,0,1,10)

        #self.main_layout.layout()

    def click_list_item(self, item):
        def check_widget():
            if(self.observer_widget.isVisible()):
                return self.observer_widget
            elif(self.sattelite_widget.isVisible()):
                return self.sattelite_widget
            elif(self.telescope_widget.isVisible()):
                return self.telescope_widget
            
        name = item.text()
        widget = check_widget()
        widget.setVisible(False)
        if(name == "Sattelite"):
            self.main_layout.replaceWidget(widget, self.sattelite_widget)
            self.sattelite_widget.setVisible(True)
        elif(name == "Observer"):
            self.main_layout.replaceWidget(widget, self.observer_widget)
            self.observer_widget.setVisible(True)
        elif(name == "Telescope"):
            self.main_layout.replaceWidget(widget, self.telescope_widget)
            self.telescope_widget.setVisible(True)
            

    def get_json_config(self):
        import json
        filename = open_file(self, "*.json")
        fin = open(filename)
        conf = json.load(fin)
        fin.close()

        #try:
        #якщо буде помилка, то помилку вивести у log
        self.site_edittext.setText(conf['Observer']['Site'])
        self.code_edittext.setText(conf['Observer']['Code'])
        self.llh_edittext.setText(str(conf['Observer']['LLH']))

        self.name_textedit.setText(conf["Telescope"]["Name"])
        self.mount_textedit.setText(conf["Telescope"]["Mount"])
        self.port_name_textedit.setText(conf["Telescope"]["Port"]["Name"])
        self.port_path_textedit.setText(conf["Telescope"]["Port"]["Path"])
        self.port_speed_textedit.setText(str(conf["Telescope"]["Port"]["Speed"]))
        self.port_size_textedit.setText(str(conf["Telescope"]["Port"]["Size"]))
        
        self.obs.type = conf['Observation']['Type']
        self.obs.time = conf['Observation']['Time']
        self.obs.magnitude = conf['Observation']['Magnitude']
        self.obs.maxsunelev = conf['Observation']['MaxSunElev']
        self.obs.minobselev = conf['Observation']['MinObsElev']
        self.obs.maxobselev = conf['Observation']['MaxObsElev']
        self.obs.timestep = conf['Observation']['TimeStep']
        
        import os
        path = os.path.dirname(os.path.abspath(__file__))
        index = 0
        self.sattelite_table.setColumnCount(1)
        #self.sattelite_table.setRowCount(1)
        sattelite_list = []
        #self.sattelite_table.clear()
        for sat_name in open(f"{path}\\{conf['Path']['List']}"):
            sattelite_list.append()
            item = QTableWidgetItem(str(sat_name.split("\n")[0]))
            self.sattelite_table.setRowCount(index+1)
            self.sattelite_table.setItem(index, 0, item)
            print(index, sat_name)
            index += 1
        
        self.sattelite_table.resizeColumnsToContents()
        
        write_to_log(self.main_window._observation_log,"File *.json with settings upload")

        
    def add_item_table(self):
        pass
    
    def delete_item_table(self):
        pass

class DownloadTLE():

    def __init__(self):
        super().__init__()

        pass
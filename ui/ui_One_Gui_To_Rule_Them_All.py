# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'One_GUI_To_Rule_Them_All.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.main_action_restore = QAction(MainWindow)
        self.main_action_restore.setObjectName(u"main_action_restore")
        self.main_action_devices = QAction(MainWindow)
        self.main_action_devices.setObjectName(u"main_action_devices")
        self.main_action_connect = QAction(MainWindow)
        self.main_action_connect.setObjectName(u"main_action_connect")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.sas_tab = QWidget()
        self.sas_tab.setObjectName(u"sas_tab")
        self.gridLayout_9 = QGridLayout(self.sas_tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.sas_butt_off = QPushButton(self.sas_tab)
        self.sas_butt_off.setObjectName(u"sas_butt_off")
        self.sas_butt_off.setMinimumSize(QSize(80, 0))
        self.sas_butt_off.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_8.addWidget(self.sas_butt_off, 2, 3, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.sas_butt_on = QPushButton(self.sas_tab)
        self.sas_butt_on.setObjectName(u"sas_butt_on")
        self.sas_butt_on.setMinimumSize(QSize(80, 0))
        self.sas_butt_on.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_8.addWidget(self.sas_butt_on, 2, 1, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.sas_butt_close = QPushButton(self.sas_tab)
        self.sas_butt_close.setObjectName(u"sas_butt_close")
        self.sas_butt_close.setMinimumSize(QSize(80, 0))
        self.sas_butt_close.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_8.addWidget(self.sas_butt_close, 2, 4, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label_14 = QLabel(self.sas_tab)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_14)

        self.sas_entry_vmp = QDoubleSpinBox(self.sas_tab)
        self.sas_entry_vmp.setObjectName(u"sas_entry_vmp")
        self.sas_entry_vmp.setMinimumSize(QSize(50, 0))
        self.sas_entry_vmp.setMaximumSize(QSize(16777215, 16777215))
        self.sas_entry_vmp.setFrame(True)
        self.sas_entry_vmp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.sas_entry_vmp.setAccelerated(False)
        self.sas_entry_vmp.setDecimals(1)
        self.sas_entry_vmp.setMaximum(999.899999999999977)
        self.sas_entry_vmp.setValue(32.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sas_entry_vmp)

        self.label_15 = QLabel(self.sas_tab)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_15)

        self.sas_entry_pmp = QDoubleSpinBox(self.sas_tab)
        self.sas_entry_pmp.setObjectName(u"sas_entry_pmp")
        self.sas_entry_pmp.setMinimumSize(QSize(50, 0))
        self.sas_entry_pmp.setMaximumSize(QSize(16777215, 16777215))
        self.sas_entry_pmp.setFrame(True)
        self.sas_entry_pmp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.sas_entry_pmp.setAccelerated(False)
        self.sas_entry_pmp.setDecimals(1)
        self.sas_entry_pmp.setMaximum(1000.000000000000000)
        self.sas_entry_pmp.setValue(100.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sas_entry_pmp)

        self.label_16 = QLabel(self.sas_tab)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_16)

        self.sas_entry_ff = QDoubleSpinBox(self.sas_tab)
        self.sas_entry_ff.setObjectName(u"sas_entry_ff")
        self.sas_entry_ff.setMinimumSize(QSize(50, 0))
        self.sas_entry_ff.setMaximumSize(QSize(16777215, 16777215))
        self.sas_entry_ff.setFrame(True)
        self.sas_entry_ff.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.sas_entry_ff.setAccelerated(False)
        self.sas_entry_ff.setMaximum(999.899999999999977)
        self.sas_entry_ff.setValue(0.780000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sas_entry_ff)

        self.label_17 = QLabel(self.sas_tab)
        self.label_17.setObjectName(u"label_17")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_17)

        self.sas_entry_irrad = QDoubleSpinBox(self.sas_tab)
        self.sas_entry_irrad.setObjectName(u"sas_entry_irrad")
        self.sas_entry_irrad.setMinimumSize(QSize(50, 0))
        self.sas_entry_irrad.setMaximumSize(QSize(16777215, 16777215))
        self.sas_entry_irrad.setFrame(True)
        self.sas_entry_irrad.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.sas_entry_irrad.setAccelerated(False)
        self.sas_entry_irrad.setMaximum(999.990000000000009)
        self.sas_entry_irrad.setValue(1.000000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.sas_entry_irrad)


        self.gridLayout_8.addLayout(self.formLayout, 0, 0, 1, 2)

        self.sas_butt_apply = QPushButton(self.sas_tab)
        self.sas_butt_apply.setObjectName(u"sas_butt_apply")
        self.sas_butt_apply.setMinimumSize(QSize(80, 0))
        self.sas_butt_apply.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_8.addWidget(self.sas_butt_apply, 2, 0, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.sas_plot = PlotWidget(self.sas_tab)
        self.sas_plot.setObjectName(u"sas_plot")

        self.gridLayout_8.addWidget(self.sas_plot, 0, 3, 2, 2)


        self.gridLayout_9.addLayout(self.gridLayout_8, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_9.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.sas_tab, "")
        self.ac_tab = QWidget()
        self.ac_tab.setObjectName(u"ac_tab")
        self.gridLayout_2 = QGridLayout(self.ac_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.ac_entry_step_size = QSpinBox(self.ac_tab)
        self.ac_entry_step_size.setObjectName(u"ac_entry_step_size")
        self.ac_entry_step_size.setMinimumSize(QSize(50, 0))
        self.ac_entry_step_size.setMaximum(999)
        self.ac_entry_step_size.setValue(1)

        self.gridLayout.addWidget(self.ac_entry_step_size, 4, 5, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.ac_butt_close = QPushButton(self.ac_tab)
        self.ac_butt_close.setObjectName(u"ac_butt_close")
        self.ac_butt_close.setMinimumSize(QSize(80, 0))
        self.ac_butt_close.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.ac_butt_close, 6, 6, 1, 2, Qt.AlignHCenter)

        self.ac_butt_off = QPushButton(self.ac_tab)
        self.ac_butt_off.setObjectName(u"ac_butt_off")
        self.ac_butt_off.setMinimumSize(QSize(80, 0))
        self.ac_butt_off.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.ac_butt_off, 6, 4, 1, 2, Qt.AlignHCenter)

        self.ac_entry_freq = QSpinBox(self.ac_tab)
        self.ac_entry_freq.setObjectName(u"ac_entry_freq")
        self.ac_entry_freq.setMinimumSize(QSize(50, 0))
        self.ac_entry_freq.setMaximum(999)
        self.ac_entry_freq.setValue(60)

        self.gridLayout.addWidget(self.ac_entry_freq, 4, 1, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.ac_entry_ac_volts = QSpinBox(self.ac_tab)
        self.ac_entry_ac_volts.setObjectName(u"ac_entry_ac_volts")
        self.ac_entry_ac_volts.setMinimumSize(QSize(50, 0))
        self.ac_entry_ac_volts.setMaximum(999)
        self.ac_entry_ac_volts.setValue(240)

        self.gridLayout.addWidget(self.ac_entry_ac_volts, 4, 3, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.label_2 = QLabel(self.ac_tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 3, 3, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.horizontalSpacer = QSpacerItem(47, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 7, 1, 1)

        self.ac_butt_on = QPushButton(self.ac_tab)
        self.ac_butt_on.setObjectName(u"ac_butt_on")
        self.ac_butt_on.setMinimumSize(QSize(80, 0))
        self.ac_butt_on.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.ac_butt_on, 6, 2, 1, 2, Qt.AlignHCenter)

        self.label_3 = QLabel(self.ac_tab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 3, 5, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.label = QLabel(self.ac_tab)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 3, 1, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.horizontalSpacer_2 = QSpacerItem(47, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 4, 0, 1, 1)

        self.ac_butt_apply = QPushButton(self.ac_tab)
        self.ac_butt_apply.setObjectName(u"ac_butt_apply")
        self.ac_butt_apply.setMinimumSize(QSize(80, 0))
        self.ac_butt_apply.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.ac_butt_apply, 6, 0, 1, 2, Qt.AlignHCenter)

        self.ac_radio_split = QRadioButton(self.ac_tab)
        self.ac_radio_split.setObjectName(u"ac_radio_split")

        self.gridLayout.addWidget(self.ac_radio_split, 0, 0, 1, 4, Qt.AlignHCenter)

        self.ac_radio_single = QRadioButton(self.ac_tab)
        self.ac_radio_single.setObjectName(u"ac_radio_single")

        self.gridLayout.addWidget(self.ac_radio_single, 1, 0, 1, 4, Qt.AlignHCenter)

        self.ac_radio_three = QRadioButton(self.ac_tab)
        self.ac_radio_three.setObjectName(u"ac_radio_three")

        self.gridLayout.addWidget(self.ac_radio_three, 2, 0, 1, 4, Qt.AlignHCenter)

        self.ac_check_abnormal = QCheckBox(self.ac_tab)
        self.ac_check_abnormal.setObjectName(u"ac_check_abnormal")

        self.gridLayout.addWidget(self.ac_check_abnormal, 2, 4, 1, 4, Qt.AlignHCenter)

        self.ac_menu_abnormal = QComboBox(self.ac_tab)
        self.ac_menu_abnormal.setObjectName(u"ac_menu_abnormal")
        self.ac_menu_abnormal.setMaximumSize(QSize(234, 16777215))

        self.gridLayout.addWidget(self.ac_menu_abnormal, 1, 4, 1, 4, Qt.AlignHCenter)

        self.ac_menu_phase = QComboBox(self.ac_tab)
        self.ac_menu_phase.setObjectName(u"ac_menu_phase")

        self.gridLayout.addWidget(self.ac_menu_phase, 0, 4, 1, 4, Qt.AlignHCenter)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.tabWidget.addTab(self.ac_tab, "")
        self.scope_tab = QWidget()
        self.scope_tab.setObjectName(u"scope_tab")
        self.gridLayout_6 = QGridLayout(self.scope_tab)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.scope_butt_close = QPushButton(self.scope_tab)
        self.scope_butt_close.setObjectName(u"scope_butt_close")
        self.scope_butt_close.setMinimumSize(QSize(80, 0))
        self.scope_butt_close.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_3.addWidget(self.scope_butt_close, 5, 4, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.scope_line_ch4_lab = QLineEdit(self.scope_tab)
        self.scope_line_ch4_lab.setObjectName(u"scope_line_ch4_lab")
        self.scope_line_ch4_lab.setMinimumSize(QSize(90, 0))

        self.gridLayout_3.addWidget(self.scope_line_ch4_lab, 1, 5, 1, 1, Qt.AlignHCenter|Qt.AlignTop)

        self.scope_line_ch1_lab = QLineEdit(self.scope_tab)
        self.scope_line_ch1_lab.setObjectName(u"scope_line_ch1_lab")
        self.scope_line_ch1_lab.setMinimumSize(QSize(90, 0))

        self.gridLayout_3.addWidget(self.scope_line_ch1_lab, 1, 0, 1, 1, Qt.AlignHCenter|Qt.AlignTop)

        self.label_4 = QLabel(self.scope_tab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 3, Qt.AlignHCenter|Qt.AlignBottom)

        self.scope_line_ch3_lab = QLineEdit(self.scope_tab)
        self.scope_line_ch3_lab.setObjectName(u"scope_line_ch3_lab")
        self.scope_line_ch3_lab.setMinimumSize(QSize(90, 0))

        self.gridLayout_3.addWidget(self.scope_line_ch3_lab, 1, 3, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.label_8 = QLabel(self.scope_tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(100, 0))
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_8, 0, 3, 1, 2, Qt.AlignBottom)

        self.scope_butt_cap = QPushButton(self.scope_tab)
        self.scope_butt_cap.setObjectName(u"scope_butt_cap")
        self.scope_butt_cap.setMinimumSize(QSize(80, 0))
        self.scope_butt_cap.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_3.addWidget(self.scope_butt_cap, 5, 2, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.scope_line_ch2_lab = QLineEdit(self.scope_tab)
        self.scope_line_ch2_lab.setObjectName(u"scope_line_ch2_lab")
        self.scope_line_ch2_lab.setMinimumSize(QSize(90, 0))

        self.gridLayout_3.addWidget(self.scope_line_ch2_lab, 1, 1, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.scope_butt_apply = QPushButton(self.scope_tab)
        self.scope_butt_apply.setObjectName(u"scope_butt_apply")
        self.scope_butt_apply.setMinimumSize(QSize(80, 0))
        self.scope_butt_apply.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_3.addWidget(self.scope_butt_apply, 5, 0, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.scope_check_auto = QCheckBox(self.scope_tab)
        self.scope_check_auto.setObjectName(u"scope_check_auto")
        self.scope_check_auto.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.scope_check_auto, 4, 4, 1, 2, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label_5 = QLabel(self.scope_tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_5, 2, 3, 1, 3, Qt.AlignHCenter|Qt.AlignBottom)

        self.label_9 = QLabel(self.scope_tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(100, 0))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_9, 0, 5, 1, 1, Qt.AlignBottom)

        self.label_6 = QLabel(self.scope_tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(100, 0))
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1, Qt.AlignBottom)

        self.scope_check_invert = QCheckBox(self.scope_tab)
        self.scope_check_invert.setObjectName(u"scope_check_invert")
        self.scope_check_invert.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.scope_check_invert, 4, 2, 1, 2, Qt.AlignHCenter|Qt.AlignVCenter)

        self.scope_check_date = QCheckBox(self.scope_tab)
        self.scope_check_date.setObjectName(u"scope_check_date")
        self.scope_check_date.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.scope_check_date, 4, 0, 1, 2, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label_7 = QLabel(self.scope_tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(100, 0))
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_7, 0, 1, 1, 2, Qt.AlignBottom)

        self.scope_butt_browse = QPushButton(self.scope_tab)
        self.scope_butt_browse.setObjectName(u"scope_butt_browse")
        self.scope_butt_browse.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_3.addWidget(self.scope_butt_browse, 3, 2, 1, 1)

        self.scope_line_cap_name = QLineEdit(self.scope_tab)
        self.scope_line_cap_name.setObjectName(u"scope_line_cap_name")
        self.scope_line_cap_name.setMinimumSize(QSize(180, 0))

        self.gridLayout_3.addWidget(self.scope_line_cap_name, 3, 3, 1, 3, Qt.AlignHCenter|Qt.AlignTop)

        self.scope_line_cap_path = QLineEdit(self.scope_tab)
        self.scope_line_cap_path.setObjectName(u"scope_line_cap_path")
        self.scope_line_cap_path.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.scope_line_cap_path, 3, 0, 1, 2)


        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.scope_tab, "")
        self.rlc_tab = QWidget()
        self.rlc_tab.setObjectName(u"rlc_tab")
        self.gridLayout_5 = QGridLayout(self.rlc_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_12 = QLabel(self.rlc_tab)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(100, 0))
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_12, 0, 3, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.label_11 = QLabel(self.rlc_tab)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(100, 0))
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_11, 0, 1, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.rlc_entry_freq = QSpinBox(self.rlc_tab)
        self.rlc_entry_freq.setObjectName(u"rlc_entry_freq")
        self.rlc_entry_freq.setMinimumSize(QSize(50, 0))
        self.rlc_entry_freq.setMaximum(999)
        self.rlc_entry_freq.setValue(60)

        self.gridLayout_4.addWidget(self.rlc_entry_freq, 1, 0, 1, 1, Qt.AlignHCenter|Qt.AlignTop)

        self.label_13 = QLabel(self.rlc_tab)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(100, 0))
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_13, 0, 5, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.label_10 = QLabel(self.rlc_tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 0))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.rlc_entry_reactive_pwr = QSpinBox(self.rlc_tab)
        self.rlc_entry_reactive_pwr.setObjectName(u"rlc_entry_reactive_pwr")
        self.rlc_entry_reactive_pwr.setMinimumSize(QSize(50, 0))
        self.rlc_entry_reactive_pwr.setMaximum(999)

        self.gridLayout_4.addWidget(self.rlc_entry_reactive_pwr, 1, 5, 1, 1, Qt.AlignHCenter|Qt.AlignTop)

        self.rlc_butt_off = QPushButton(self.rlc_tab)
        self.rlc_butt_off.setObjectName(u"rlc_butt_off")
        self.rlc_butt_off.setMinimumSize(QSize(80, 0))
        self.rlc_butt_off.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_4.addWidget(self.rlc_butt_off, 2, 2, 1, 2, Qt.AlignHCenter)

        self.rlc_entry_real_pwr = QSpinBox(self.rlc_tab)
        self.rlc_entry_real_pwr.setObjectName(u"rlc_entry_real_pwr")
        self.rlc_entry_real_pwr.setMinimumSize(QSize(50, 0))
        self.rlc_entry_real_pwr.setMaximum(999)

        self.gridLayout_4.addWidget(self.rlc_entry_real_pwr, 1, 3, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.rlc_entry_ac_volts = QSpinBox(self.rlc_tab)
        self.rlc_entry_ac_volts.setObjectName(u"rlc_entry_ac_volts")
        self.rlc_entry_ac_volts.setMinimumSize(QSize(50, 0))
        self.rlc_entry_ac_volts.setMaximum(999)
        self.rlc_entry_ac_volts.setValue(240)

        self.gridLayout_4.addWidget(self.rlc_entry_ac_volts, 1, 1, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.rlc_butt_on = QPushButton(self.rlc_tab)
        self.rlc_butt_on.setObjectName(u"rlc_butt_on")
        self.rlc_butt_on.setMinimumSize(QSize(80, 0))
        self.rlc_butt_on.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_4.addWidget(self.rlc_butt_on, 2, 0, 1, 2, Qt.AlignHCenter)

        self.rlc_butt_close = QPushButton(self.rlc_tab)
        self.rlc_butt_close.setObjectName(u"rlc_butt_close")
        self.rlc_butt_close.setMinimumSize(QSize(80, 0))
        self.rlc_butt_close.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_4.addWidget(self.rlc_butt_close, 2, 4, 1, 2, Qt.AlignHCenter)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.rlc_tab, "")

        self.gridLayout_7.addWidget(self.tabWidget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 600, 22))
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuOptions.addAction(self.main_action_restore)
        self.menuOptions.addAction(self.main_action_devices)
        self.menuOptions.addAction(self.main_action_connect)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"One Gui To Rule Them All", None))
        self.main_action_restore.setText(QCoreApplication.translate("MainWindow", u"Restore Defaults", None))
        self.main_action_devices.setText(QCoreApplication.translate("MainWindow", u"Configure Equipment", None))
        self.main_action_connect.setText(QCoreApplication.translate("MainWindow", u"Reconnect Equipment", None))
        self.sas_butt_off.setText(QCoreApplication.translate("MainWindow", u"SAS Off", None))
        self.sas_butt_on.setText(QCoreApplication.translate("MainWindow", u"SAS On", None))
        self.sas_butt_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Vmp", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Pmp", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Fill Factor", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Irradiance", None))
        self.sas_butt_apply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sas_tab), QCoreApplication.translate("MainWindow", u"SAS", None))
        self.ac_butt_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.ac_butt_off.setText(QCoreApplication.translate("MainWindow", u"AC Off", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"AC Voltage (Vrms)", None))
        self.ac_butt_on.setText(QCoreApplication.translate("MainWindow", u"AC On", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Step Size", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.ac_butt_apply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.ac_radio_split.setText(QCoreApplication.translate("MainWindow", u"Split Phase", None))
        self.ac_radio_single.setText(QCoreApplication.translate("MainWindow", u"Single Phase", None))
        self.ac_radio_three.setText(QCoreApplication.translate("MainWindow", u"Three Phase", None))
        self.ac_check_abnormal.setText(QCoreApplication.translate("MainWindow", u"Abnormal Waveform", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ac_tab), QCoreApplication.translate("MainWindow", u"AC Source", None))
        self.scope_butt_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Capture Path", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"CH3 Label", None))
        self.scope_butt_cap.setText(QCoreApplication.translate("MainWindow", u"Capture", None))
        self.scope_butt_apply.setText(QCoreApplication.translate("MainWindow", u"Apply Labels", None))
        self.scope_check_auto.setText(QCoreApplication.translate("MainWindow", u"Auto Capture", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Capture Name", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"CH4 Label", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"CH1 Label", None))
        self.scope_check_invert.setText(QCoreApplication.translate("MainWindow", u"Invert Colours", None))
        self.scope_check_date.setText(QCoreApplication.translate("MainWindow", u"Date Prefix", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"CH2 Label", None))
        self.scope_butt_browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scope_tab), QCoreApplication.translate("MainWindow", u"Scope", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Real Power\n"
"(W)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"AC Voltage\n"
"(Vrms)", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Reactive Pwr\n"
"(Vars)", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Frequency\n"
"(Hz)", None))
        self.rlc_butt_off.setText(QCoreApplication.translate("MainWindow", u"RLC off", None))
        self.rlc_butt_on.setText(QCoreApplication.translate("MainWindow", u"RLC on", None))
        self.rlc_butt_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rlc_tab), QCoreApplication.translate("MainWindow", u"RLC", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'One_GUI_To_Rule_Them_All.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QStatusBar, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_pps = QWidget()
        self.tab_pps.setObjectName(u"tab_pps")
        self.gridLayout_2 = QGridLayout(self.tab_pps)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.radio_single = QRadioButton(self.tab_pps)
        self.radio_single.setObjectName(u"radio_single")

        self.gridLayout.addWidget(self.radio_single, 1, 0, 1, 3)

        self.radio_three = QRadioButton(self.tab_pps)
        self.radio_three.setObjectName(u"radio_three")

        self.gridLayout.addWidget(self.radio_three, 2, 0, 1, 3)

        self.check_abnormal = QCheckBox(self.tab_pps)
        self.check_abnormal.setObjectName(u"check_abnormal")

        self.gridLayout.addWidget(self.check_abnormal, 2, 3, 1, 3)

        self.label = QLabel(self.tab_pps)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 2)

        self.label_2 = QLabel(self.tab_pps)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 2, 1, 2)

        self.label_3 = QLabel(self.tab_pps)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 4, 1, 2)

        self.entry_freq = QSpinBox(self.tab_pps)
        self.entry_freq.setObjectName(u"entry_freq")
        self.entry_freq.setMaximum(999)

        self.gridLayout.addWidget(self.entry_freq, 4, 0, 1, 2)

        self.entry_ac_volts = QSpinBox(self.tab_pps)
        self.entry_ac_volts.setObjectName(u"entry_ac_volts")
        self.entry_ac_volts.setMaximum(999)

        self.gridLayout.addWidget(self.entry_ac_volts, 4, 2, 1, 2)

        self.entry_step_size = QSpinBox(self.tab_pps)
        self.entry_step_size.setObjectName(u"entry_step_size")
        self.entry_step_size.setMaximum(999)

        self.gridLayout.addWidget(self.entry_step_size, 4, 4, 1, 2)

        self.butt_apply = QPushButton(self.tab_pps)
        self.butt_apply.setObjectName(u"butt_apply")

        self.gridLayout.addWidget(self.butt_apply, 5, 0, 1, 1)

        self.butt_ac_on = QPushButton(self.tab_pps)
        self.butt_ac_on.setObjectName(u"butt_ac_on")

        self.gridLayout.addWidget(self.butt_ac_on, 5, 1, 1, 2)

        self.butt_ac_off = QPushButton(self.tab_pps)
        self.butt_ac_off.setObjectName(u"butt_ac_off")

        self.gridLayout.addWidget(self.butt_ac_off, 5, 3, 1, 2)

        self.butt_close = QPushButton(self.tab_pps)
        self.butt_close.setObjectName(u"butt_close")

        self.gridLayout.addWidget(self.butt_close, 5, 5, 1, 1)

        self.radio_split = QRadioButton(self.tab_pps)
        self.radio_split.setObjectName(u"radio_split")

        self.gridLayout.addWidget(self.radio_split, 0, 0, 1, 3)

        self.menu_phase = QComboBox(self.tab_pps)
        self.menu_phase.setObjectName(u"menu_phase")

        self.gridLayout.addWidget(self.menu_phase, 0, 3, 1, 3)

        self.menu_abnormal = QComboBox(self.tab_pps)
        self.menu_abnormal.setObjectName(u"menu_abnormal")

        self.gridLayout.addWidget(self.menu_abnormal, 1, 3, 1, 3)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_pps, "")
        self.tab_scope = QWidget()
        self.tab_scope.setObjectName(u"tab_scope")
        self.gridLayout_6 = QGridLayout(self.tab_scope)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_6 = QLabel(self.tab_scope)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_7 = QLabel(self.tab_scope)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 1, 1, 2)

        self.label_8 = QLabel(self.tab_scope)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 3, 1, 2)

        self.label_9 = QLabel(self.tab_scope)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 0, 5, 1, 1)

        self.line_ch1_lab = QLineEdit(self.tab_scope)
        self.line_ch1_lab.setObjectName(u"line_ch1_lab")

        self.gridLayout_3.addWidget(self.line_ch1_lab, 1, 0, 1, 1)

        self.line_ch2_lab = QLineEdit(self.tab_scope)
        self.line_ch2_lab.setObjectName(u"line_ch2_lab")

        self.gridLayout_3.addWidget(self.line_ch2_lab, 1, 1, 1, 2)

        self.line_ch3_lab = QLineEdit(self.tab_scope)
        self.line_ch3_lab.setObjectName(u"line_ch3_lab")

        self.gridLayout_3.addWidget(self.line_ch3_lab, 1, 3, 1, 2)

        self.line_ch4_lab = QLineEdit(self.tab_scope)
        self.line_ch4_lab.setObjectName(u"line_ch4_lab")

        self.gridLayout_3.addWidget(self.line_ch4_lab, 1, 5, 1, 1)

        self.label_4 = QLabel(self.tab_scope)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 3)

        self.label_5 = QLabel(self.tab_scope)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 2, 3, 1, 3)

        self.line_cap_path = QLineEdit(self.tab_scope)
        self.line_cap_path.setObjectName(u"line_cap_path")

        self.gridLayout_3.addWidget(self.line_cap_path, 3, 0, 1, 3)

        self.line_cap_name = QLineEdit(self.tab_scope)
        self.line_cap_name.setObjectName(u"line_cap_name")

        self.gridLayout_3.addWidget(self.line_cap_name, 3, 3, 1, 3)

        self.check_date = QCheckBox(self.tab_scope)
        self.check_date.setObjectName(u"check_date")

        self.gridLayout_3.addWidget(self.check_date, 4, 0, 1, 2)

        self.check_invert = QCheckBox(self.tab_scope)
        self.check_invert.setObjectName(u"check_invert")

        self.gridLayout_3.addWidget(self.check_invert, 4, 2, 1, 2)

        self.check_auto = QCheckBox(self.tab_scope)
        self.check_auto.setObjectName(u"check_auto")

        self.gridLayout_3.addWidget(self.check_auto, 4, 4, 1, 2)

        self.butt_apply_lab = QPushButton(self.tab_scope)
        self.butt_apply_lab.setObjectName(u"butt_apply_lab")

        self.gridLayout_3.addWidget(self.butt_apply_lab, 5, 0, 1, 2)

        self.butt_cap = QPushButton(self.tab_scope)
        self.butt_cap.setObjectName(u"butt_cap")

        self.gridLayout_3.addWidget(self.butt_cap, 5, 2, 1, 2)

        self.butt_close_3 = QPushButton(self.tab_scope)
        self.butt_close_3.setObjectName(u"butt_close_3")

        self.gridLayout_3.addWidget(self.butt_close_3, 5, 4, 1, 2)


        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_scope, "")
        self.tab_rlc = QWidget()
        self.tab_rlc.setObjectName(u"tab_rlc")
        self.gridLayout_5 = QGridLayout(self.tab_rlc)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_10 = QLabel(self.tab_rlc)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_11 = QLabel(self.tab_rlc)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 0, 1, 1, 2)

        self.label_12 = QLabel(self.tab_rlc)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 0, 3, 1, 2)

        self.label_13 = QLabel(self.tab_rlc)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 0, 5, 1, 1)

        self.line_freq = QLineEdit(self.tab_rlc)
        self.line_freq.setObjectName(u"line_freq")

        self.gridLayout_4.addWidget(self.line_freq, 1, 0, 1, 1)

        self.line_ac_volts = QLineEdit(self.tab_rlc)
        self.line_ac_volts.setObjectName(u"line_ac_volts")

        self.gridLayout_4.addWidget(self.line_ac_volts, 1, 1, 1, 2)

        self.line_real_pwr = QLineEdit(self.tab_rlc)
        self.line_real_pwr.setObjectName(u"line_real_pwr")

        self.gridLayout_4.addWidget(self.line_real_pwr, 1, 3, 1, 2)

        self.line_reactive_pwr = QLineEdit(self.tab_rlc)
        self.line_reactive_pwr.setObjectName(u"line_reactive_pwr")

        self.gridLayout_4.addWidget(self.line_reactive_pwr, 1, 5, 1, 1)

        self.butt_rlc_off = QPushButton(self.tab_rlc)
        self.butt_rlc_off.setObjectName(u"butt_rlc_off")

        self.gridLayout_4.addWidget(self.butt_rlc_off, 2, 2, 1, 2)

        self.butt_rlc_on = QPushButton(self.tab_rlc)
        self.butt_rlc_on.setObjectName(u"butt_rlc_on")

        self.gridLayout_4.addWidget(self.butt_rlc_on, 2, 0, 1, 1)

        self.butt_close_2 = QPushButton(self.tab_rlc)
        self.butt_close_2.setObjectName(u"butt_close_2")

        self.gridLayout_4.addWidget(self.butt_close_2, 2, 5, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_rlc, "")

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.radio_single.setText(QCoreApplication.translate("MainWindow", u"Single Phase", None))
        self.radio_three.setText(QCoreApplication.translate("MainWindow", u"Three Phase", None))
        self.check_abnormal.setText(QCoreApplication.translate("MainWindow", u"Abnormal Waveform", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"AC Voltage (Vrms)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Step Size", None))
        self.butt_apply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.butt_ac_on.setText(QCoreApplication.translate("MainWindow", u"AC On", None))
        self.butt_ac_off.setText(QCoreApplication.translate("MainWindow", u"AC Off", None))
        self.butt_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.radio_split.setText(QCoreApplication.translate("MainWindow", u"Split Phase", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pps), QCoreApplication.translate("MainWindow", u"PPS", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"CH1 Label", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"CH2 Label", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"CH3 Label", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"CH4 Label", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Capture Path", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Capture Name", None))
        self.check_date.setText(QCoreApplication.translate("MainWindow", u"Date Prefix", None))
        self.check_invert.setText(QCoreApplication.translate("MainWindow", u"Invert Colours", None))
        self.check_auto.setText(QCoreApplication.translate("MainWindow", u"Auto Capture", None))
        self.butt_apply_lab.setText(QCoreApplication.translate("MainWindow", u"Apply Labels", None))
        self.butt_cap.setText(QCoreApplication.translate("MainWindow", u"Capture", None))
        self.butt_close_3.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_scope), QCoreApplication.translate("MainWindow", u"Scope", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"AC Voltage (Vrms)", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Real Power (W)", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Reactive Power (Vars)", None))
        self.butt_rlc_off.setText(QCoreApplication.translate("MainWindow", u"RLC off", None))
        self.butt_rlc_on.setText(QCoreApplication.translate("MainWindow", u"RLC on", None))
        self.butt_close_2.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_rlc), QCoreApplication.translate("MainWindow", u"RLC", None))
    # retranslateUi


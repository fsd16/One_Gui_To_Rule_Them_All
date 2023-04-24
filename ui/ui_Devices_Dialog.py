# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Devices_Dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QWidget)

class Ui_DevicesDialog(object):
    def setupUi(self, DevicesDialog):
        if not DevicesDialog.objectName():
            DevicesDialog.setObjectName(u"DevicesDialog")
        DevicesDialog.resize(523, 345)
        self.gridLayout_2 = QGridLayout(DevicesDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.sas_entry_device = QLineEdit(DevicesDialog)
        self.sas_entry_device.setObjectName(u"sas_entry_device")

        self.gridLayout.addWidget(self.sas_entry_device, 3, 2, 1, 1)

        self.label = QLabel(DevicesDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(DevicesDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_2 = QLabel(DevicesDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_4 = QLabel(DevicesDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.sas_menu_config = QComboBox(DevicesDialog)
        self.sas_menu_config.setObjectName(u"sas_menu_config")

        self.gridLayout.addWidget(self.sas_menu_config, 4, 2, 1, 1)

        self.scope_entry_device = QLineEdit(DevicesDialog)
        self.scope_entry_device.setObjectName(u"scope_entry_device")

        self.gridLayout.addWidget(self.scope_entry_device, 1, 2, 1, 1)

        self.ac_entry_device = QLineEdit(DevicesDialog)
        self.ac_entry_device.setObjectName(u"ac_entry_device")

        self.gridLayout.addWidget(self.ac_entry_device, 0, 2, 1, 1)

        self.rlc_entry_device = QLineEdit(DevicesDialog)
        self.rlc_entry_device.setObjectName(u"rlc_entry_device")

        self.gridLayout.addWidget(self.rlc_entry_device, 2, 2, 1, 1)

        self.ac_menu_driver = QComboBox(DevicesDialog)
        self.ac_menu_driver.setObjectName(u"ac_menu_driver")

        self.gridLayout.addWidget(self.ac_menu_driver, 0, 1, 1, 1)

        self.scope_menu_driver = QComboBox(DevicesDialog)
        self.scope_menu_driver.setObjectName(u"scope_menu_driver")

        self.gridLayout.addWidget(self.scope_menu_driver, 1, 1, 1, 1)

        self.rlc_menu_driver = QComboBox(DevicesDialog)
        self.rlc_menu_driver.setObjectName(u"rlc_menu_driver")

        self.gridLayout.addWidget(self.rlc_menu_driver, 2, 1, 1, 1)

        self.sas_menu_driver = QComboBox(DevicesDialog)
        self.sas_menu_driver.setObjectName(u"sas_menu_driver")

        self.gridLayout.addWidget(self.sas_menu_driver, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)

        self.device_entry_startup = QCheckBox(DevicesDialog)
        self.device_entry_startup.setObjectName(u"device_entry_startup")
        self.device_entry_startup.setChecked(True)

        self.gridLayout_2.addWidget(self.device_entry_startup, 3, 0, 1, 2)

        self.buttonBox = QDialogButtonBox(DevicesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)


        self.retranslateUi(DevicesDialog)
        self.buttonBox.accepted.connect(DevicesDialog.accept)
        self.buttonBox.rejected.connect(DevicesDialog.reject)

        QMetaObject.connectSlotsByName(DevicesDialog)
    # setupUi

    def retranslateUi(self, DevicesDialog):
        DevicesDialog.setWindowTitle(QCoreApplication.translate("DevicesDialog", u"Device Connection", None))
        self.sas_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"GPIB0::<address>::INSTR", None))
        self.label.setText(QCoreApplication.translate("DevicesDialog", u"AC Source", None))
        self.label_3.setText(QCoreApplication.translate("DevicesDialog", u"RLC Load", None))
        self.label_2.setText(QCoreApplication.translate("DevicesDialog", u"Scope", None))
        self.label_4.setText(QCoreApplication.translate("DevicesDialog", u"SAS", None))
        self.sas_menu_config.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"Cluster Config", None))
        self.scope_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"GPIB0::<address>::INSTR", None))
        self.ac_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"GPIB0::<address>::INSTR", None))
        self.rlc_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"COM<address>,COM<address>", None))
        self.ac_menu_driver.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"Select Driver", None))
        self.scope_menu_driver.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"Select Driver", None))
        self.rlc_menu_driver.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"Select Driver", None))
        self.sas_menu_driver.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"Select Driver", None))
        self.device_entry_startup.setText(QCoreApplication.translate("DevicesDialog", u"Show on Startup", None))
    # retranslateUi


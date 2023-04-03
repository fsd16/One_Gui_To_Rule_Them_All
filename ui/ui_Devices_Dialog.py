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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(259, 196)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.device_entry_startup = QCheckBox(Dialog)
        self.device_entry_startup.setObjectName(u"device_entry_startup")
        self.device_entry_startup.setChecked(True)

        self.gridLayout.addWidget(self.device_entry_startup, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.ac_entry_device = QLineEdit(Dialog)
        self.ac_entry_device.setObjectName(u"ac_entry_device")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ac_entry_device)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.scope_entry_device = QLineEdit(Dialog)
        self.scope_entry_device.setObjectName(u"scope_entry_device")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.scope_entry_device)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.rlc_entry_device = QLineEdit(Dialog)
        self.rlc_entry_device.setObjectName(u"rlc_entry_device")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.rlc_entry_device)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.sas_entry_device = QLineEdit(Dialog)
        self.sas_entry_device.setObjectName(u"sas_entry_device")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.sas_entry_device)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)


        self.gridLayout.addLayout(self.formLayout, 2, 0, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Device Connection", None))
        self.device_entry_startup.setText(QCoreApplication.translate("Dialog", u"Show on Startup", None))
        self.ac_entry_device.setPlaceholderText(QCoreApplication.translate("Dialog", u"GPIB0::<address>::INSTR", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Scope", None))
        self.scope_entry_device.setPlaceholderText(QCoreApplication.translate("Dialog", u"GPIB0::<address>::INSTR", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"RLC Load", None))
        self.rlc_entry_device.setPlaceholderText(QCoreApplication.translate("Dialog", u"COM<address>,COM<address>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"SAS", None))
        self.sas_entry_device.setPlaceholderText(QCoreApplication.translate("Dialog", u"GPIB0::<address>::INSTR", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"AC Source", None))
    # retranslateUi


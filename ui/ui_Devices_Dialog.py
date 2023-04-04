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

class Ui_DevicesDialog(object):
    def setupUi(self, DevicesDialog):
        if not DevicesDialog.objectName():
            DevicesDialog.setObjectName(u"DevicesDialog")
        DevicesDialog.resize(259, 222)
        self.gridLayout = QGridLayout(DevicesDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.device_entry_startup = QCheckBox(DevicesDialog)
        self.device_entry_startup.setObjectName(u"device_entry_startup")
        self.device_entry_startup.setChecked(True)

        self.gridLayout.addWidget(self.device_entry_startup, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DevicesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label = QLabel(DevicesDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.ac_entry_device = QLineEdit(DevicesDialog)
        self.ac_entry_device.setObjectName(u"ac_entry_device")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ac_entry_device)

        self.label_2 = QLabel(DevicesDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.scope_entry_device = QLineEdit(DevicesDialog)
        self.scope_entry_device.setObjectName(u"scope_entry_device")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.scope_entry_device)

        self.label_3 = QLabel(DevicesDialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.rlc_entry_device = QLineEdit(DevicesDialog)
        self.rlc_entry_device.setObjectName(u"rlc_entry_device")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.rlc_entry_device)

        self.label_4 = QLabel(DevicesDialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_4)

        self.sas_entry_device = QLineEdit(DevicesDialog)
        self.sas_entry_device.setObjectName(u"sas_entry_device")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.sas_entry_device)


        self.gridLayout.addLayout(self.formLayout, 2, 0, 1, 1)


        self.retranslateUi(DevicesDialog)
        self.buttonBox.accepted.connect(DevicesDialog.accept)
        self.buttonBox.rejected.connect(DevicesDialog.reject)

        QMetaObject.connectSlotsByName(DevicesDialog)
    # setupUi

    def retranslateUi(self, DevicesDialog):
        DevicesDialog.setWindowTitle(QCoreApplication.translate("DevicesDialog", u"Device Connection", None))
        self.device_entry_startup.setText(QCoreApplication.translate("DevicesDialog", u"Show on Startup", None))
        self.label.setText(QCoreApplication.translate("DevicesDialog", u"AC Source", None))
        self.ac_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"GPIB0::<address>::INSTR", None))
        self.label_2.setText(QCoreApplication.translate("DevicesDialog", u"Scope", None))
        self.scope_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"GPIB0::<address>::INSTR", None))
        self.label_3.setText(QCoreApplication.translate("DevicesDialog", u"RLC Load", None))
        self.rlc_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"COM<address>,COM<address>", None))
        self.label_4.setText(QCoreApplication.translate("DevicesDialog", u"SAS", None))
        self.sas_entry_device.setPlaceholderText(QCoreApplication.translate("DevicesDialog", u"GPIB0::<address>::INSTR", None))
    # retranslateUi


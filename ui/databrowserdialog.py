# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/databrowserdialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DataBrowserDialog(object):
    def setupUi(self, DataBrowserDialog):
        DataBrowserDialog.setObjectName(_fromUtf8("DataBrowserDialog"))
        DataBrowserDialog.resize(780, 562)
        self.gridLayout = QtGui.QGridLayout(DataBrowserDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(DataBrowserDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.nameEdit = QtGui.QLineEdit(DataBrowserDialog)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridLayout.addWidget(self.nameEdit, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(DataBrowserDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.dateTimeEdit = QtGui.QDateTimeEdit(DataBrowserDialog)
        self.dateTimeEdit.setEnabled(False)
        self.dateTimeEdit.setDisplayFormat(_fromUtf8("dd/MM/yyyy"))
        self.dateTimeEdit.setCalendarPopup(False)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.gridLayout.addWidget(self.dateTimeEdit, 0, 4, 1, 1)
        self.projectCombo = QtGui.QComboBox(DataBrowserDialog)
        self.projectCombo.setObjectName(_fromUtf8("projectCombo"))
        self.gridLayout.addWidget(self.projectCombo, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(DataBrowserDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 5, 1, 1)
        self.channelNameEdit = QtGui.QLineEdit(DataBrowserDialog)
        self.channelNameEdit.setObjectName(_fromUtf8("channelNameEdit"))
        self.gridLayout.addWidget(self.channelNameEdit, 0, 6, 1, 1)
        self.sectionWidget = SectionWidget(DataBrowserDialog)
        self.sectionWidget.setObjectName(_fromUtf8("sectionWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.sectionWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout.addWidget(self.sectionWidget, 1, 0, 1, 7)

        self.retranslateUi(DataBrowserDialog)
        QtCore.QMetaObject.connectSlotsByName(DataBrowserDialog)

    def retranslateUi(self, DataBrowserDialog):
        DataBrowserDialog.setWindowTitle(_translate("DataBrowserDialog", "Wincan 2 QGEP", None))
        self.label.setText(_translate("DataBrowserDialog", "Nom", None))
        self.label_2.setText(_translate("DataBrowserDialog", "Date", None))
        self.label_3.setText(_translate("DataBrowserDialog", "Collecteur", None))

from ..gui.sectionwidget import SectionWidget

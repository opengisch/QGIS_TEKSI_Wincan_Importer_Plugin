# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/inspectionwidget.ui'
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

class Ui_InspectionWidget(object):
    def setupUi(self, InspectionWidget):
        InspectionWidget.setObjectName(_fromUtf8("InspectionWidget"))
        InspectionWidget.resize(543, 294)
        self.gridLayout = QtGui.QGridLayout(InspectionWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inspectionDirEdit = QtGui.QLineEdit(InspectionWidget)
        self.inspectionDirEdit.setObjectName(_fromUtf8("inspectionDirEdit"))
        self.gridLayout.addWidget(self.inspectionDirEdit, 2, 1, 1, 1)
        self.inspectionCombo = QtGui.QComboBox(InspectionWidget)
        self.inspectionCombo.setObjectName(_fromUtf8("inspectionCombo"))
        self.gridLayout.addWidget(self.inspectionCombo, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(InspectionWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(InspectionWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label = QtGui.QLabel(InspectionWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.inspMethodEdit = QtGui.QLineEdit(InspectionWidget)
        self.inspMethodEdit.setObjectName(_fromUtf8("inspMethodEdit"))
        self.gridLayout.addWidget(self.inspMethodEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(InspectionWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.inspectedLengthEdit = QtGui.QLineEdit(InspectionWidget)
        self.inspectedLengthEdit.setObjectName(_fromUtf8("inspectedLengthEdit"))
        self.gridLayout.addWidget(self.inspectedLengthEdit, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(InspectionWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.operatorEdit = QtGui.QLineEdit(InspectionWidget)
        self.operatorEdit.setObjectName(_fromUtf8("operatorEdit"))
        self.gridLayout.addWidget(self.operatorEdit, 2, 3, 1, 1)
        self.observationTable = ObservationTable(InspectionWidget)
        self.observationTable.setObjectName(_fromUtf8("observationTable"))
        self.observationTable.setColumnCount(0)
        self.observationTable.setRowCount(0)
        self.gridLayout.addWidget(self.observationTable, 3, 0, 1, 4)

        self.retranslateUi(InspectionWidget)
        QtCore.QMetaObject.connectSlotsByName(InspectionWidget)

    def retranslateUi(self, InspectionWidget):
        InspectionWidget.setWindowTitle(_translate("InspectionWidget", "Form", None))
        self.label_9.setText(_translate("InspectionWidget", "Inspection", None))
        self.label_4.setText(_translate("InspectionWidget", "Opérateur", None))
        self.label.setText(_translate("InspectionWidget", "Méthode", None))
        self.label_3.setText(_translate("InspectionWidget", "Longueur", None))
        self.label_2.setText(_translate("InspectionWidget", "Direction", None))

from ..gui.observationtable import ObservationTable

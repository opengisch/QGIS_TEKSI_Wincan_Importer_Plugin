# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/sectionwidget.ui'
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

class Ui_SectionWidget(object):
    def setupUi(self, SectionWidget):
        SectionWidget.setObjectName(_fromUtf8("SectionWidget"))
        SectionWidget.resize(649, 294)
        self.gridLayout = QtGui.QGridLayout(SectionWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.endNodeEdit = QtGui.QLineEdit(SectionWidget)
        self.endNodeEdit.setObjectName(_fromUtf8("endNodeEdit"))
        self.gridLayout.addWidget(self.endNodeEdit, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(SectionWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label = QtGui.QLabel(SectionWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(SectionWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(SectionWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.startNodeEdit = QtGui.QLineEdit(SectionWidget)
        self.startNodeEdit.setObjectName(_fromUtf8("startNodeEdit"))
        self.gridLayout.addWidget(self.startNodeEdit, 1, 1, 1, 1)
        self.inspectionWidget = InspectionWidget(SectionWidget)
        self.inspectionWidget.setObjectName(_fromUtf8("inspectionWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.inspectionWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout.addWidget(self.inspectionWidget, 6, 0, 1, 4)
        self.sectionlengthEdit = QtGui.QLineEdit(SectionWidget)
        self.sectionlengthEdit.setObjectName(_fromUtf8("sectionlengthEdit"))
        self.gridLayout.addWidget(self.sectionlengthEdit, 1, 3, 1, 1)
        self.sectionUseEdit = QtGui.QLineEdit(SectionWidget)
        self.sectionUseEdit.setObjectName(_fromUtf8("sectionUseEdit"))
        self.gridLayout.addWidget(self.sectionUseEdit, 2, 3, 1, 1)
        self.label_5 = QtGui.QLabel(SectionWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(SectionWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 2, 1, 1)
        self.label_8 = QtGui.QLabel(SectionWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 2, 1, 1)
        self.label_7 = QtGui.QLabel(SectionWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.pipeDiaEdit = QtGui.QLineEdit(SectionWidget)
        self.pipeDiaEdit.setObjectName(_fromUtf8("pipeDiaEdit"))
        self.gridLayout.addWidget(self.pipeDiaEdit, 3, 3, 1, 1)
        self.pipeMaterialEdit = QtGui.QLineEdit(SectionWidget)
        self.pipeMaterialEdit.setObjectName(_fromUtf8("pipeMaterialEdit"))
        self.gridLayout.addWidget(self.pipeMaterialEdit, 3, 1, 1, 1)
        self.profileEdit = QtGui.QLineEdit(SectionWidget)
        self.profileEdit.setObjectName(_fromUtf8("profileEdit"))
        self.gridLayout.addWidget(self.profileEdit, 4, 1, 1, 1)
        self.pipeWidthEdit = QtGui.QLineEdit(SectionWidget)
        self.pipeWidthEdit.setObjectName(_fromUtf8("pipeWidthEdit"))
        self.gridLayout.addWidget(self.pipeWidthEdit, 4, 3, 1, 1)
        self.sectionCombo = QtGui.QComboBox(SectionWidget)
        self.sectionCombo.setObjectName(_fromUtf8("sectionCombo"))
        self.gridLayout.addWidget(self.sectionCombo, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(SectionWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.sectionSelector = FeatureSelectorWidget(SectionWidget)
        self.sectionSelector.setObjectName(_fromUtf8("sectionSelector"))
        self.gridLayout.addWidget(self.sectionSelector, 0, 3, 1, 1)

        self.retranslateUi(SectionWidget)
        QtCore.QMetaObject.connectSlotsByName(SectionWidget)

    def retranslateUi(self, SectionWidget):
        SectionWidget.setWindowTitle(_translate("SectionWidget", "Form", None))
        self.label_4.setText(_translate("SectionWidget", "Utilisation", None))
        self.label.setText(_translate("SectionWidget", "Chambre départ", None))
        self.label_3.setText(_translate("SectionWidget", "Longueur", None))
        self.label_2.setText(_translate("SectionWidget", "Chambre arrivée", None))
        self.label_5.setText(_translate("SectionWidget", "Matériau", None))
        self.label_6.setText(_translate("SectionWidget", "Diameter", None))
        self.label_8.setText(_translate("SectionWidget", "Width", None))
        self.label_7.setText(_translate("SectionWidget", "Profile", None))
        self.label_9.setText(_translate("SectionWidget", "Section", None))

from ..gui.featureselectorwidget import FeatureSelectorWidget
from ..gui.inspectionwidget import InspectionWidget

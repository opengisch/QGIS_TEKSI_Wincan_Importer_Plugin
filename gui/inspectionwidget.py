#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------
#
# QGIS Quick Finder Plugin
# Copyright (C) 2013 Denis Rouzaud
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------


from collections import OrderedDict

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget

from wincan2qgep.core.mysettings import MySettings
from wincan2qgep.ui.inspectionwidget import Ui_InspectionWidget



class InspectionWidget(QWidget, Ui_InspectionWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.settings = MySettings()
        self.inspections = {}
        self.observations = {}

    def setInspections(self, inspections):
        self.inspectionCombo.clear()

        self.inspections = inspections

        for i_id, inspection in self.inspections.items():
            self.inspectionCombo.addItem(inspection['InspDate'].toString('dd.MM.yyyy'), i_id)


    @pyqtSlot(int)
    def on_inspectionCombo_currentIndexChanged(self, idx):

            self.inspMethodEdit.clear()
            self.inspectionDirEdit.clear()
            self.inspectedLengthEdit.clear()
            self.operatorEdit.clear()
            self.observationTable.clear()

            if idx < 0:
                return

            inspection = self.inspections[self.inspectionCombo.itemData(idx)]

            self.inspMethodEdit.setText(inspection['InspMethod'])
            self.inspectionDirEdit.setText(inspection['InspectionDir'])
            self.inspectedLengthEdit.setText('{}'.format(inspection['InspectedLength']))
            self.operatorEdit.setText(inspection['Operator'])

            self.observations = OrderedDict( sorted(inspection['Observations'].items(), key=lambda t: t[1]['Counter']) )

            self.observationTable.setObservations(self.observations)










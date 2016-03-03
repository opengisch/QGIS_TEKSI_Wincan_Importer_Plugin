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


from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog

from wincan2qgep.core.mysettings import MySettings
from wincan2qgep.ui.databrowserdialog import Ui_DataBrowserDialog


class DataBrowserDialog(QDialog, Ui_DataBrowserDialog):
    def __init__(self, iface, data):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        self.data = data

        self.sectionWidget.finishInit(iface, self.data)

        for p_id, project in self.data.items():
            self.projectCombo.addItem(project['Name'], p_id)

    @pyqtSlot(int)
    def on_projectCombo_currentIndexChanged(self, idx):
        prjId = self.projectCombo.itemData(idx)
        self.nameEdit.setText(self.data[prjId]['Name'])
        self.dateTimeEdit.setDateTime(self.data[prjId]['Date'])

        self.sectionWidget.setProjectId(prjId)

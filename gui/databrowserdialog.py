#-----------------------------------------------------------
#
# QGIS wincan 2 QGEP Plugin
# Copyright (C) 2016 Denis Rouzaud
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
from wincan2qgep.core.section import findSection
from wincan2qgep.ui.ui_databrowserdialog import Ui_DataBrowserDialog


class DataBrowserDialog(QDialog, Ui_DataBrowserDialog):
    def __init__(self, iface, data):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        self.data = data
        self.currentProjectId = None

        self.cannotImportLabel.hide()

        self.sectionWidget.finishInit(iface, self.data)

        for p_id, project in self.data.items():
            self.projectCombo.addItem(project['Name'], p_id)

    @pyqtSlot(str)
    def on_channelNameEdit_textChanged(self, txt):
        if self.currentProjectId is not None:
            self.data[self.currentProjectId]['Channel'] = txt

    @pyqtSlot(int)
    def on_projectCombo_currentIndexChanged(self, idx):
        self.currentProjectId = self.projectCombo.itemData(idx)
        self.dateTimeEdit.setDateTime(self.data[self.currentProjectId]['Date'])
        self.channelNameEdit.setText(self.data[self.currentProjectId]['Channel'])
        self.sectionWidget.setProjectId(self.currentProjectId)

    @pyqtSlot()
    def on_searchButton_clicked(self):
        if self.currentProjectId is None:
            return

        self.sectionWidget.setEnabled(False)

        channel = self.data[self.currentProjectId]['Channel']
        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]['Sections'].items():
                feature = findSection(channel, section['StartNode'], section['EndNode'])
                if feature.isValid():
                    self.data[p_id]['Sections'][s_id]['QgepChannelId'] = feature.attribute('obj_id')

        self.sectionWidget.setEnabled(True)
        self.sectionWidget.setProjectId(self.currentProjectId)


    @pyqtSlot()
    def on_importButton_clicked(self):
        # check that reaches are properly assigned
        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]['Sections'].items():
                for inspection in self.data[p_id]['Sections'][s_id]['Inspections'].values():
                    if inspection['Import']:
                        if section['QgepChannelId'] is None:
                            self.cannotImportLabel.show()
                            return
                        break


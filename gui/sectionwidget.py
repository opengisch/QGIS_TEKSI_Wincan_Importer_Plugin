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

from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest

from wincan2qgep.core.mysettings import MySettings
from wincan2qgep.ui.sectionwidget import Ui_SectionWidget


class SectionWidget(QWidget, Ui_SectionWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.settings = MySettings()
        self.data = {}
        self.projectId = None
        self.sectionId = None

        self.sectionSelector.featureIdentified.connect(self.setQgepChannelId)



    def finishInit(self, iface, data):
        layerid = self.settings.value("channelLayer")
        self.sectionSelector.setLayer(QgsMapLayerRegistry.instance().mapLayer(layerid))
        self.sectionSelector.setCanvas(iface.mapCanvas())
        self.data = data

    def setProjectId(self, prjId = None):
        self.sectionCombo.clear()

        self.projectId = prjId

        if prjId is None:
            return

        for s_id, section in self.data[prjId]['Sections'].items():
            title = '{0}: de {1} a {2}'.format(section['Counter'], section['StartNode'], section['EndNode'])
            self.sectionCombo.addItem(title, s_id)

    def setQgepChannelId(self, feature):
        if self.projectId is None or self.sectionId is None:
            return

        self.data[self.projectId]['Sections'][self.sectionId]['QgepChannelId'] = feature.attribute('obj_id')


    @pyqtSlot(int)
    def on_sectionCombo_currentIndexChanged(self, idx):
            self.sectionSelector.clear()
            self.endNodeEdit.clear()
            self.pipeDiaEdit.clear()
            self.pipeMaterialEdit.clear()
            self.pipeWidthEdit.clear()
            self.profileEdit.clear()
            self.sectionlengthEdit.clear()
            self.sectionUseEdit.clear()
            self.startNodeEdit.clear()

            self.sectionId = None

            if idx < 0 or self.projectId is None:
                return

            self.sectionId = self.sectionCombo.itemData(idx)
            section = self.data[self.projectId]['Sections'][self.sectionId]

            feature = QgsFeature()
            if section['QgepChannelId'] is not None:
                layerid = self.settings.value("channelLayer")
                layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
                request = QgsFeatureRequest().setFilterExpression('"obj_id" = \'{}\''.format(section['QgepChannelId']))
                for f in layer.getFeatures( request ):
                    feature = QgsFeature(f)
            self.sectionSelector.setFeature(feature)

            self.endNodeEdit.setText(section['EndNode'])
            self.pipeDiaEdit.setText('{}'.format(section['PipeDia']))
            self.pipeMaterialEdit.setText(section['PipeMaterial'])
            self.pipeWidthEdit.setText('{}'.format(section['PipeWidth']))
            self.profileEdit.setText(section['Profile'])
            self.sectionlengthEdit.setText('{}'.format(section['Sectionlength']))
            self.sectionUseEdit.setText(section['SectionUse'])
            self.startNodeEdit.setText(section['StartNode'])

            self.inspectionWidget.setInspections(section['Inspections'])




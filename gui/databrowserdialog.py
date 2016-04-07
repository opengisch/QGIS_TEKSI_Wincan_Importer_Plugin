#!/usr/bin/env python
# coding: utf-8 -*-
#
# #-----------------------------------------------------------
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


from PyQt4.QtCore import pyqtSlot, QDateTime
from PyQt4.QtGui import QDialog

from qgis.core import QgsMapLayerRegistry, QgsFeature, edit
from qgis.gui import QgsEditorWidgetRegistry, QgsAttributeEditorContext

from wincan2qgep.core.mysettings import MySettings
from wincan2qgep.core.section import findSection, sectionAtId
from wincan2qgep.ui.ui_databrowserdialog import Ui_DataBrowserDialog


class DataBrowserDialog(QDialog, Ui_DataBrowserDialog):
    def __init__(self, iface, data):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        self.data = data
        self.currentProjectId = None
        self.channelNameEdit.setFocus()

        self.cannotImportLabel.hide()

        mLayer = QgsMapLayerRegistry.instance().mapLayer(self.settings.value('maintenanceLayer'))
        if mLayer is not None:
            fieldIdx = mLayer.fieldNameIndex('fk_operator_company')
            widgetConfig = mLayer.editorWidgetV2Config(fieldIdx)
            editorContext = QgsAttributeEditorContext()
            editorContext.setVectorLayerTools(iface.vectorLayerTools())
            self.relationWidgetWrapper = QgsEditorWidgetRegistry.instance().create("ValueRelation",
                                                                                   mLayer,
                                                                                   fieldIdx,
                                                                                   widgetConfig,
                                                                                   self.operatingCompanyComboBox,
                                                                                   self,
                                                                                   editorContext)


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
                    self.data[p_id]['Sections'][s_id]['QgepChannelId1'] = feature.attribute('obj_id')

        self.sectionWidget.setEnabled(True)
        self.sectionWidget.setProjectId(self.currentProjectId)


    @pyqtSlot()
    def on_importButton_clicked(self):
        self.cannotImportLabel.hide()

        # initilaize maintenance and damage layers and features
        mLayerid = self.settings.value("maintenanceLayer")
        mLayer = QgsMapLayerRegistry.instance().mapLayer(mLayerid)
        dLayerid = self.settings.value("damageLayer")
        dLayer = QgsMapLayerRegistry.instance().mapLayer(dLayerid)
        features = {}  # dictionnary with maintenance event as key, and damages as values

        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]['Sections'].items():
                for i_id, inspection in self.data[p_id]['Sections'][s_id]['Inspections'].iteritems():
                    if inspection['Import']:

                        # get corresponding reaches in qgep project
                        reachFeatures = []
                        for fid in [section['QgepChannelId{}'.format(i)] for i in (1,2,3)]:
                            if fid is None:
                                break
                            f = sectionAtId( fid )
                            if f.isValid() is False:
                                self.cannotImportLabel.show()
                                self.cannotImportLabel.setText('L''inspection {} chambre {} à {} a un collecteur assigné qui n''existe pas ou plus.'
                                                               .format(section['Counter'], section['StartNode'], section['EndNode']))
                                return
                            reachFeatures.append(QgsFeature(f))

                        if len(reachFeatures) == 0:
                            self.cannotImportLabel.show()
                            self.cannotImportLabel.setText('L''inspection {} chambre {} à {} n''a pas de collecteur assigné.'
                                                           .format(section['Counter'], section['StartNode'], section['EndNode']))
                            return


                        # create maintenance/examination event
                        maintenanceFeatures = []
                        for rf in reachFeatures:
                            mf = QgsFeature()
                            initFields = mLayer.dataProvider().fields()
                            mf.setFields(initFields)
                            mf.initAttributes(initFields.size())
                            #mf['identifier'] = i_id  # use custom id to retrieve feature
                            mf['maintenance_type'] = 'examination'
                            mf['kind'] = 4564  # vl_maintenance_event_kind: inspection
                            mf['operator'] = inspection['Operator']
                            mf['time_point'] = QDateTime(inspection['InspDate'])
                            mf['remark'] = ''
                            mf['status'] = 2550  # vl_maintenance_event: accomplished
                            if inspection['CodeInspectionDir'] == 'D':
                                mf['fs_reach_point'] = rf['rp_from_obj_id']
                            else:
                                mf['fs_reach_point'] = rf['rp_to_obj_id']
                            maintenanceFeatures.append(QgsFeature(mf))

                        # add corresponding damages
                        damageFeatures = []
                        for reachIndex in range(0,len(maintenanceFeatures)):
                            damageFeatures[reachIndex] = []
                        reachIndex = 0
                        for observation in self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'].values():
                            if observation['Import']:

                                distance = observation['Position']
                                while distance > reachFeatures[reachIndex]['length_effective']:
                                    if reachIndex < len(reachFeatures):
                                        distance -= reachFeatures[reachIndex]['length_effective']
                                        reachIndex += 1
                                    else:
                                        if distance <= reachFeatures[reachIndex]['length_effective'] + .5:  # add 50cm tolerance
                                            break
                                        else:
                                            self.cannotImportLabel.show()
                                            self.cannotImportLabel.setText('L''inspection {} chambre {} à {} a des observations à des positions supérieures à la longueur'
                                                                           ' du ou des collecteurs assignés.'.format(section['Counter'], section['StartNode'], section['EndNode']))
                                            return

                                # get corresponding code for damage level
                                code2vl = {0: 3707, 1: 3708, 2: 3709, 3: 3710, 4: 3711, 'Unkown': 4561}
                                if observation['Rate'] in code2vl.keys():
                                    class_damage = code2vl[observation['Rate']]
                                else:
                                    class_damage = code2vl['Unknown']

                                # create maintenance/examination event
                                df = QgsFeature()
                                initFields = dLayer.dataProvider().fields()
                                df.setFields(initFields)
                                df.initAttributes(initFields.size())
                                df['comments'] = observation['Text']
                                df['single_damage_class'] = class_damage
                                df['channel_damage_code'] = observation['OpCode']
                                df['distance'] = distance

                                damageFeatures[reachIndex].append(df)

                        for reachIndex in range(0,len(maintenanceFeatures)):
                            features[maintenanceFeatures[reachIndex]] = damageFeatures[reachIndex]




        with edit(mLayer):

            for maintenanceFeature, damageFeatures in features.iteritems():

                if len(damageFeatures) == 0:
                    continue

                mLayer.addFeature(maintenanceFeature)
                fid = maintenanceFeature['obj_id']





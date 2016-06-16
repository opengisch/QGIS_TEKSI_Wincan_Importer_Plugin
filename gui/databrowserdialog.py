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
from wincan2qgep.core.vsacode import damageCode2vl, damageLevel2vl
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
        self.progressBar.hide()

        self.relationWidgetWrapper = None
        maintenance_layer = QgsMapLayerRegistry.instance().mapLayer(self.settings.value('maintenanceLayer'))
        if maintenance_layer is not None:
            field_idx = maintenance_layer.fieldNameIndex('fk_operator_company')
            widget_config = maintenance_layer.editorWidgetV2Config(field_idx)
            editor_context = QgsAttributeEditorContext()
            editor_context.setVectorLayerTools(iface.vectorLayerTools())
            self.relationWidgetWrapper = QgsEditorWidgetRegistry.instance().create("ValueRelation",
                                                                                   maintenance_layer,
                                                                                   field_idx,
                                                                                   widget_config,
                                                                                   self.operatingCompanyComboBox,
                                                                                   self,
                                                                                   editor_context)

        self.sectionWidget.finishInit(iface, self.data)

        for p_id, project in self.data.items():
            self.projectCombo.addItem(project['Name'], p_id)

        self.channelNameEdit.setText('5004B')
        # self.on_searchButton_clicked()

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

        # init progress bar
        c = 0
        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]['Sections'].items():
                c += 1
        self.progressBar.setMaximum(c)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.show()
        i = 0

        # find sections
        channel = self.data[self.currentProjectId]['Channel']
        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]['Sections'].items():
                feature = findSection(channel, section['StartNode'], section['EndNode'])
                if feature.isValid():
                    self.data[p_id]['Sections'][s_id]['QgepChannelId1'] = feature.attribute('obj_id')
                self.progressBar.setValue(i)
                i += 1
        self.progressBar.hide()

        self.sectionWidget.setEnabled(True)
        self.sectionWidget.setProjectId(self.currentProjectId)


    @pyqtSlot()
    def on_importButton_clicked(self):
        self.cannotImportLabel.hide()

        # initilaize maintenance and damage layers and features
        maintenance_layer_id = self.settings.value("maintenanceLayer")
        maintenance_layer = QgsMapLayerRegistry.instance().mapLayer(maintenance_layer_id)
        damage_layer_id = self.settings.value("damageLayer")
        damage_layer = QgsMapLayerRegistry.instance().mapLayer(damage_layer_id)
        join_layer_id = self.settings.value("joinMaintenceWastewaterstructureLayer")
        join_layer = QgsMapLayerRegistry.instance().mapLayer(join_layer_id)
        features = {}  # dictionnary with waste water structure id (reach) as key, and as values: a dict with maintenance event and damages

        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]['Sections'].items():
                for i_id, inspection in self.data[p_id]['Sections'][s_id]['Inspections'].iteritems():
                    if inspection['Import']:

                        # get corresponding reaches in qgep project
                        reach_features = []
                        for fid in [section['QgepChannelId{}'.format(i)] for i in (1, 2, 3)]:
                            if fid is None:
                                break
                            f = sectionAtId( fid )
                            if f.isValid() is False:
                                self.cannotImportLabel.show()
                                self.cannotImportLabel.setText('L''inspection {} chambre {} à {} a un collecteur assigné qui n''existe pas ou plus.'
                                                               .format(section['Counter'], section['StartNode'], section['EndNode']))
                                return
                            reach_features.append(QgsFeature(f))

                        if len(reach_features) == 0:
                            self.cannotImportLabel.show()
                            self.cannotImportLabel.setText('L''inspection {} chambre {} à {} n''a pas de collecteur assigné.'
                                                           .format(section['Counter'], section['StartNode'], section['EndNode']))
                            return

                        # create maintenance/examination event
                        for rf in reach_features:
                            mf = QgsFeature()
                            initFields = maintenance_layer.dataProvider().fields()
                            mf.setFields(initFields)
                            mf.initAttributes(initFields.size())
                            # mf['identifier'] = i_id  # use custom id to retrieve feature
                            mf['maintenance_type'] = 'examination'
                            mf['kind'] = 4564  # vl_maintenance_event_kind: inspection
                            mf['operator'] = inspection['Operator']
                            mf['time_point'] = QDateTime(inspection['InspDate'])
                            mf['remark'] = ''
                            mf['status'] = 2550  # vl_maintenance_event: accomplished
                            mf['inspected_length'] = section['Sectionlength']
                            if self.relationWidgetWrapper is not None:
                                mf['fk_operator_company'] = self.relationWidgetWrapper.value()
                            if inspection['CodeInspectionDir'] == 'D':
                                mf['fs_reach_point'] = rf['rp_from_obj_id']
                            else:
                                mf['fs_reach_point'] = rf['rp_to_obj_id']

                            features[rf['ws_obj_id']] = {'maintenance': QgsFeature(mf), 'damages': []}

                        # add corresponding damages
                        reach_index = 0
                        for observation in self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'].values():
                            if observation['Import']:

                                distance = observation['Position']
                                while distance > reach_features[reach_index]['length_effective']:
                                    if reach_index < len(reach_features)-1:
                                        distance -= reach_features[reach_index]['length_effective']
                                        reach_index += 1
                                    else:
                                        if distance <= reach_features[reach_index]['length_effective'] + .5:  # add 50cm tolerance
                                            break
                                        else:
                                            self.cannotImportLabel.show()
                                            self.cannotImportLabel.setText('L''inspection {} chambre {} à {} a des observations à des positions supérieures à la longueur'
                                                                           ' du ou des collecteurs assignés.'.format(section['Counter'], section['StartNode'], section['EndNode']))
                                            return

                                # create maintenance/examination event
                                df = QgsFeature()
                                initFields = damage_layer.dataProvider().fields()
                                df.setFields(initFields)
                                df.initAttributes(initFields.size())
                                df['damage_type'] = 'channel'
                                df['comments'] = observation['Text']
                                df['single_damage_class'] = damageLevel2vl(observation['Rate'])
                                df['channel_damage_code'] = int(damageCode2vl(observation['OpCode']))
                                df['distance'] = distance
                                df['video_counter'] = observation['MPEGPosition']

                                ws_obj_id = reach_features[reach_index]['ws_obj_id']
                                features[ws_obj_id]['damages'].append(df)

        with edit(maintenance_layer):
            self.progressBar.setMaximum(len(features))
            self.progressBar.setMinimum(0)
            self.progressBar.setValue(0)
            self.progressBar.show()
            i = 0
            for ws_obj_id, elements in features.iteritems():

                maintenance = elements['maintenance']
                damages = elements['damages']

                if len(damages) == 0:
                    continue

                # write maintenace feature
                maintenance_layer.addFeature(maintenance)

                # set fkey maintenance event id to all damages
                for i, _ in enumerate(damages):
                    damages[i]['fs_examination'] = maintenance['obj_id']

                # write damages
                damage_layer.addFeatures(damages, False)

                # write in relation table (wasterwater structure - maintenance events)
                jf = QgsFeature()
                init_fields = join_layer.dataProvider().fields()
                jf.setFields(init_fields)
                jf.initAttributes(init_fields.size())
                jf['fk_wastewater_structure'] = ws_obj_id
                jf['fk_maintenance_event'] = maintenance['obj_id']
                join_layer.addFeature(jf)

                i += 1
                self.progressBar.setValue(i)

        self.progressBar.hide()





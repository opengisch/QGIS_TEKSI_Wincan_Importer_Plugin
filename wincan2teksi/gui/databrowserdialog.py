# encoding: utf-8
#
# #-----------------------------------------------------------
#
# QGIS wincan 2 QGEP Plugin
# Copyright (C) 2016 Denis Rouzaud
#
# -----------------------------------------------------------
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
# ---------------------------------------------------------------------

import re
import os

from qgis.PyQt.QtCore import pyqtSlot, QDateTime, QCoreApplication
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.uic import loadUiType

from qgis.core import QgsProject, QgsFeature, QgsFeatureRequest
from qgis.gui import QgsGui, QgsAttributeEditorContext, QgisInterface

from wincan2teksi.core.settings import Settings
from wincan2teksi.core.section import find_section, section_at_id
from wincan2teksi.core.vsacode import (
    damage_code_to_vl,
    damage_level_to_vl,
    damage_level_2_structure_condition,
    structure_condition_2_damage_level,
)
from wincan2teksi.core.layer_edit import edit
from wincan2teksi.core.utils import info, dbg_info

Ui_DataBrowserDialog, _ = loadUiType(
    os.path.join(os.path.dirname(__file__), "..", "ui", "databrowserdialog.ui")
)


class DataBrowserDialog(QDialog, Ui_DataBrowserDialog):
    def __init__(self, iface: QgisInterface, data, data_path=""):
        print(os.path.join(os.path.dirname(__file__), "..", "ui", "databrowserdialog.ui"))
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = Settings()
        self.data = data
        self.current_project_id = None
        self.channelNameEdit.setFocus()
        self.cancel = False

        self.data_path_line_edit.setText(data_path)
        self.pdf_path_widget.setDefaultRoot(data_path)

        self.cannotImportLabel.hide()
        self.progressBar.setTextVisible(True)
        self.progressBar.hide()
        self.cancelButton.hide()

        self.pdf_path_widget.setDefaultRoot(data_path)

        self.relationWidgetWrapper = None
        maintenance_layer = QgsProject.instance().mapLayer(self.settings.value("maintenance_layer"))
        if maintenance_layer is not None:
            widget_config = maintenance_layer.editFormConfig().widgetConfig("fk_operating_company")
            editor_context = QgsAttributeEditorContext()
            editor_context.setVectorLayerTools(iface.vectorLayerTools())
            self.relationWidgetWrapper = QgsGui.editorWidgetRegistry().create(
                "ValueRelation",
                maintenance_layer,
                maintenance_layer.fields().indexFromName("fk_operating_company"),
                widget_config,
                self.operatingCompanyComboBox,
                self,
            )

        self.sectionWidget.finish_init(iface, self.data)

        for p_id, project in self.data.items():
            self.projectCombo.addItem(project["Name"], p_id)

        self.channelNameEdit.setText("")
        # self.on_searchButton_clicked()

    @pyqtSlot(str)
    def on_channelNameEdit_textChanged(self, txt):
        if self.current_project_id is not None:
            self.data[self.current_project_id]["Channel"] = txt

    @pyqtSlot(int)
    def on_projectCombo_currentIndexChanged(self, idx):
        self.current_project_id = self.projectCombo.itemData(idx)
        self.dateTimeEdit.setDateTime(self.data[self.current_project_id]["Date"])
        self.channelNameEdit.setText(self.data[self.current_project_id]["Channel"])
        self.sectionWidget.set_project_id(self.current_project_id)

    @pyqtSlot()
    def on_cancelButton_clicked(self):
        self.cancel = True

    @pyqtSlot()
    def on_searchButton_clicked(self):
        if self.current_project_id is None:
            return

        self.sectionWidget.setEnabled(False)

        # init progress bar
        c = 0
        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]["Sections"].items():
                c += 1
        self.progressBar.setMaximum(c)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.setFormat("Searching channels %v/%m")
        self.progressBar.show()
        self.cancelButton.show()
        self.importButton.hide()
        self.cancel = False
        i = 0

        # find sections
        channel = self.data[self.current_project_id]["Channel"]
        for p_id in self.data.keys():
            if self.cancel:
                break
            for s_id, section in self.data[p_id]["Sections"].items():
                QCoreApplication.processEvents()
                if self.cancel:
                    break
                feature = find_section(channel, section["StartNode"], section["EndNode"])
                if not feature.isValid() and self.settings.value("remove_trailing_chars"):
                    # try without trailing alpha char
                    feature = find_section(
                        channel,
                        re.sub("\D*$", "", section["StartNode"]),
                        re.sub("\D*$", "", section["EndNode"]),
                    )
                if feature.isValid():
                    self.data[p_id]["Sections"][s_id]["qgep_channel_id_1"] = feature.attribute(
                        "obj_id"
                    )
                self.progressBar.setValue(i)
                i += 1
        self.progressBar.hide()
        self.cancelButton.hide()
        self.importButton.show()

        self.sectionWidget.setEnabled(True)
        self.sectionWidget.set_project_id(self.current_project_id)

    @pyqtSlot()
    def on_importButton_clicked(self):
        self.cannotImportLabel.hide()

        # init progress bar
        c = 0
        for p_id in self.data.keys():
            for s_id, section in self.data[p_id]["Sections"].items():
                c += 1
        self.progressBar.setMaximum(c)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.setFormat("Checking channels %v/%m")
        self.progressBar.show()
        self.cancelButton.show()
        self.importButton.hide()
        self.cancel = False
        i = 0

        # initialize maintenance and damage layers and features
        maintenance_layer_id = self.settings.value("maintenance_layer")
        maintenance_layer = QgsProject.instance().mapLayer(maintenance_layer_id)
        damage_layer_id = self.settings.value("damage_layer")
        damage_layer = QgsProject.instance().mapLayer(damage_layer_id)
        join_layer_id = self.settings.value("join_maintence_wastewaterstructure_layer")
        join_layer = QgsProject.instance().mapLayer(join_layer_id)
        if join_layer is None:
            self.cannotImportLabel.show()
            self.cannotImportLabel.setText(
                self.tr("The join layer '{layer_id}' is missing in the project.")
            )
            self.hide_progress()
            return
        features = {}  # dictionnary with waste water structure id (reach) as key, and as values: a dict with maintenance event and damages

        for p_id in self.data.keys():
            previous_section_imported = True
            for s_id, section in self.data[p_id]["Sections"].items():
                if self.cancel:
                    self.hide_progress()
                    return

                if section["Import"] is not True:
                    previous_section_imported = False
                    continue

                for i_id, inspection in self.data[p_id]["Sections"][s_id]["Inspections"].items():
                    if inspection["Import"]:
                        # offset in case of several sections in inspection
                        # data correspond to a single section in qgep data
                        distance_offset = 0

                        if section["UsePreviousSection"] is not True:
                            previous_section_imported = True
                            # get corresponding reaches in qgep project
                            reach_features = []

                            for fid in [section["qgep_channel_id_{}".format(i)] for i in (1, 2, 3)]:
                                if fid is None:
                                    break
                                f = section_at_id(fid)
                                if f.isValid() is False:
                                    self.cannotImportLabel.show()
                                    self.cannotImportLabel.setText(
                                        self.tr(
                                            "Inspection {i} from manhole {c1} to {c2}"
                                            " has an non-existent channel assigned.".format(
                                                i=section["Counter"],
                                                c1=section["StartNode"],
                                                c2=section["EndNode"],
                                            )
                                        )
                                    )
                                    self.sectionWidget.select_section(s_id)
                                    self.hide_progress()
                                    return
                                reach_features.append(QgsFeature(f))

                            if len(reach_features) == 0:
                                self.cannotImportLabel.show()
                                self.cannotImportLabel.setText(
                                    self.tr(
                                        "Inspection {i} from manhole {c1} to {c2}"
                                        " has no channel assigned.".format(
                                            i=section["Counter"],
                                            c1=section["StartNode"],
                                            c2=section["EndNode"],
                                        )
                                    )
                                )
                                self.sectionWidget.select_section(s_id)
                                self.hide_progress()
                                return

                            # create maintenance/examination event (one per qgep reach feature)
                            for rf in reach_features:
                                # in case several sections in qgep data
                                # correspond to a single section in inspection data
                                mf = QgsFeature()
                                init_fields = maintenance_layer.fields()
                                mf.setFields(init_fields)
                                mf.initAttributes(init_fields.size())
                                mf["obj_id"] = maintenance_layer.dataProvider().defaultValue(
                                    maintenance_layer.fields().indexFromName("obj_id")
                                )
                                # mf['identifier'] = i_id  # use custom id to retrieve feature
                                mf["maintenance_event_type"] = "examination"
                                mf["kind"] = 4564  # vl_maintenance_event_kind: inspection
                                mf["operator"] = inspection["Operator"]
                                mf["time_point"] = QDateTime(inspection["InspDate"])
                                mf["remark"] = ""
                                mf["status"] = 2550  # vl_maintenance_event: accomplished
                                mf["inspected_length"] = section["Sectionlength"]
                                mf["videonumber"] = inspection["VideoName"]
                                mf["base_data"] = self.pdf_path_widget.filePath()
                                if self.relationWidgetWrapper is not None:
                                    mf["fk_operating_company"] = self.relationWidgetWrapper.value()
                                if inspection["CodeInspectionDir"] == "D":
                                    mf["fk_reach_point"] = rf["rp_from_obj_id"]
                                else:
                                    mf["fk_reach_point"] = rf["rp_to_obj_id"]

                                features[rf["ws_obj_id"]] = {
                                    "maintenance": QgsFeature(mf),
                                    "damages": [],
                                    "pictures": [],
                                    "structure_condition": 4,
                                }

                        else:
                            # in case several sections in inspection data correspond to a single section in qgep data
                            # substract length from previous sections in inspection data
                            if not previous_section_imported:
                                self.cannotImportLabel.show()
                                self.cannotImportLabel.setText(
                                    self.tr(
                                        "Inspection {i} from manhole {c1} to {c2}"
                                        " uses previous channel, but it is not defined.".format(
                                            i=section["Counter"],
                                            c1=section["StartNode"],
                                            c2=section["EndNode"],
                                        )
                                    )
                                )
                                self.sectionWidget.select_section(s_id)
                                self.hide_progress()
                                return
                            distance_offset = 0
                            offset_section_id = s_id
                            while (
                                self.data[p_id]["Sections"][offset_section_id]["UsePreviousSection"]
                                is True
                            ):
                                # get previous section id
                                offset_section_id_index = list(self.data[p_id]["Sections"]).index(
                                    offset_section_id
                                )
                                assert offset_section_id_index > 0
                                offset_section_id = list(self.data[p_id]["Sections"])[
                                    offset_section_id_index - 1
                                ]
                                # accumulate offset
                                distance_offset -= self.data[p_id]["Sections"][offset_section_id][
                                    "Sectionlength"
                                ]
                                info(
                                    "using previous section: {} with distance offset {}".format(
                                        offset_section_id, distance_offset
                                    )
                                )

                                # add corresponding damages
                        reach_index = 0
                        structure_condition = 4  # = ok
                        for observation in self.data[p_id]["Sections"][s_id]["Inspections"][i_id][
                            "Observations"
                        ].values():
                            if observation["Import"]:
                                distance = observation["Position"] + distance_offset
                                if not observation["ForceImport"]:
                                    while (
                                        distance > reach_features[reach_index]["length_effective"]
                                    ):
                                        if reach_index < len(reach_features) - 1:
                                            distance -= reach_features[reach_index][
                                                "length_effective"
                                            ]
                                            reach_index += 1
                                        else:
                                            if distance <= reach_features[reach_index][
                                                "length_effective"
                                            ] + self.settings.value(
                                                "tolerance_channel_length"
                                            ):  # add 50cm tolerance
                                                break
                                            else:
                                                self.cannotImportLabel.show()
                                                self.cannotImportLabel.setText(
                                                    self.tr(
                                                        "Inspection {i} from manhole {c1} to {c2}"
                                                        " has observations further than the length"
                                                        " of the assigned channels.".format(
                                                            i=section["Counter"],
                                                            c1=section["StartNode"],
                                                            c2=section["EndNode"],
                                                        )
                                                    )
                                                )
                                                self.sectionWidget.select_section(s_id)
                                                self.hide_progress()
                                                return

                                # create maintenance/examination event
                                df = QgsFeature()
                                init_fields = damage_layer.fields()
                                df.setFields(init_fields)
                                df.initAttributes(init_fields.size())
                                df["obj_id"] = damage_layer.dataProvider().defaultValue(
                                    damage_layer.fields().indexFromName("obj_id")
                                )
                                df["damage_type"] = "channel"
                                df["comments"] = observation["Text"]
                                df["single_damage_class"] = damage_level_to_vl(observation["Rate"])
                                df["channel_damage_code"] = int(
                                    damage_code_to_vl(observation["OpCode"])
                                )
                                df["distance"] = distance
                                df["video_counter"] = observation["MPEGPosition"]
                                # pictures
                                pics = observation["PhotoFilename"]
                                # get wastewater structure id
                                ws_obj_id = reach_features[reach_index]["ws_obj_id"]
                                features[ws_obj_id]["damages"].append(df)
                                features[ws_obj_id]["pictures"].append(pics)
                                structure_condition = min(structure_condition, observation["Rate"])
                                features[ws_obj_id]["structure_condition"] = structure_condition
                self.progressBar.setValue(i)
                i += 1

        self.progressBar.setMaximum(len(features))
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.setFormat("Importing %v/%m")
        self.progressBar.show()
        self.cancelButton.show()
        self.importButton.hide()
        self.cancel = False

        file_layer_id = Settings().value("file_layer")
        file_layer = QgsProject.instance().mapLayer(file_layer_id)

        with edit(join_layer):
            with edit(file_layer):
                with edit(damage_layer):
                    with edit(maintenance_layer):
                        i = 0
                        for ws_obj_id, elements in features.items():
                            QCoreApplication.processEvents()
                            if self.cancel:
                                break

                            maintenance = elements["maintenance"]
                            damages = elements["damages"]
                            pictures = elements["pictures"]
                            structure_condition = elements["structure_condition"]

                            if len(damages) == 0:
                                continue

                            # write maintenance feature
                            ok = maintenance_layer.addFeature(maintenance)
                            dbg_info(
                                "adding feature to maintenance layer (fid: {}): {}".format(
                                    maintenance["obj_id"], "ok" if ok else "error"
                                )
                            )

                            # write video
                            of = QgsFeature()
                            init_fields = file_layer.fields()
                            of.setFields(init_fields)
                            of.initAttributes(init_fields.size())
                            of["obj_id"] = file_layer.dataProvider().defaultValue(
                                file_layer.fields().indexFromName("obj_id")
                            )
                            of["class"] = 3825  # i.e. maintenance event
                            of["kind"] = 3771  # i.e. video
                            of["object"] = maintenance["obj_id"]
                            of["identifier"] = maintenance["videonumber"]
                            of["path_relative"] = self.data_path_line_edit.text() + "\Video"
                            ok = file_layer.addFeature(of)
                            dbg_info(
                                "adding feature to filer layer (fid: {}): {}".format(
                                    of["obj_id"], "ok" if ok else "error"
                                )
                            )

                            # set fkey maintenance event id to all damages
                            for k, _ in enumerate(damages):
                                damages[k]["fk_examination"] = maintenance["obj_id"]

                            # write damages
                            for k, damage in enumerate(damages):
                                ok = damage_layer.addFeature(damage)
                                dbg_info(
                                    "adding feature to damage layer (fid: {}): {}".format(
                                        damage["obj_id"], "ok" if ok else "error"
                                    )
                                )

                                # add pictures to od_file with reference to damage
                                for pic in pictures[k]:
                                    of = QgsFeature()
                                    init_fields = file_layer.fields()
                                    of.setFields(init_fields)
                                    of.initAttributes(init_fields.size())
                                    of["obj_id"] = file_layer.dataProvider().defaultValue(
                                        file_layer.fields().indexFromName("obj_id")
                                    )
                                    of["class"] = 3871  # i.e. damage
                                    of["kind"] = 3772  # i.e. photo
                                    of["object"] = damage["obj_id"]
                                    of["identifier"] = pic
                                    of["path_relative"] = (
                                        self.data_path_line_edit.text() + "\Picture"
                                    )
                                    ok = file_layer.addFeature(of)
                                    dbg_info(
                                        "adding picture to file layer (fid: {}): {}".format(
                                            of["obj_id"], "ok" if ok else "error"
                                        )
                                    )

                            # write in relation table (wastewater structure - maintenance events)
                            jf = QgsFeature()
                            init_fields = join_layer.fields()
                            jf.setFields(init_fields)
                            jf.initAttributes(init_fields.size())
                            jf["obj_id"] = join_layer.dataProvider().defaultValue(
                                join_layer.fields().indexFromName("obj_id")
                            )
                            jf["fk_wastewater_structure"] = ws_obj_id
                            jf["fk_maintenance_event"] = maintenance["obj_id"]
                            ok = join_layer.addFeature(jf)
                            dbg_info(
                                "adding feature to join layer (fid: {}): {}".format(
                                    jf["obj_id"], "ok" if ok else "error"
                                )
                            )

                            # get current reach
                            rf = QgsFeature()
                            layer_id = Settings().value("wastewater_structure")
                            wsl = QgsProject.instance().mapLayer(layer_id)
                            if wsl is not None:
                                request = QgsFeatureRequest().setFilterExpression(
                                    "\"obj_id\" = '{}'".format(ws_obj_id)
                                )
                                rf = next(wsl.getFeatures(request))
                            if rf.isValid():
                                # update structure condition if worse
                                old_level = structure_condition_2_damage_level(
                                    rf["structure_condition"]
                                )
                                if old_level is None or old_level > "Z{}".format(
                                    structure_condition
                                ):
                                    rf["structure_condition"] = damage_level_2_structure_condition(
                                        structure_condition
                                    )
                                    wsl.updateFeature(rf)

                            i += 1
                            self.progressBar.setValue(i)

        self.progressBar.hide()
        self.cancelButton.hide()
        self.importButton.show()

    def hide_progress(self):
        self.progressBar.hide()
        self.cancelButton.hide()
        self.importButton.show()

# -*- coding: utf-8 -*-
"""
/***************************************************************************

 QGIS Solothurn Locator Plugin
 Copyright (C) 2019 Denis Rouzaud

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.uic import loadUiType
from qgis.gui import (
    QgsSettingsStringComboBoxWrapper,
)

from wincan2teksi.core.settings import Settings

DialogUi, _ = loadUiType(os.path.join(os.path.dirname(__file__), "../ui/settings.ui"))


class SettingsDialog(QDialog, DialogUi):
    def __init__(self, parent=None):
        self.settings = Settings()
        QDialog.__init__(self, parent)
        self.setupUi(self)

        for setting_key in (
            "wastewater_structure_layer",
            "join_maintence_wastewaterstructure_layer",
            "channel_layer",
            "cover_layer",
            "maintenance_layer",
            "damage_layer",
            "file_layer",
            "vl_damage_channel_layer",
            "vl_damage_single_class",
            "vl_wastewater_structure_structure_condition",
        ):
            wrapper = QgsSettingsStringComboBoxWrapper(
                setting_key,
                self.settings.value(setting_key),
                QgsSettingsStringComboBoxWrapper.Mode.Data,
            )
            self.wrappers.append(wrapper)

    def accept(self):
        for wrapper in self.wrappers:
            wrapper.setSettingFromWidget()

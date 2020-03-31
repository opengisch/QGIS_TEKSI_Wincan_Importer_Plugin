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

from wincan2qgep.core.my_settings import MySettings
from wincan2qgep.qgissettingmanager import SettingDialog, UpdateMode


DialogUi, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/settings.ui'))


class SettingsDialog(QDialog, DialogUi, SettingDialog):
    def __init__(self, parent=None):
        settings = MySettings()
        QDialog.__init__(self, parent)
        SettingDialog.__init__(self, setting_manager=settings, mode=UpdateMode.DialogAccept)
        self.setupUi(self)
        self.settings = settings
        self.init_widgets()


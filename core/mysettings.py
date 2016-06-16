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

from PyQt4.QtGui import QColor
from wincan2qgep.qgissettingmanager import SettingManager

pluginName = "wincan2qgep_plugin"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        # project settings
        self.addSetting("channelLayer", "string", "project", 'vw_qgep_reach')
        self.addSetting("coverLayer", "string", "project", 'vw_qgep_cover')
        self.addSetting("maintenanceLayer", "string", "project", 'vw_qgep_maintenance')
        self.addSetting("damageLayer", "string", "project", 'vw_qgep_damage')
        self.addSetting("joinMaintenceWastewaterstructureLayer", "string", "project", 're_maintenance_event_wastewater_structure')
        self.addSetting("vlDamageChannelLayer", "string", "project", 'vl_damage_channel_code')
        self.addSetting("vlDamageSingleClass", "string", "project", 'vl_damage_single_damage_class')

        self.addSetting("xmlPath", "string", "project", '')




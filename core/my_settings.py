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


from ..qgissettingmanager import *

pluginName = "wincan2qgep_plugin"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        # project settings
        self.add_setting(Bool('remove_trailing_chars', Scope.Global, True))  # TODO: make it false whenever the settings dialog is done
        self.add_setting(Double('tolerance_channel_length', Scope.Global, 1))

        self.add_setting(String("channel_layer", Scope.Project, 'vw_qgep_reach'))
        self.add_setting(String("cover_layer", Scope.Project, 'vw_qgep_cover'))
        self.add_setting(String("maintenance_layer", Scope.Project, 'vw_qgep_maintenance'))
        self.add_setting(String("damage_layer", Scope.Project, 'vw_qgep_damage'))
        self.add_setting(String('join_maintence_wastewaterstructure_layer', Scope.Project, 're_maintenance_event_wastewater_structure'))
        self.add_setting(String("vl_damage_channel_layer", Scope.Project, 'vl_damage_channel_code'))
        self.add_setting(String("vl_damage_single_class", Scope.Project, 'vl_damage_single_damage_class'))

        self.add_setting(String('xmlPath', Scope.Project, ''))




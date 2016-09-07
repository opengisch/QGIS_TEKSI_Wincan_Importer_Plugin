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

from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest

from wincan2qgep.core.my_settings import MySettings


# return pkey of vl from VSA damage code
def damageCode2vl(code):
    feature = QgsFeature()

    layerid = MySettings().value("vl_damage_channel_layer")
    layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
    if layer is not None:
        requestText = '"value_en" = \'{}\''.format(code)

        request = QgsFeatureRequest().setFilterExpression(requestText)
        for f in layer.getFeatures( request ):
            feature = QgsFeature(f)
        #print requestText, feature.isValid()

    if feature.isValid():
        return f['code']

    else:
        return None


# return pkey of vl from VSA damage level
def damageLevel2vl(code):
    feature = QgsFeature()

    layerid = MySettings().value("vl_damage_single_class")
    layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
    if layer is not None:
        requestText = '"value_en" = \'EZ{}\''.format(code)

        request = QgsFeatureRequest().setFilterExpression(requestText)
        for f in layer.getFeatures( request ):
            feature = QgsFeature(f)
        #print requestText, feature.isValid()

    if feature.isValid():
        return f['code']

    else:
        return None


# return damage code to renovation necessity pkey
def damage_level_2_structure_condition(level):
    feature = QgsFeature()

    layerid = MySettings().value("vl_wastewater_structure_structure_condition")
    layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
    if layer is not None:
        requestText = '"value_en" = \'Z{}\''.format(level)

        request = QgsFeatureRequest().setFilterExpression(requestText)
        for f in layer.getFeatures(request):
            feature = QgsFeature(f)
            # print requestText, feature.isValid()

    if feature.isValid():
        return f['code']

    else:
        return None
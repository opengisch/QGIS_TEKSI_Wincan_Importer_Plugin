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

from wincan2qgep.core.mysettings import MySettings



def findSection(channel, startNode, endNode):
    feature = QgsFeature()

    layerid = MySettings().value("channelLayer")
    layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
    if layer is not None:
        requestText = '"rp_from_identifier" = \'{}-{}\' and "rp_to_identifier" = \'{}-{}\''.format(channel, startNode, channel, endNode)

        request = QgsFeatureRequest().setFilterExpression(requestText)
        for f in layer.getFeatures( request ):
            feature = QgsFeature(f)

        #print requestText, feature.isValid()
    return feature


def sectionAtId(id):
    feature = QgsFeature()
    if id is not None:
        layerid = MySettings().value("channelLayer")
        layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
        if layer is not None:
            request = QgsFeatureRequest().setFilterExpression('"obj_id" = \'{}\''.format(id))
            for f in layer.getFeatures( request ):
                feature = QgsFeature(f)
    return feature
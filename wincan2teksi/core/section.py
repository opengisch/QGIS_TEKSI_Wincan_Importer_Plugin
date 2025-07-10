# -----------------------------------------------------------
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

from qgis.core import QgsProject, QgsFeature, QgsFeatureRequest

from wincan2teksi.core.settings import Settings


def find_section(channel, start_node, end_node):
    feature = QgsFeature()

    layerid = Settings().value("channel_layer")
    layer = QgsProject.instance().mapLayer(layerid)
    if layer is not None:
        request_text = (
            "\"rp_from_identifier\" LIKE '{}-{}%' and \"rp_to_identifier\" LIKE '{}-{}%'".format(
                channel, start_node, channel, end_node
            )
        )
        request = QgsFeatureRequest().setFilterExpression(request_text)
        feature = next(layer.getFeatures(request), QgsFeature())
        # print requestText, feature.isValid()
    return feature


def section_at_id(obj_id):
    feature = QgsFeature()
    if obj_id is not None:
        layer_id = Settings().value("channel_layer")
        layer = QgsProject.instance().mapLayer(layer_id)
        if layer is not None:
            request = QgsFeatureRequest().setFilterExpression("\"obj_id\" = '{}'".format(obj_id))
            feature = next(layer.getFeatures(request), QgsFeature())
    return feature

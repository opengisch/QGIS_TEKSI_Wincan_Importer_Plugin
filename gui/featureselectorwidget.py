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

from PyQt4.QtCore import pyqtSignal, QSettings, QTimer
from PyQt4.QtGui import QWidget, QHBoxLayout, QLineEdit, QToolButton, QAction, QColor

from qgis.core import QgsApplication, QgsFeature, QGis
from qgis.gui import QgsMapToolIdentifyFeature, QgsHighlight


class CanvasExtent(object):
    Fixed = 1
    Pan = 2
    Scale = 3


class FeatureSelectorWidget(QWidget):
    featureIdentified = pyqtSignal(QgsFeature)

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        editLayout = QHBoxLayout()
        editLayout.setContentsMargins(0, 0, 0, 0)
        editLayout.setSpacing(2)
        self.setLayout(editLayout)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setReadOnly(True)
        editLayout.addWidget(self.lineEdit)
        
        self.highlightFeatureButton = QToolButton(self)
        self.highlightFeatureButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.highlightFeatureAction = QAction(QgsApplication.getThemeIcon("/mActionHighlightFeature.svg"), "Highlight feature", self)
        self.scaleHighlightFeatureAction = QAction(QgsApplication.getThemeIcon("/mActionScaleHighlightFeature.svg"), "Scale and highlight feature", self)
        self.panHighlightFeatureAction = QAction(QgsApplication.getThemeIcon("/mActionPanHighlightFeature.svg"), "Pan and highlight feature", self)
        self.highlightFeatureButton.addAction(self.highlightFeatureAction)
        self.highlightFeatureButton.addAction(self.scaleHighlightFeatureAction)
        self.highlightFeatureButton.addAction(self.panHighlightFeatureAction)
        self.highlightFeatureButton.setDefaultAction(self.highlightFeatureAction)
        editLayout.addWidget(self.highlightFeatureButton)

        self.mapIdentificationButton = QToolButton(self)
        self.mapIdentificationButton.setIcon(QgsApplication.getThemeIcon("/mActionMapIdentification.svg"))
        self.mapIdentificationButton.setText("Select on map")
        self.mapIdentificationButton.setCheckable(True)
        editLayout.addWidget(self.mapIdentificationButton)

        self.mapIdentificationButton.clicked.connect(self.mapIdentification)
        self.highlightFeatureButton.triggered.connect(self.highlightActionTriggered)

        self.layer = None
        self.mapTool = None
        self.canvas = None
        self.windowWidget = None
        self.highlight = None
        self.feature = QgsFeature()

    def setCanvas(self, mapCanvas):
        self.mapTool = QgsMapToolIdentifyFeature(mapCanvas)
        self.mapTool.setButton(self.mapIdentificationButton)
        self.canvas = mapCanvas

    def setLayer(self, layer):
        self.layer = layer

    def setFeature(self, feature, canvasExtent = CanvasExtent.Fixed):
        self.lineEdit.clear()
        self.feature = feature

        if not self.feature.isValid() or self.layer is None:
            return

        featureTitle = feature.attribute(self.layer.displayField())
        if featureTitle == '':
            featureTitle = feature.id()
        self.lineEdit.setText(str(featureTitle))
        self.highlightFeature(canvasExtent)


    def clear(self):
        self.feature = QgsFeature()
        self.lineEdit.clear()

    def mapIdentification(self):
        if self.layer is None or self.mapTool is None or self.canvas is None:
            return

        self.mapTool.setLayer(self.layer)
        self.canvas.setMapTool(self.mapTool)

        self.windowWidget = QWidget.window(self)
        self.canvas.window().raise_()
        self.canvas.activateWindow()
        self.canvas.setFocus()

        self.mapTool.featureIdentified.connect(self.mapToolFeatureIdentified)
        self.mapTool.deactivated.connect(self.mapToolDeactivated)

    def mapToolFeatureIdentified(self, feature):
        feature = QgsFeature(feature)
        self.featureIdentified.emit(feature)
        self.unsetMapTool()
        self.setFeature(feature)

    def mapToolDeactivated(self):
        if self.windowWidget is not None:
            self.windowWidget.raise_()
            self.windowWidget.activateWindow()

    def highlightFeature(self, canvasExtent = CanvasExtent.Fixed):
        if self.canvas is None or not self.feature.isValid():
            return

        geom = self.feature.geometry()

        if geom is None:
            return
  
        if canvasExtent == CanvasExtent.Scale:
            featBBox = geom.boundingBox()
            featBBox = self.canvas.mapSettings().layerToMapCoordinates(self.layer, featBBox)
            extent = self.canvas.extent()
            if not extent.contains(featBBox):
                extent.combineExtentWith(featBBox)
                extent.scale(1.1)
                self.canvas.setExtent(extent)
                self.canvas.refresh()
            
        elif canvasExtent == CanvasExtent.Pan:
            centroid = geom.centroid()
            center = centroid.asPoint()

            center = self.canvas.mapSettings().layerToMapCoordinates(self.layer, center)
            self.canvas.zoomByFactor(1.0, center)  # refresh is done in this method

        # highlight
        self.deleteHighlight()
        self.highlight = QgsHighlight(self.canvas, geom, self.layer)

        settings = QSettings()
        color = QColor(settings.value("/Map/highlight/color", QGis.DEFAULT_HIGHLIGHT_COLOR.name()))
        alpha = int(settings.value("/Map/highlight/colorAlpha", QGis.DEFAULT_HIGHLIGHT_COLOR.alpha()))
        buffer = 2*float(settings.value("/Map/highlight/buffer", QGis.DEFAULT_HIGHLIGHT_BUFFER_MM))
        min_width = 2*float(settings.value("/Map/highlight/min_width", QGis.DEFAULT_HIGHLIGHT_MIN_WIDTH_MM))

        self.highlight.setColor(color)  # sets also fill with default alpha
        color.setAlpha(alpha)
        self.highlight.setFillColor(color)  # sets fill with alpha
        self.highlight.setBuffer(buffer)
        self.highlight.setmin_width(min_width)
        self.highlight.show()
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.deleteHighlight)
        self.timer.start(3000)

    def deleteHighlight(self):
        if self.highlight is not None:
            self.highlight.hide()
            self.highlight = None

    def unsetMapTool(self):
        if self.canvas is not None and self.mapTool is not None:
            # this will call mapToolDeactivated
            self.canvas.unsetMapTool(self.mapTool)

    def highlightActionTriggered(self, action):
        self.highlightFeatureButton.setDefaultAction(action)

        if action == self.highlightFeatureAction:
            self.highlightFeature()

        elif action == self.scaleHighlightFeatureAction:
            self.highlightFeature(CanvasExtent.Scale)

        elif action == self.panHighlightFeatureAction:
            self.highlightFeature(CanvasExtent.Pan)

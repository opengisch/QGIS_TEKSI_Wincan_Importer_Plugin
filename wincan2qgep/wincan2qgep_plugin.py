#-----------------------------------------------------------
#
# QGIS Quick Finder Plugin
# Copyright (C) 2013 Denis Rouzaud
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

import os.path
from qgis.PyQt.QtCore import Qt, QObject, QSettings, QCoreApplication, QTranslator, pyqtSlot
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject
from qgis.gui import QgsRubberBand, QgsMessageBar, QgisInterface

from .core.my_settings import MySettings
from .core.import_data import ImportData
from .gui.databrowserdialog import DataBrowserDialog

import wincan2qgep.resources_rc


class Wincan2Qgep(QObject):

    name = "&Wincan 2 QGEP"
    actions = None

    def __init__(self, iface: QgisInterface):
        QObject.__init__(self)
        self.iface = iface
        self.actions = {}
        self.settings = MySettings()
        self.dlg = None

        # translation environment
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(self.plugin_dir, 'i18n', 'wincan2qgep_{0}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.actions['openInspection'] = QAction(
            QIcon(":/plugins/wincan2qgep/icons/wincan_logo.png"),
            self.tr("Ouvrir une inspection"),
            self.iface.mainWindow())
        self.actions['openInspection'].triggered.connect(self.open_inspection)
        self.iface.addPluginToMenu(self.name, self.actions['openInspection'])
        self.iface.addToolBarIcon(self.actions['openInspection'])

        # self.actions['showSettings'] = QAction(
        #     QIcon(":/plugins/wincan2qgep/icons/settings.svg"),
        #     self.tr("&Settings"),
        #     self.iface.mainWindow())
        # self.actions['showSettings'].triggered.connect(self.showSettings)
        # self.iface.addPluginToMenu(self.name, self.actions['showSettings'])

        # self.actions['help'] = QAction(
        #     QIcon(":/plugins/wincan2qgep/icons/help.svg"),
        #     self.tr("Help"),
        #     self.iface.mainWindow())
        # self.actions['help'].triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/wincan2qgep")))
        # self.iface.addPluginToMenu(self.name, self.actions['help'])

        self.rubber = QgsRubberBand(self.iface.mapCanvas())
        self.rubber.setColor(QColor(255, 255, 50, 200))
        self.rubber.setIcon(self.rubber.ICON_CIRCLE)
        self.rubber.setIconSize(15)
        self.rubber.setWidth(4)
        self.rubber.setBrushStyle(Qt.NoBrush)

    def unload(self):
        """ Unload plugin """
        for action in self.actions.values():
            self.iface.removePluginMenu(self.name, action)
            self.iface.removeToolBarIcon(action)
        if self.rubber:
            self.iface.mapCanvas().scene().removeItem(self.rubber)
            del self.rubber
        if self.dlg:
            self.dlg.close()

    #@pyqtSlot(str, QgsMessageBar.MessageLevel)
    #def display_message(self, message, level):
    #    self.iface.messageBar().pushMessage("Wincan 2 QGEP", message, level)

    # def showSettings(self):
    #     if ConfigurationDialog().exec_():
    #         self._reloadFinders()

    def open_inspection(self):
        xml_path = self.settings.value('xml_path')
        if xml_path == '':
            xml_path = QgsProject.instance().homePath()
        file_path, _ = QFileDialog.getOpenFileName(None, "Open WIncan inspection data", xml_path, "Wincan file (*.xml)")

        if file_path:
            absolute_path = os.path.dirname(os.path.realpath(file_path))
            parent_path = os.path.abspath(os.path.join(absolute_path, os.pardir))
            self.settings.set_value('xml_path', absolute_path)
            data = ImportData(file_path).data
            self.dlg = DataBrowserDialog(self.iface, data, parent_path)
            self.dlg.show()



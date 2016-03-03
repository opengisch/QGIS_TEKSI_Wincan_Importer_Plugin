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
from PyQt4.QtCore import Qt, QObject, QSettings, QCoreApplication, QTranslator, QUrl, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QColor, QDesktopServices
from qgis.gui import QgsRubberBand, QgsMessageBar

from wincan2qgep.core.mysettings import MySettings
from wincan2qgep.core.import_data import ImportData
from wincan2qgep.gui.configurationdialog import ConfigurationDialog
from wincan2qgep.gui.databrowserdialog import DataBrowserDialog

import resources_rc


class wincan2qgep(QObject):

    name = u"&Wincan 2 QGEP"
    actions = None


    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.actions = {}
        self.settings = MySettings()

        # translation environment
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'wincan2qgep_{0}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.actions['showSettings'] = QAction(
            QIcon(":/plugins/wincan2qgep/icons/settings.svg"),
            self.tr(u"&Settings"),
            self.iface.mainWindow())
        self.actions['showSettings'].triggered.connect(self.showSettings)
        self.iface.addPluginToMenu(self.name, self.actions['showSettings'])

        self.actions['help'] = QAction(
            QIcon(":/plugins/wincan2qgep/icons/help.svg"),
            self.tr("Help"),
            self.iface.mainWindow())
        self.actions['help'].triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/wincan2qgep")))
        self.iface.addPluginToMenu(self.name, self.actions['help'])

        self.actions['browse'] = QAction(
            QIcon(":/plugins/wincan2qgep/icons/test.svg"),
            self.tr("Browse data"),
            self.iface.mainWindow())
        self.actions['browse'].triggered.connect(self.test)
        self.iface.addPluginToMenu(self.name, self.actions['browse'])

        self.rubber = QgsRubberBand(self.iface.mapCanvas())
        self.rubber.setColor(QColor(255, 255, 50, 200))
        self.rubber.setIcon(self.rubber.ICON_CIRCLE)
        self.rubber.setIconSize(15)
        self.rubber.setWidth(4)
        self.rubber.setBrushStyle(Qt.NoBrush)

        self.test()

    def unload(self):
        """ Unload plugin """
        for action in self.actions.itervalues():
            self.iface.removePluginMenu(self.name, action)
        if self.rubber:
            self.iface.mapCanvas().scene().removeItem(self.rubber)
            del self.rubber

    @pyqtSlot(str, QgsMessageBar.MessageLevel)
    def displayMessage(self, message, level):
        self.iface.messageBar().pushMessage("Wincan 2 QGEP", message, level)

    def showSettings(self):
        if ConfigurationDialog().exec_():
            self._reloadFinders()

    def test(self):
        data = ImportData().data
        self.dlg = DataBrowserDialog(self.iface, data)
        self.dlg.show()



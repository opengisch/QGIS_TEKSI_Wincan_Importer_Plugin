#!/usr/bin/env python
# coding: utf-8 -*-

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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


ColumnHeaders = ['distance', 'code', 'description', 'mpeg', 'photo', 'gravité', 'forcer']
ColumnData = ['Position', 'OpCode', 'Text', 'MPEGPosition', 'PhotoFilename', 'Rate', 'ForceImport']


class ObservationTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.data = None
        self.projectId = None
        self.sectionId = None
        self.inspectionId = None

        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setMinimumSectionSize(15)
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setDefaultSectionSize(25)

        self.itemClicked.connect(self.import_checkbox_clicked)

    def finish_init(self, data):
        self.data = data
        for c, col in enumerate(ColumnHeaders):
            self.insertColumn(c)
            item = QTableWidgetItem(col)
            font = item.font()
            font.setPointSize(font.pointSize()-2)
            item.setFont(font)
            self.setHorizontalHeaderItem(c, item)
        self.adjustSize()

    def set_inspection(self, projectId, sectionId, inspectionId):
        self.clearContents()

        self.projectId = projectId
        self.sectionId = sectionId
        self.inspectionId = inspectionId

        for r in range(self.rowCount() - 1, -1, -1):
            self.removeRow(r)

        if self.projectId is None or self.sectionId is None or self.inspectionId is None:
            return

        for o_id, obs in self.data[self.projectId]['Sections'][self.sectionId]['Inspections'][self.inspectionId]['Observations'].items():
            r = self.rowCount()
            self.insertRow(r)

            for c, col in enumerate(ColumnData):
                item = QTableWidgetItem('{}'.format(obs[col] if c < 6 else ''))
                if c in (0, 6):
                    data_column = 'Import' if c == 0 else 'ForceImport'
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Checked if obs[data_column] else Qt.Unchecked)
                    item.setData(Qt.UserRole, o_id)
                    item.setData(Qt.UserRole+1, data_column)
                else:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                font = item.font()
                font.setPointSize(font.pointSize() - 2)
                item.setFont(font)
                self.setItem(r, c, item)

        self.resizeColumnsToContents()

    def import_checkbox_clicked(self, item):
        if item.flags() & Qt.ItemIsUserCheckable:
            o_id = item.data(Qt.UserRole)
            data_column = item.data(Qt.UserRole+1)
            self.data[self.projectId]['Sections'][self.sectionId]['Inspections'][self.inspectionId]['Observations'][o_id][data_column] = True if item.checkState() == Qt.Checked else False






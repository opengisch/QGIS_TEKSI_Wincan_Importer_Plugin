#!/usr/bin/env python
# coding: utf-8 -*-
#
# #-----------------------------------------------------------
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



from collections import OrderedDict
import xml.etree.ElementTree as ET
import os

from PyQt4.QtCore import QDate, QDateTime

# codes which should not be imported by default
SkipCode = ('BCD')

class ImportData():
    def __init__(self, filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        self.data = {}

        for child in root:

            # project
            if child.tag == 'P_T':
                self.data[child.find('P_ID').text] = dict(
                    RootPath=os.path.dirname(filepath),
                    Name=self.getValue(child, 'P_Name'),
                    Date=QDateTime.fromString(self.getValue(child, 'P_Date'), 'dd.MM.yyyy hh:mm:ss'),
                    Channel='',
                    Sections={})

                #print child.find('P_Name').text

            # section
            if child.tag == 'S_T':
                self.data[child.find('S_Project_ID').text]['Sections'][child.find('S_ID').text] = dict(
                    QgepChannelId1=None,
                    QgepChannelId2=None,
                    QgepChannelId3=None,
                    UsePreviousSection=False,
                    Counter=self.getValue(child, 'S_Counter'),
                    StartNode=self.getValue(child, 'S_StartNode'),
                    EndNode=self.getValue(child, 'S_EndNode'),
                    Sectionlength=float(self.getValue(child, 'S_Sectionlength')),
                    SectionUse=self.getValue(child, 'S_SectionUse'),
                    PipeMaterial=self.getValue(child, 'S_PipeMaterial'),
                    Profile=self.getValue(child, 'S_Profile'),
                    PipeDia=float(self.getValue(child, 'S_PipeDia')),
                    PipeWidth=float(self.getValue(child, 'S_PipeWidth')),
                    #Medianumber=self.getValue(child, 'S_Medianumber'),  # do not exist in XML
                    Inspections={},
                    Import=True)


            # inspection
            if child.tag == 'SI_T':
                found = False
                for p_id, project in self.data.items():
                    for s_id in project['Sections']:
                        if s_id == child.find('SI_Section_ID').text:
                            self.data[p_id]['Sections'][s_id]['Inspections'][child.find('SI_ID').text] = dict(
                                InspMethod=self.getValue(child, 'SI_InspMethod'),
                                InspectionDir=self.getValue(child, 'SI_InspectionDir'),
                                CodeInspectionDir=self.getValue(child, 'CodeSI_InspectionDir'),
                                InspectedLength=float(self.getValue(child, 'SI_InspectedLength') or 0),
                                Operator=self.getValue(child, 'SI_Operator'),
                                Weather=self.getValue(child, 'SI_Weather'),
                                InclinationFileName=self.getValue(child, 'SI_InclinationFileName'),
                                Cleaned=self.getValue(child, 'SI_Cleaned'),
                                InspDate=QDate.fromString(self.getValue(child, 'SI_InspDate'), 'dd.MM.yyyy'),
                                VideoName=self.getValue(child, 'SI_Virtual_x007E_ClipFilename'),
                                Observations={},
                                Import=True)
                            found = True
                            break
                    if found: break
                if not found:
                    raise ValueError('insepction has no section')

            # observation
            if child.tag == 'SO_T':
                found = False
                for p_id, project in self.data.items():
                    for s_id, section in project['Sections'].items():
                        for i_id in section['Inspections']:
                            if i_id == child.find('SO_Inspecs_ID').text:
                                code = self.getValue(child, 'SO_OpCode')
                                PhotoFilenames = []
                                i = 1
                                while True:
                                    pf = self.getValue(child, 'SO_PhotoFilename{}'.format(i))
                                    i += 1
                                    if pf is None:
                                        break
                                    PhotoFilenames.append(pf)
                                self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'][child.find('SO_ID').text] = dict(
                                    Counter=self.getValue(child, 'SO_Counter'),
                                    Position=float(self.getValue(child, 'SO_Position')),
                                    ToGoMeter=self.getValue(child, 'SO_ToGoMeter'),
                                    Text=self.getValue(child, 'SO_Text'),
                                    MPEGPosition=self.getValue(child, 'SO_MPEGPosition'),
                                    PhotoFilename=PhotoFilenames,
                                    Rate=int(round(float(self.getValue(child, 'SO_Rate') or 4))),
                                    OpCode=code,
                                    ClipFileName1=self.getValue(child, 'SO_ClipFileName1'),
                                    Quant1=self.getValue(child, 'SO_Quant1'),
                                    Quant2=self.getValue(child, 'SO_Quant2'),
                                    Quant1Unit=self.getValue(child, 'SO_Quant1Unit'),
                                    Quant2Unit=self.getValue(child, 'SO_Quant2Unit'),
                                    ObservCode=self.getValue(child, 'SO_ObservCode'),
                                    BendAngleDeg=self.getValue(child, 'SO_BendAngleDeg'),
                                    BendClockH=self.getValue(child, 'SO_BendClockH'),
                                    Import=True if code is not None and code not in SkipCode else False,
                                    ForceImport=False)  # force import if observation is out of channel (channel too short)
                                found = True
                                break
                    if found: break
                if not found:
                        raise ValueError('observation has no insepction')


        # order elements by counter
        for p_id in self.data.keys():
            self.data[p_id]['Sections'] = OrderedDict(sorted(self.data[p_id]['Sections'].items(), key=lambda t: int(t[1]['Counter'])))

            for s_id in self.data[p_id]['Sections'].keys():
                for i_id in self.data[p_id]['Sections'][s_id]['Inspections'].keys():
                    self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'] = OrderedDict( sorted(self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'].items(), key=lambda t: t[1]['Position']) )


    def getValue(self, node, tag):
        val = node.find(tag)
        if val is not None:
            return val.text
        else:
            #print 'tag {} not found'.format(tag)
            return None


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



# root p_t project
# s_t section
# si inspection
#
# so_t observation

import csv

from collections import OrderedDict

from PyQt4.QtCore import QDateTime


class ImportData():
    def __init__(self):

        self.data = {}
        with open('/home/drouzaud/Documents/qgis/wincan_import/project.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data[row['P_ID']] = dict(Name=row['P_Name'],
                                              Date=QDateTime.fromString(row['P_Date'], 'MM/dd/yy hh:mm:ss').addYears(100),
                                              Channel='',
                                              Sections={})

        with open('/home/drouzaud/Documents/qgis/wincan_import/section.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data[row['S_Project_ID']]['Sections'][row['S_ID']] = dict(
                    QgepChannelId=None,
                    Counter=row['S_Counter'],
                    StartNode=row['S_StartNode'],
                    EndNode=row['S_EndNode'],
                    Sectionlength=float(row['S_Sectionlength']),
                    SectionUse=row['S_SectionUse'],
                    PipeMaterial=row['S_PipeMaterial'],
                    Profile=row['S_Profile'],
                    PipeDia=float(row['S_PipeDia']),
                    PipeWidth=float(row['S_PipeWidth']),
                    Medianumber=row['S_Medianumber'],
                    Inspections={})


        with open('/home/drouzaud/Documents/qgis/wincan_import/inspection.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                found = False
                for p_id, project in self.data.items():
                    for s_id in project['Sections']:
                        if s_id == row['SI_Section_ID']:
                            self.data[p_id]['Sections'][s_id]['Inspections'][row['SI_ID']] = dict(
                                InspMethod=row['SI_InspMethod'],
                                InspectionDir=row['SI_InspectionDir'],
                                InspectedLength=float(row['SI_InspectedLength']),
                                Operator=row['SI_Operator'],
                                Weather=row['SI_Weather'],
                                InclinationFileName=row['SI_InclinationFileName'],
                                Cleaned=row['SI_Cleaned'],
                                InspDate=QDateTime.fromString(row['SI_InspDate'], 'MM/dd/yy hh:mm:ss').addYears(100),
                                Observations={},
                                Import=True)
                            found = True
                            break
                    if found: break
                if not found:
                    raise ValueError('insepction has no section')



        with open('/home/drouzaud/Documents/qgis/wincan_import/observation.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                found = False
                if row['SO_Rate'] == '':
                    continue
                for p_id, project in self.data.items():
                    for s_id, section in project['Sections'].items():
                        for i_id in section['Inspections']:
                            if i_id == row['SO_Inspecs_ID']:
                                self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'][row['SO_ID']] = dict(
                                    Counter=row['SO_Counter'],
                                    Position=float(row['SO_Position']),
                                    ToGoMeter=row['SO_ToGoMeter'],
                                    Text=row['SO_Text'],
                                    MPEGPosition=row['SO_MPEGPosition'],
                                    Photonumber1=row['SO_Photonumber1'],
                                    PhotoFilename1=row['SO_PhotoFilename1'],
                                    Rate=int(round(float(row['SO_Rate']))),
                                    OpCode=row['SO_OpCode'],
                                    ClipFileName1=row['SO_ClipFileName1'],
                                    Quant1=row['SO_Quant1'],
                                    Quant2=row['SO_Quant2'],
                                    Quant1Unit=row['SO_Quant1Unit'],
                                    Quant2Unit=row['SO_Quant2Unit'],
                                    ObservCode=row['SO_ObservCode'],
                                    BendAngleDeg=row['SO_BendAngleDeg'],
                                    BendClockH=row['SO_BendClockH'],
                                    Import=True)
                                found = True
                                break
                    if found: break
                if not found:
                        raise ValueError('observation has no insepction')

        # order elements by counter
        for p_id in self.data.keys():
            self.data[p_id]['Sections'] = OrderedDict(sorted(self.data[p_id]['Sections'].items(), key=lambda t: t[1]['Counter']))

            for s_id in self.data[p_id]['Sections'].keys():
                for i_id in self.data[p_id]['Sections'][s_id]['Inspections'].keys():
                    self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'] = OrderedDict( sorted(self.data[p_id]['Sections'][s_id]['Inspections'][i_id]['Observations'].items(), key=lambda t: t[1]['Position']) )



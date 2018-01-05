# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DrainageDockWidget
                                 A QGIS plugin
 Drainage
                             -------------------
        begin                : 2017-04-14
        git sha              : $Format:%H$
        copyright            : (C) 2017 by HermeSys
        email                : shpark@hermesys.co.kr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os,sys
from PyQt4 import uic
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsMapTool
# import Qtree
import Util
from FillSink_dialog import FillSinkDialog
from Flat_dialog import FlatDialog
from Catchment_dialog import CatchmentDialog
from Flow_Accumulation_dialog import Flow_AccumulationDialog
from Flow_Direction_dialog import Flow_DirectionDialog
from Slope_dialog import SlopeDialog
from Stream_Definition_dialog import Stream_DefinitionDialog
from Watershed_dialog import WatershedDialog
from Batch_Processor_dialog import BatchProcessor

import Drainage
# from SetupGRM_dialog import SetupGRMDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Drainage_dockwidget_base.ui'))


# 아이콘 경로들 임 추후에 변경 할것임
path=os.path.dirname(os.path.realpath(__file__))
Drainage_icon =  path +'\image\internet.png'
Cube = path + '\image\cube.png'
_util = Util.util()

class DrainageDockWidget(QtGui.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()
    def __init__(self, parent=None):
        """Constructor."""
        super(DrainageDockWidget, self).__init__(parent)
        self.setupUi(self)
        # 트리 위젯에 메뉴 항목을 넣는 부분임
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drainage")
        #배경 색상 회색
        # self.treeWidget.setStyleSheet("background-color: gray;")
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels([''])

        #Qtree 박스에 헤더 부분 제거
        self.treeWidget.setHeaderHidden(True)
        result=_util.CheckTaudem()
        if(result==False):
            _util.MessageboxShowError("Drainage","Taudem is not installed.")
        item10 = QtGui.QTreeWidgetItem(self.treeWidget, ['Drainage'])
        #2017-12-14 박: 기존 기능 한개로 통합 (batch processor) 로 변경 기존 파일은 그대로 유지
        #item11 = QtGui.QTreeWidgetItem(item10, ['Fill Sink'])
        #icon = QtGui.QIcon(Cube)
        #item11.setIcon(0, icon)
        #item12 = QtGui.QTreeWidgetItem(item10, ['Flat'])
        #icon = QtGui.QIcon(Cube)
        #item12.setIcon(0, icon)
        #item13 = QtGui.QTreeWidgetItem(item10, ['Flow Direction'])
        #icon = QtGui.QIcon(Cube)
        #item13.setIcon(0, icon)
        #item14 = QtGui.QTreeWidgetItem(item10, ['Flow Accumulation'])
        #icon = QtGui.QIcon(Cube)
        #item14.setIcon(0, icon)
        #item15 = QtGui.QTreeWidgetItem(item10, ['Slope'])
        #icon = QtGui.QIcon(Cube)
        #item15.setIcon(0, icon)
        #item16 = QtGui.QTreeWidgetItem(item10, ['Stream Definition'])
        #icon = QtGui.QIcon(Cube)
        #item16.setIcon(0, icon)

        item16 = QtGui.QTreeWidgetItem(item10, ['Batch Processor'])
        icon = QtGui.QIcon(Cube)
        item16.setIcon(0, icon)
        item17 = QtGui.QTreeWidgetItem(item10, ['Catchment GRID Delination'])
        icon = QtGui.QIcon(Cube)
        item17.setIcon(0, icon)
        item18 = QtGui.QTreeWidgetItem(item10, ['Create OutletPoint Layer and Draw OutletPoint'])
        icon = QtGui.QIcon(Cube)
        item18.setIcon(0, icon)
        item19 = QtGui.QTreeWidgetItem(item10, ['Watershed'])
        icon = QtGui.QIcon(Cube)
        item19.setIcon(0, icon)

        ##좌표계정보확인용 
        #item20 = QtGui.QTreeWidgetItem(item10, ['test'])
        #icon = QtGui.QIcon(Cube)
        #item20.setIcon(0, icon)

        icon = QtGui.QIcon(Drainage)
        item10.setIcon(0, icon)
        self.treeWidget.expandAll()

        self.mainLayout = QtGui.QGridLayout(self)
        self.mainLayout.addWidget(self.treeWidget)
        # 더블 클릭 했을대 메뉴 명칭 확인
        self.treeWidget.itemDoubleClicked.connect(self.onDoubleClick)


    def onDoubleClick(self, item):
        SelectItme = item.text(0)
        #2017-12-14 박: 기존 기능 한개로 통합 (batch processor) 로 변경 기존 파일은 그대로 유지
        #if SelectItme =='Flat':
        #     results_dialog = FlatDialog()
        #     results_dialog.exec_()
        #elif SelectItme =='Fill Sink':
        #    results_dialog = FillSinkDialog()
        #    results_dialog.exec_()
        #elif SelectItme =='Flow Direction':
        #    results_dialog = Flow_DirectionDialog()
        #    results_dialog.exec_()
        #elif SelectItme =='Flow Accumulation':
        #    results_dialog = Flow_AccumulationDialog()
        #    results_dialog.exec_()
        #elif SelectItme =='Slope':
        #    results_dialog = SlopeDialog()
        #    results_dialog.exec_()
        #elif SelectItme =='Stream Definition':
        #    results_dialog = Stream_DefinitionDialog()
        #    results_dialog.exec_()

        if SelectItme =='Batch Processor':
            results_dialog = BatchProcessor()
            results_dialog.exec_()

        elif SelectItme =='Catchment GRID Delination':
            results_dialog = CatchmentDialog()
            results_dialog.exec_()
        elif SelectItme == "Create OutletPoint Layer and Draw OutletPoint":
            _util.MessageboxShowInfo("info","The base layer and coordinate information must be created identically.")
            Drainage._iface.actionNewVectorLayer().trigger()
            #Edit 상태로 변환
            layer = Drainage._iface.activeLayer()
            layer.startEditing()
            #ADD 상태
            Drainage._iface.actionAddFeature().trigger()
        elif SelectItme =='Watershed':
            results_dialog = WatershedDialog()
            results_dialog.exec_()
        elif SelectItme =='Helps':
            results_dialog = Watershed_StetupDialog()
            results_dialog.exec_()
        #elif SelectItme =='test':
        #    layer = Drainage._iface.activeLayer()
        #    lyrCRS = layer.crs()
        #    if lyrCRS.isValid():
        #        _util.MessageboxShowInfo("lyrCRS",str(lyrCRS.toProj4()))


    def closeEvent(self, event):
            self.closingPlugin.emit()
            event.accept()


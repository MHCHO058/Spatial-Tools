# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WatershedDialog
                                 A QGIS plugin
 Watershed
                             -------------------
        begin                : 2017-04-04
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Hermesys
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
from PyQt4.QtGui import QFileDialog,QComboBox
from PyQt4.QtCore import QFileInfo
from qgis.gui import *
from qgis.core import QgsMapLayerRegistry,QgsVectorLayer,QgsRasterLayer
import os
import Util
from PyQt4 import QtGui, uic
import Drainage

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Watershed_dialog_base.ui'))

_util = Util.util()
class WatershedDialog(QtGui.QDialog, FORM_CLASS):

    # 저장 위치 출력 다이얼 로그
    def Select_Ouput_File(self):
        self.txtOutput.clear();
        if self.TifPath !="" and os.path.isdir(dir):
            dir = os.path.dirname(self.TifPath)
            filename = QFileDialog.getSaveFileName(self, "select output file ", dir, "*.tif")
        else : 
            filename = QFileDialog.getSaveFileName(self, "select output file ",os.getcwd() , "*.tif")
        self.txtOutput.setText(filename)

    # 콤보 박스에서 선택한 레이어의 경로 받아오기
    def Get_ComboBox_LayerPath(self, combo , txt):
        if combo.currentIndex() != 0:
            if txt =="tif":
                self.TifPath = _util.GetcomboSelectedLayerPath(combo)
            elif txt =="shp":
                self.Shape = _util.GetcomboSelectedLayerPath(combo).split('|')[0]

    # 레이어 목록 Qgis에 올리기
    def Addlayer_OutputFile(self, outputpath):
        if (os.path.isfile(outputpath)):
            fileName = outputpath
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            Drainage._iface.addRasterLayer(fileName, baseName)

    def Click_Okbutton(self):
        self.Get_ComboBox_LayerPath(self.cmbLayers ,"tif")
        self.Get_ComboBox_LayerPath(self.cmbShape , "shp")

        #콤보박스 레이어 선택 하지 않았을때
        Rindex = self.cmbLayers.currentIndex()
        Sindex = self.cmbShape.currentIndex()

        if Rindex == 0:
            _util.MessageboxShowInfo("Watershed", "\n No raster layer selected. \n")
            self.cmbLayers.setFocus()
            return

        if Sindex == 0:
            _util.MessageboxShowInfo("Watershed", "\n No shape layer selected. \n")
            self.cmbShape.setFocus()
            return

        # 텍스트 박스에 결과 파일 경로가 없을때 오류 메시지 출력
        if self.txtOutput.text() == "":
            _util.MessageboxShowInfo("Watershed", "\n File path not selected. \n")
            self.txtOutput.setFocus()
            return

        ## 확장자 TIF 만 허용
        #filename = os.path.splitext(self.txtOutput.text())[1]
        #if filename.upper() !=".TIF":
        #    _util.MessageboxShowInfo("Watershed", "\n Only TIF extensions are allowed. \n")
        #    self.txtOutput.setFocus()
        #    return


        # True 면 한글 포함 하고 있음, False 면 한글 없음
        if _util.CheckKorea(self.txtOutput.text()):
            _util.MessageboxShowInfo("Watershed", "\n The file path contains Korean. \n")
            return

        # 선택된 레이어 경로 한글 체크
        if _util.CheckKorea( self.TifPath):
            _util.MessageboxShowInfo("Watershed", "\n selected raster layer path contains Korean. \n")
            return

        # 선택된 레이어 경로 한글 체크
        if _util.CheckKorea(self.Shape):
            _util.MessageboxShowInfo("Watershed", "\n selected shape layer path contains Korean. \n")
            return

        # True 이면 기존 파일 존재함
        if _util.CheckFile(self.txtOutput.text()):
            _util.MessageboxShowInfo("Watershed", "\n A file with the same name already exists. \n")
            return

        #        arg = "C:\Program Files\TauDEM\TauDEM5Exe\GageWatershed.exe -p " + self.TifPath  + " -o " + self.Shape.split('|')[0] + " -gw " + self.txtOutput.text()
        #_util.MessageboxShowInfo("arg", arg)
        #returnValue=_util.Execute(arg)

        '''
        Watershed   진행 하기 전에 raster 파일과 shape 파일의 좌표계 정보가 다르면 
        파일이 잘 생성 되지 않을수 있다는 메시지 출력
        '''
       
        #레스터 레이어
        baseName =_util.GetFilename(self.TifPath)
        rlayer = QgsRasterLayer(self.TifPath, baseName)
        if rlayer.isValid():
             self.rcsr=self.layerCRS(rlayer)
        else : 
             self.rcsr=""
        #벡터 레이어
        name = _util.GetFilename(self.Shape)
        vlayer = QgsVectorLayer(self.Shape,name , "ogr")
        if vlayer.isValid():
            self.scsr=self.layerCRS(vlayer)
        if self.rcsr!=self.scsr:
            self.aboutApp()            
            #_util.MessageboxShowInfo(" Caution!!", "If the coordinate system of the two layers are different, there may be a problem in the watershed processing. ")

        # 타우프로그램 실행 시킬 arg 문자열 받아 오기
        arg = _util.GetWatershed(self.TifPath ,self.Shape, self.txtOutput.text())
        returnValue=_util.Execute(arg)
        if returnValue==0:
            self.Addlayer_OutputFile(self.txtOutput.text())
            _util.MessageboxShowInfo("Watershed", "processor complete")
            #self.close()

    def layerCRS(self,layer):
        lyrCRS = layer.crs()
        if lyrCRS.isValid():
            return lyrCRS.toProj4()
        else:
            return ""

    #정보창 띄움
    def aboutApp(self):
        website = "http://code.google.com/p/comictagger"
        email = "comictagger@gmail.com"
        Project = "test"
        msgBox = QtGui.QMessageBox()
        msgBox.addButton("Continue",QtGui.QMessageBox.AcceptRole)
        msgBox.addButton("Cancel",QtGui.QMessageBox.RejectRole)
        msgBox.setWindowTitle(self.tr("Caution!!"))
        msgBox.setTextFormat(QtCore.Qt.RichText)
        msgBox.setIconPixmap(QtGui.QPixmap(Project))
        msgBox.setText('If the coordinate system of the two layers are different, there may be a problem in the watershed processing.<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><font color=white>'+"{0},{1}</font><br><br>".format(website,email+"comictagger@gma"))
        
        self.addGroupWidget(msgBox)
        ret=msgBox.exec_()
        if ret == QtGui.QMessageBox.AcceptRole:
            pass
        else:
            self.post_grid_remove()
            self.rdo_selection()
            self.mapcanvas.refresh()
            self.scale_changed_mapcanvas()
            self.tool.scale_changed_disconnect()

    #메시지 창에 그룹 박스와 그룹 박스안 텍스트 창넣기
    def addGroupWidget (self, parentItem) :

        self.groupWidget = QtGui.QGroupBox(parentItem)
        self.groupWidget.setTitle("groupWidget")
        self.groupWidget.setGeometry (QtCore.QRect(10, 50, 480, 130)) #사이즈
        self.groupWidget.setObjectName ('groupWidget')
        
        self.groupWidget1 = QtGui.QGroupBox(parentItem)
        self.groupWidget1.setTitle("groupWidget")
        self.groupWidget1.setGeometry (QtCore.QRect(10, 190, 480, 130)) #사이즈
        self.groupWidget1.setObjectName ('groupWidget1')

        self.txtCSR_FD = QtGui.QTextEdit(self.groupWidget)
        self.txtCSR_FD.setGeometry(10,15,460,105)
        self.txtCSR_FD.setText(self.rcsr)

        self.txtCSR_Point = QtGui.QTextEdit(self.groupWidget1)
        self.txtCSR_Point.setGeometry(10,15,460,105)
        self.txtCSR_Point.setText(self.scsr)

    # 프로그램 종료
    def Close_Form(self):
        self.close()

    def __init__(self, parent=None):
        super(WatershedDialog, self).__init__(parent)
        self.setupUi(self)
        self.TifPath =""
        self.Shape =""
        #다이얼 로그 창 사이즈 조절 못하게 고정
        self.setFixedSize(self.size())

        # LineEdit 컨트롤러 초기화
        self.txtOutput.clear()

        # 레이어목록 콤보 박스 리스트 넣기 이벤트
        layers = Drainage._iface.legendInterface().layers()

        # 전달인자 layer 목록, 콤보박스,layertype("tif" or "shp" or ""-->전체 목록)
        _util.SetCommbox(layers, self.cmbLayers, "tif")
        _util.SetCommbox(layers, self.cmbShape, "shp")

        # 다이얼 로그 버튼 눌렀을때 파일 저장 경로 설정 이벤트
        self.btnOpenDialog.clicked.connect(self.Select_Ouput_File)

        # OK버튼 눌렀을때 처리 부분
        self.btnOK.clicked.connect(self.Click_Okbutton)

        # Cancle버튼 클릭 이벤트
        self.btnCancel.clicked.connect(self.Close_Form)
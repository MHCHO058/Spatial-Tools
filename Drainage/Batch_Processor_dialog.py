# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FillSinkDialog
                                 A QGIS plugin
 FillSink plug-in
                             -------------------
        begin                : 2017-03-13
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
from PyQt4.QtGui import QComboBox
from PyQt4.QtCore import QFileInfo
import os
import Util
from PyQt4 import QtGui, uic
import Drainage

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Batch_Processor_dialog_base.ui'))

_util = Util.util()
class BatchProcessor(QtGui.QDialog, FORM_CLASS):

    #레이어 목록 콤보 박스 셋팅
    def SetCombobox(self):
        layers = Drainage._iface.legendInterface().layers()
        _util.SetCommbox(layers, self.cmbLayer, "tif")

    #콤보 박스 선택시 이벤트 처리
    def SelectCombobox_event(self):
        index = self.cmbLayer.currentIndex()
        if index >0:
            self.LayerPath=_util.GetcomboSelectedLayerPath(self.cmbLayer)
            self.Layername=_util.GetFilename(self.LayerPath)
            self.txtFill.setText(self.Layername + "_Hydro")
            self.txtFlat.setText(self.Layername + "_Flat")
            self.txtFD.setText(self.Layername + "_Fdr")
            self.txtFAC.setText(self.Layername + "_Fac")
            self.txtSlope.setText(self.Layername + "_Slope")
            self.txtStream.setText(self.Layername + "_Stream")

    def Click_Okbutton(self):
        #레이어 경로에 한글이 있으면 오류로 처리 
        if _util.CheckKorea(self.LayerPath):
            _util.MessageboxShowInfo("Batch Processor", "\n The file path contains Korean. \n")
            return

        #파일 이름이 없는 텍스트 박스 확인
        self.checkTextbox(self.txtFill)
        self.checkTextbox(self.txtFlat)
        self.checkTextbox(self.txtFD )
        self.checkTextbox(self.txtFAC)
        self.checkTextbox(self.txtSlope)
        self.checkTextbox(self.txtStream)
        if self.txtCellValue.text() == "":
            _util.MessageboxShowError("Batch Processor", " CellValue is required. ")
            self.txtCellValue.setFocus()
            return False


        #파일 경로 변수에 셋팅
        self.SettingValue()

        #Fill sink 시작
        arg=_util.GetTaudemArg(self.LayerPath, self.Fill, _util.tauDEMCommand.SK, False,0)
        self.ExecuteArg(arg,self.Fill)

        #FD 시작
        arg = _util.GetTaudemArg(self.Fill, self.FD, _util.tauDEMCommand.FD, False,0)
        self.ExecuteArg(arg,self.FD)
        
        #FA 시작
        arg = _util.GetTaudemArg(self.FD, self.FAC, _util.tauDEMCommand.FA, False,0)
        self.ExecuteArg(arg,self.FAC)

        #Slope 시작
        arg = _util.GetTaudemArg(self.Fill,self.Slope, _util.tauDEMCommand.SG, False, 0)
        self.ExecuteArg(arg,self.Slope)

         #Stream 시작
        cellValue=self.txtCellValue.text()
        arg = _util.GetTaudemArg(self.FAC,self.Stream, _util.tauDEMCommand.ST, False, cellValue)
        self.ExecuteArg(arg,self.Stream)

        #tif 파일 asc 파일로 변환 
        self.ConvertTiff_To_Asc()

    #arg 받아서 처리 완료 되면 레이어  Qgis 에서 올림
    def ExecuteArg(self,arg,outpath):
        returnValue=_util.Execute(arg)
        if returnValue==0:
            #self.Addlayer_OutputFile(outpath)
            return True
        else:
            _util.MessageboxShowError("Batch Processor", " There was an error creating the file. ")
            return False
        
    # 레이어 목록 Qgis에 올리기
    def Addlayer_OutputFile(self, outputpath):
        if (os.path.isfile(outputpath)):
            fileName = outputpath
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            Drainage._iface.addRasterLayer(fileName, baseName)

    #파일 경로 변수에 셋팅
    def SettingValue(self):
        self.Fill=os.path.dirname(self.LayerPath) + "\\"+ self.txtFill.text() + ".tif"
        self.Flat=os.path.dirname(self.LayerPath) + "\\"+ self.txtFlat.text()+ ".tif"
        self.FD=os.path.dirname(self.LayerPath) + "\\"+ self.txtFD.text()+ ".tif"
        self.FAC=os.path.dirname(self.LayerPath) + "\\"+ self.txtFAC.text()+ ".tif"
        self.Slope=os.path.dirname(self.LayerPath) + "\\"+ self.txtSlope.text()+ ".tif"
        self.Stream=os.path.dirname(self.LayerPath) + "\\"+ self.txtStream.text()+ ".tif"
        self.CellValue= int(self.txtCellValue.text())
        

    #텍스트 박스에 파일 이름이 없는 경우 체크
    def checkTextbox(self,txt):
         if txt.text() == "":
            _util.MessageboxShowInfo("Batch Processor", " A filename is required. ")
            txt.setFocus()
            return

    #기본 변수 초기화
    def Settingfile(self):
        self.LayerPath="";self.Layername=""
        self.Fill="";self.Flat="";self.FD="";self.FAC=""
        self.Slope="";self.Stream="";self.CellValue=0


    # 프로그램 종료
    def Close_Form(self):
        self.close()

    def ConvertTiff_To_Asc(self):
        _util.Convert_TIFF_To_ASCii(self.Fill)
        _util.Convert_TIFF_To_ASCii(self.Flat)
        _util.Convert_TIFF_To_ASCii(self.FD)
        _util.Convert_TIFF_To_ASCii(self.FAC)
        _util.Convert_TIFF_To_ASCii(self.Slope)
        _util.Convert_TIFF_To_ASCii(self.Stream)
        
    def __init__(self, parent=None):
        """Constructor."""
        super(BatchProcessor, self).__init__(parent)
        self.setupUi(self)

        #파일 경로 변수 선언
        self.Settingfile()


        #콤보 박스 레이어 셋팅
        self.SetCombobox()

        #콤보 박스 선택 시 텍스트 창에 기본 파일 이름 적용 
        self.cmbLayer.currentIndexChanged.connect(self.SelectCombobox_event)

        # OK버튼 눌렀을때 처리 부분
        self.btnOK.clicked.connect(self.Click_Okbutton)

        # Cancle버튼 클릭 이벤트
        self.btnCancel.clicked.connect(self.Close_Form)



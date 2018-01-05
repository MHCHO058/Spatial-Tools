# -*- coding: utf-8 -*-
# SetupGRM_dialog.py
# copyrigth : (주)헤르메시스
#from fSetupRunGRM.SetupGRM_ui import _fromUtf8
from fileinput import filename


'''
작성일자 : 2017-04-07
프로그램 개요 : 캔버스 내에 도구 사용
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *
import sys, os
import resources_rc2
from PyQt4 import QtCore, QtGui

#ui가 없어도 dialog에서 처리가 가능함.
#단,resources_rc(n)은 필수적으로 필요 새로운 아이콘이 생겼으면 다시 추가해야 함.
#from SetupGRM_ui import Ui_SetupGRM

#qgis_prefix = os.getenv("C:\Users\mhcho058\.qgis2\python\plugins\fSetupRunGRM")

class SetupGRMdialog(QtGui.QMainWindow):
		
	def __init__(self, layer):
		#super(SetupGRMdialog, self).__init__(parent)
		#self.canvas = canvas
		QMainWindow.__init__(self)
		
		#만들어 둔 ui 사용
		#딱히 필요 없음, 사용하지 않습니다.
		#self.setupUi( self )
		#창 이름 Setup Run GRM 으로 변경
		self.setWindowTitle("Setup Run GRM")
		
		#canvas 생성
		self.canvas = QgsMapCanvas()
		
# 		self.reset()
# 		#현재 실행된 layer를 Canvas에 올리기
		self.canvas.setExtent(layer.extent())
		self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
# 		self.canvas.enableAntiAliasing(True)

#		widget에 canvas를 적용
		self.setCentralWidget(self.canvas)
		
		#기능  생성
		#zoom in 기능
		actionZoomIN = QAction(self)
		actionZoomIN.setIcon(QtGui.QIcon(':/plugins/fSetupRunGRM/img/zoomIN.png'))
		actionZoomIN.setObjectName("actionZoomIN")
        		
        #zoom out 기능
		actionZoomOut = QAction(self)
		actionZoomOut.setIcon(QtGui.QIcon(':/plugins/fSetupRunGRM/img/zoomOut.png'))
		actionZoomOut.setObjectName("actionZoomOut")
			
		#pan 기능
		actionPan = QAction(self)
		actionPan.setIcon(QtGui.QIcon(':/plugins/fSetupRunGRM/img/pan.png'))
		actionPan.setObjectName("actionPan")
		
		#레이어 추가
		actionAddLayer = QAction(self)
		actionAddLayer.setIcon(QtGui.QIcon(':/plugins/fSetupRunGRM/img/addLayer.png'))
		actionAddLayer.setObjectName("actionAddLayer")
  		
  		#information 기능(마우스 클릭한 지점의 좌표값)
  		actionInfo = QAction(self)
  		actionInfo.setIcon(QtGui.QIcon(':/plugins/fSetupRunGRM/img/info.png'))
  		actionInfo.setObjectName("actionInfo")
  		
		actionZoomIN.setCheckable(True)
		actionZoomOut.setCheckable(True)
		actionPan.setCheckable(True)
		actionAddLayer.setCheckable(False)
		actionInfo.setCheckable(True)
  		
  		#기능 함수 연결
		self.connect(actionZoomIN, SIGNAL("triggered()"), self.ZoomIN)
		self.connect(actionZoomOut, SIGNAL("triggered()"), self.ZoomOut)
		self.connect(actionPan, SIGNAL("triggered()"), self.Pan)
		self.connect(actionAddLayer, SIGNAL("triggered()"), self.AddLayer)
		#mouse event 
		self.connect(actionInfo,SIGNAL("triggered()"),self.Info)
  		
		#툴바 추가
		self.toolbar= self.addToolBar("ToolBar")
		self.toolbar.addAction(actionZoomIN)		
		self.toolbar.addAction(actionZoomOut)
		self.toolbar.addAction(actionPan)
		self.toolbar.addAction(actionAddLayer)
		self.toolbar.addAction(actionInfo)
  		
		#create the map tools
		self.toolZoomIN = QgsMapToolZoom(self.canvas, False)
		self.toolZoomIN.setAction(actionZoomIN)
		self.toolZoomOut = QgsMapToolZoom(self.canvas,True)
		self.toolZoomOut.setAction(actionZoomOut)
		self.toolPan = QgsMapToolPan(self.canvas)
		self.toolPan.setAction(actionPan)
		
		
  		
	
	#zoon in 기능 함수
	def ZoomIN(self):
		self.canvas.setMapTool(self.toolZoomIN)
	
	#zoom out 기능 함수			
	def ZoomOut(self):
		self.canvas.setMapTool(self.toolZoomOut)
	
	#pan 기능 함수	
	def Pan(self):
		self.canvas.setMapTool(self.toolPan)
		
	#information 기능 함수
	#마우스 이벤트를 사용, 클릭 시 좌표 값을 받아온다
	def Info(QMouseEvent):
		QgsMessageLog.logMessage("Click Mouse")
		cursor = QtGui.QCursor()
		#QgsMessageLog.logMessage(str(QMouseEvent.pos()))
		QgsMessageLog.logMessage(str(cursor.pos()))
		"""
		작성일자 : 2017-04-24 
		작성자 : 조민혜 
		Comment : 마우스 이벤트는 보완해야 합니다. 이제서야 마우스 이벤트가 먹히는 걸로 보아선 현재 진행 20%가 되었다고 생각합니다.
					  마우스가 캔버스 안에서 클릭했을 때 값이 나오게 해야 합니다.
					  현재는 버튼을 눌렀을 때 버튼의 위치값만 나오고 있습니다.
					 참고 https://gis.stackexchange.com/questions/45094/how-to-programatically-check-for-a-mouse-click-in-qgis
					 	http://stackoverflow.com/questions/19825650/python-pyqt4-how-to-detect-the-mouse-click-position-anywhere-in-the-window
		"""
		
		
		#QgsMessageLog.logMessage(str(layer.dataProvider().dataSourceUri()))
		#QgsMessageLog.logMessage(str(point))
	#add layer 기능 함수
	#Raster 레이어 올리기--어성공...? 2017/4/21
	
# 	def select_all(layer):
# 		layer.select(all)
# 		layer.setSelectedFeatures([obj.id() for obj in layer])
	
	def AddLayer(self):
		
# 		fileName="C:\\Users\\mhcho058\\.qgis2\\python\\plugins\\fSetupRunGRM\\shp\\logan_st.tif"
# 		fileInfo = QFileInfo(fileName)
# 		baseName = fileInfo.baseName()
		
# 		layer = QgsRasterLayer(fileName, baseName)

#		vector layer load
		path = "C:\\Users\mhcho058\\Desktop\\testplugin\\shp\\union\\test1.shp"
		name="test"
		provider = "ogr"
		
		layer = QgsVectorLayer(path, name, provider)
 		if not layer.isValid():
 			raise IOError, "Failed load layer"
		
		QgsMapLayerRegistry.instance().addMapLayer(layer,False)
 		self.canvas.setExtent(layer.extent())
 		self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
 		QgsMessageLog.logMessage("Success open layer")
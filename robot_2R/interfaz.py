# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interfaz_Robot_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 446)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_superior = QtWidgets.QFrame(self.frame)
        self.frame_superior.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_superior.setStyleSheet("\n"
"QFrame{\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton{\n"
"background-color: #000000ff;\n"
"border-radius:20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(53, 53, 79);\n"
"border-radius:20px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(30, 30, 50); /* Cambia el color de fondo cuando se presiona */\n"
"    border: 1px solid rgb(200, 200, 200); /* Cambia el color del borde cuando se presiona */\n"
"}\n"
"\n"
"\n"
"")
        self.frame_superior.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_superior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_superior.setObjectName("frame_superior")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_superior)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_superior)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imagenes/AREA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(30, 20))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.frame_superior)
        self.label.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
"color: rgb(20, 200, 220);")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(349, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_minimizar = QtWidgets.QPushButton(self.frame_superior)
        self.btn_minimizar.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_minimizar.setBaseSize(QtCore.QSize(40, 40))
        self.btn_minimizar.setStyleSheet("")
        self.btn_minimizar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imagenes/signo-menos.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_minimizar.setIcon(icon1)
        self.btn_minimizar.setIconSize(QtCore.QSize(30, 30))
        self.btn_minimizar.setObjectName("btn_minimizar")
        self.horizontalLayout_2.addWidget(self.btn_minimizar)
        self.btn_restaurar = QtWidgets.QPushButton(self.frame_superior)
        self.btn_restaurar.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_restaurar.setStyleSheet("")
        self.btn_restaurar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imagenes/minimizar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_restaurar.setIcon(icon2)
        self.btn_restaurar.setIconSize(QtCore.QSize(30, 30))
        self.btn_restaurar.setObjectName("btn_restaurar")
        self.horizontalLayout_2.addWidget(self.btn_restaurar)
        self.btn_maximizar = QtWidgets.QPushButton(self.frame_superior)
        self.btn_maximizar.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_maximizar.setStyleSheet("")
        self.btn_maximizar.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("imagenes/maximizar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_maximizar.setIcon(icon3)
        self.btn_maximizar.setIconSize(QtCore.QSize(30, 30))
        self.btn_maximizar.setObjectName("btn_maximizar")
        self.horizontalLayout_2.addWidget(self.btn_maximizar)
        self.btn_cerrar = QtWidgets.QPushButton(self.frame_superior)
        self.btn_cerrar.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_cerrar.setStyleSheet("")
        self.btn_cerrar.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("imagenes/cerrar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cerrar.setIcon(icon4)
        self.btn_cerrar.setIconSize(QtCore.QSize(30, 30))
        self.btn_cerrar.setObjectName("btn_cerrar")
        self.horizontalLayout_2.addWidget(self.btn_cerrar)
        self.verticalLayout_2.addWidget(self.frame_superior)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.toolBox = QtWidgets.QToolBox(self.frame_2)
        self.toolBox.setStyleSheet("\n"
"QToolBox::tab{\n"
"    background-color: rgb(255, 255, 255); \n"
"    border-radius: Spic;\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 8pt \"MS Shell Dig 2\";\n"
"}\n"
"\n"
"QToolBox::tab:selected {\n"
"    background-color: rgb(20, 200, 220);\n"
"    font: 75 12pt \"MS Shell Dig 2\";\n"
"    color: rgb(0, 0, 0);    \n"
"}\n"
"")
        self.toolBox.setObjectName("toolBox")
        self.Coordenadas_2 = QtWidgets.QWidget()
        self.Coordenadas_2.setGeometry(QtCore.QRect(0, 0, 370, 228))
        self.Coordenadas_2.setObjectName("Coordenadas_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.Coordenadas_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(20, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.Coordenadas_2)
        self.label_3.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: transparent;\n"
"qproperty-alignment: \'AlignCenter\';")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.Coordenadas_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(400, 50))
        self.label_4.setStyleSheet("font: 87 18pt \"Arial Black\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: transparent;\n"
"qproperty-alignment: \'AlignCenter\';")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.coor_x = QtWidgets.QPlainTextEdit(self.Coordenadas_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coor_x.sizePolicy().hasHeightForWidth())
        self.coor_x.setSizePolicy(sizePolicy)
        self.coor_x.setMaximumSize(QtCore.QSize(150, 30))
        self.coor_x.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.coor_x.setStyleSheet("QPlainTextEdit{\n"
"border:2px solid #14c8dc;\n"
"border-radius:8px;\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0); \n"
"font: 75 10pt \"Times New Roman\";\n"
"}")
        self.coor_x.setObjectName("coor_x")
        self.horizontalLayout_3.addWidget(self.coor_x)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.Coordenadas_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QtCore.QSize(400, 50))
        self.label_7.setStyleSheet("font: 87 18pt \"Arial Black\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: transparent;\n"
"qproperty-alignment: \'AlignCenter\';")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.coor_y = QtWidgets.QPlainTextEdit(self.Coordenadas_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coor_y.sizePolicy().hasHeightForWidth())
        self.coor_y.setSizePolicy(sizePolicy)
        self.coor_y.setMaximumSize(QtCore.QSize(150, 30))
        self.coor_y.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.coor_y.setStyleSheet("QPlainTextEdit{\n"
"border:2px solid #14c8dc;\n"
"border-radius:8px;\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0); \n"
"font: 75 10pt \"Times New Roman\";\n"
"}")
        self.coor_y.setObjectName("coor_y")
        self.horizontalLayout_4.addWidget(self.coor_y, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.aceptar_coor = QtWidgets.QPushButton(self.Coordenadas_2)
        self.aceptar_coor.setStyleSheet("\n"
"QPushButton{\n"
"    font: 87 12pt \"Arial Black\";\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(20, 200, 220); \n"
"    border-radius: 5px; \n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(53, 53, 79);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(30, 30, 50); /* Cambia el color de fondo cuando se presiona */\n"
"    border: 1px solid rgb(200, 200, 200); /* Cambia el color del borde cuando se presiona */\n"
"}")
        self.aceptar_coor.setObjectName("aceptar_coor")
        self.verticalLayout_6.addWidget(self.aceptar_coor)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        spacerItem4 = QtWidgets.QSpacerItem(20, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem4)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("imagenes/coordinar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.Coordenadas_2, icon5, "")
        self.Areadetrabajo_2 = QtWidgets.QWidget()
        self.Areadetrabajo_2.setGeometry(QtCore.QRect(0, 0, 370, 228))
        self.Areadetrabajo_2.setObjectName("Areadetrabajo_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.Areadetrabajo_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        spacerItem5 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem5)
        self.label_8 = QtWidgets.QLabel(self.Areadetrabajo_2)
        self.label_8.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: transparent;\n"
"qproperty-alignment: \'AlignCenter\';")
        self.label_8.setWordWrap(False)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem6 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.aceptar_areatrabajo = QtWidgets.QPushButton(self.Areadetrabajo_2)
        self.aceptar_areatrabajo.setStyleSheet("\n"
"QPushButton{\n"
"    font: 87 12pt \"Arial Black\";\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(20, 200, 220); \n"
"    border-radius: 5px; \n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(53, 53, 79);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(30, 30, 50); /* Cambia el color de fondo cuando se presiona */\n"
"    border: 1px solid rgb(200, 200, 200); /* Cambia el color del borde cuando se presiona */\n"
"}")
        self.aceptar_areatrabajo.setObjectName("aceptar_areatrabajo")
        self.horizontalLayout_6.addWidget(self.aceptar_areatrabajo)
        spacerItem7 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        spacerItem8 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem8)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("imagenes/brazo-robotico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.Areadetrabajo_2, icon6, "")
        self.Nombre_2 = QtWidgets.QWidget()
        self.Nombre_2.setGeometry(QtCore.QRect(0, 0, 370, 228))
        self.Nombre_2.setObjectName("Nombre_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.Nombre_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        spacerItem9 = QtWidgets.QSpacerItem(20, 54, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem9)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem10 = QtWidgets.QSpacerItem(21, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem10)
        self.label_9 = QtWidgets.QLabel(self.Nombre_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: transparent;\n"
"qproperty-alignment: \'AlignCenter\';")
        self.label_9.setWordWrap(False)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        spacerItem11 = QtWidgets.QSpacerItem(21, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem11)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem12)
        self.txt_nombre = QtWidgets.QPlainTextEdit(self.Nombre_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_nombre.sizePolicy().hasHeightForWidth())
        self.txt_nombre.setSizePolicy(sizePolicy)
        self.txt_nombre.setMaximumSize(QtCore.QSize(200, 30))
        self.txt_nombre.setStyleSheet("QPlainTextEdit{\n"
"border:2px solid #14c8dc;\n"
"border-radius:8px;\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0); \n"
"font: 75 10pt \"Times New Roman\";\n"
"\n"
"}")
        self.txt_nombre.setObjectName("txt_nombre")
        self.horizontalLayout_8.addWidget(self.txt_nombre)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem13)
        self.verticalLayout_10.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem14 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem14)
        self.aceptar_Nombre = QtWidgets.QPushButton(self.Nombre_2)
        self.aceptar_Nombre.setStyleSheet("\n"
"QPushButton{\n"
"    font: 87 12pt \"Arial Black\";\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(20, 200, 220); \n"
"    border-radius: 5px; \n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(53, 53, 79);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(30, 30, 50); /* Cambia el color de fondo cuando se presiona */\n"
"    border: 1px solid rgb(200, 200, 200); /* Cambia el color del borde cuando se presiona */\n"
"}")
        self.aceptar_Nombre.setObjectName("aceptar_Nombre")
        self.horizontalLayout_7.addWidget(self.aceptar_Nombre)
        spacerItem15 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem15)
        self.verticalLayout_10.addLayout(self.horizontalLayout_7)
        spacerItem16 = QtWidgets.QSpacerItem(20, 54, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem16)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("imagenes/firma-digital.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.Nombre_2, icon7, "")
        self.Imagenes_2 = QtWidgets.QWidget()
        self.Imagenes_2.setGeometry(QtCore.QRect(0, 0, 370, 228))
        self.Imagenes_2.setObjectName("Imagenes_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.Imagenes_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_7 = QtWidgets.QFrame(self.Imagenes_2)
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 59))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem17 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem17)
        self.label_10 = QtWidgets.QLabel(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setStyleSheet("QLabel {\n"
"    font-family: \"Arial Black\";\n"
"    font-size: 10pt; /* Ajusta el tamaÃ±o de la fuente segÃºn lo necesites */\n"
"    color: white; /* Ajusta el color del texto si es necesario */\n"
"    background-color: transparent; /* Asegura que el fondo sea transparente */\n"
"    word-wrap: break-word; /* Permite que el texto se ajuste en mÃºltiples lÃ­neas */\n"
"    white-space: normal; /* Permite que el texto se ajuste en mÃºltiples lÃ­neas */\n"
"    padding: 5px; /* AÃ±ade un poco de espacio alrededor del texto */\n"
"    border: none; /* Elimina el borde si no es necesario */\n"
"    min-width: 200px; /* Ajusta el ancho mÃ­nimo si es necesario */\n"
"}")
        self.label_10.setWordWrap(False)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        spacerItem18 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem18)
        self.verticalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout_11.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.Imagenes_2)
        self.frame_8.setStyleSheet("QFrame{\n"
"background-color: rgb(0,0, 0);\n"
"}\n"
"QPushButton{\n"
"    font: 87 12pt \"Arial Black\";\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(20, 200, 220); \n"
"    border-radius: 5px; \n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(53, 53, 79);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(30, 30, 50); /* Cambia el color de fondo cuando se presiona */\n"
"    border: 1px solid rgb(200, 200, 200); /* Cambia el color del borde cuando se presiona */\n"
"}")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_9 = QtWidgets.QFrame(self.frame_8)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.chevrolet = QtWidgets.QPushButton(self.frame_9)
        self.chevrolet.setObjectName("chevrolet")
        self.verticalLayout_13.addWidget(self.chevrolet)
        self.Apple = QtWidgets.QPushButton(self.frame_9)
        self.Apple.setObjectName("Apple")
        self.verticalLayout_13.addWidget(self.Apple)
        self.horizontalLayout_10.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(self.frame_8)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.hyundai = QtWidgets.QPushButton(self.frame_10)
        self.hyundai.setObjectName("hyundai")
        self.verticalLayout_14.addWidget(self.hyundai)
        self.Tesla = QtWidgets.QPushButton(self.frame_10)
        self.Tesla.setObjectName("Tesla")
        self.verticalLayout_14.addWidget(self.Tesla)
        self.horizontalLayout_10.addWidget(self.frame_10)
        self.verticalLayout_11.addWidget(self.frame_8)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("imagenes/ima.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.Imagenes_2, icon8, "")
        self.verticalLayout_3.addWidget(self.toolBox)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setStyleSheet("QLabel {\n"
"    font-family: \"Arial Black\";\n"
"    font-size: 10pt; /* Ajusta el tamaÃ±o de la fuente segÃºn lo necesites */\n"
"    color: white; /* Ajusta el color del texto si es necesario */\n"
"    background-color: transparent; /* Asegura que el fondo sea transparente */\n"
"    word-wrap: break-word; /* Permite que el texto se ajuste en mÃºltiples lÃ­neas */\n"
"    white-space: normal; /* Permite que el texto se ajuste en mÃºltiples lÃ­neas */\n"
"    padding: 5px; /* AÃ±ade un poco de espacio alrededor del texto */\n"
"    border: none; /* Elimina el borde si no es necesario */\n"
"    min-width: 200px; /* Ajusta el ancho mÃ­nimo si es necesario */    \n"
"qproperty-alignment: \'AlignCenter\';\n"
"}\n"
"\n"
"")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.verticalLayout_4.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_grafica = QtWidgets.QVBoxLayout()
        self.verticalLayout_grafica.setSpacing(0)
        self.verticalLayout_grafica.setObjectName("verticalLayout_grafica")
        self.horizontalLayout_12.addLayout(self.verticalLayout_grafica)
        self.verticalLayout_robot = QtWidgets.QVBoxLayout()
        self.verticalLayout_robot.setObjectName("verticalLayout_robot")
        self.horizontalLayout_12.addLayout(self.verticalLayout_robot)
        self.verticalLayout_4.addWidget(self.frame_6)
        self.horizontalLayout.addWidget(self.frame_4)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "ROBOT SCARA: Panel de Operaciones"))
        self.label_3.setText(_translate("MainWindow", "Ingrese las coordenadas X e Y deseadas:"))
        self.label_4.setText(_translate("MainWindow", "X"))
        self.label_7.setText(_translate("MainWindow", "Y"))
        self.aceptar_coor.setText(_translate("MainWindow", "ACEPTAR"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Coordenadas_2), _translate("MainWindow", "Coordenadas"))
        self.label_8.setText(_translate("MainWindow", "Iniciar Trayectoria del Ãrea de Trabajo"))
        self.aceptar_areatrabajo.setText(_translate("MainWindow", "ACEPTAR"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Areadetrabajo_2), _translate("MainWindow", "Areadetrabajo"))
        self.label_9.setText(_translate("MainWindow", "Ingrese un nombre (mÃ¡x. 9 letras):"))
        self.aceptar_Nombre.setText(_translate("MainWindow", "ACEPTAR"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Nombre_2), _translate("MainWindow", "Nombre"))
        self.label_10.setText(_translate("MainWindow", "Seleccione una imagen de las opciones:"))
        self.chevrolet.setText(_translate("MainWindow", "Chevrolet"))
        self.Apple.setText(_translate("MainWindow", "Apple"))
        self.hyundai.setText(_translate("MainWindow", "Hyundai"))
        self.Tesla.setText(_translate("MainWindow", "Tesla"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Imagenes_2), _translate("MainWindow", "Imagenes"))
        self.label_2.setText(_translate("MainWindow", "Panel de visualizaciÃ³n del Robot"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
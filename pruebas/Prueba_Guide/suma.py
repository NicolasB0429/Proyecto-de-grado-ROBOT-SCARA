# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'suma.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.lbl_titulo = QtWidgets.QLabel(Form)
        self.lbl_titulo.setGeometry(QtCore.QRect(190, 40, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbl_titulo.setFont(font)
        self.lbl_titulo.setMouseTracking(False)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.txt_num1 = QtWidgets.QTextEdit(Form)
        self.txt_num1.setGeometry(QtCore.QRect(50, 130, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txt_num1.setFont(font)
        self.txt_num1.setObjectName("txt_num1")
        self.lbl_icon_suma = QtWidgets.QLabel(Form)
        self.lbl_icon_suma.setGeometry(QtCore.QRect(190, 130, 30, 40))
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_icon_suma.setFont(font)
        self.lbl_icon_suma.setObjectName("lbl_icon_suma")
        self.txt_num2 = QtWidgets.QTextEdit(Form)
        self.txt_num2.setGeometry(QtCore.QRect(240, 130, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txt_num2.setFont(font)
        self.txt_num2.setObjectName("txt_num2")
        self.lbl_icon_igual = QtWidgets.QLabel(Form)
        self.lbl_icon_igual.setGeometry(QtCore.QRect(380, 130, 30, 40))
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_icon_igual.setFont(font)
        self.lbl_icon_igual.setObjectName("lbl_icon_igual")
        self.lbl_nombres = QtWidgets.QLabel(Form)
        self.lbl_nombres.setGeometry(QtCore.QRect(120, 260, 170, 100))
        self.lbl_nombres.setObjectName("lbl_nombres")
        self.btn_calcular = QtWidgets.QPushButton(Form)
        self.btn_calcular.setGeometry(QtCore.QRect(250, 200, 99, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.btn_calcular.setFont(font)
        self.btn_calcular.setMouseTracking(False)
        self.btn_calcular.setTabletTracking(False)
        self.btn_calcular.setAutoFillBackground(False)
        self.btn_calcular.setCheckable(False)
        self.btn_calcular.setAutoRepeat(False)
        self.btn_calcular.setObjectName("btn_calcular")
        self.lbl_resultado = QtWidgets.QLabel(Form)
        self.lbl_resultado.setGeometry(QtCore.QRect(440, 130, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_resultado.setFont(font)
        self.lbl_resultado.setText("")
        self.lbl_resultado.setObjectName("lbl_resultado")
        self.lbl_icon_ecci = QtWidgets.QLabel(Form)
        self.lbl_icon_ecci.setGeometry(QtCore.QRect(340, 260, 191, 121))
        self.lbl_icon_ecci.setText("")
        self.lbl_icon_ecci.setPixmap(QtGui.QPixmap("icono_ecci.png"))
        self.lbl_icon_ecci.setScaledContents(True)
        self.lbl_icon_ecci.setObjectName("lbl_icon_ecci")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_titulo.setText(_translate("Form", "PRUEBA SUMA"))
        self.lbl_icon_suma.setText(_translate("Form", "+"))
        self.lbl_icon_igual.setText(_translate("Form", "="))
        self.lbl_nombres.setText(_translate("Form", "  Angie Paola Mancipe\n"
"Nicolas Barrera Fonseca\n"
"  Igenieria Mecatronica\n"
"                2024"))
        self.btn_calcular.setText(_translate("Form", "CALCULAR"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
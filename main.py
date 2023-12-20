from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QComboBox
from PyQt5.QtGui import QTextDocument, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtXml import QDomElement
from PyQt5 import uic
from math import *
from cmath import cos, sin, sqrt, pi
import sys
import numpy
from sympy import *

from Matrix import *
from IntegralCalc import *
from ExtCalc import *
from Deriative import *
from BaseCalc import *
from FunctionCourse import *
from Limit import *


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.loadMainUI()
        self.show()

    def loadMainUI(self):
        uic.loadUi("UIs/main.ui", self)
        self.btnBaseCalc.clicked.connect(self.loadBaseCalcUI)
        self.btnAdvCalc.clicked.connect(self.loadAdvCalcUI)
        self.btnMatrixCalc.clicked.connect(self.loadMatrixMenuUI)
        self.btnFunctions.clicked.connect(self.loadFunctionCourse)
        


    def loadBaseCalcUI(self):
        ui = uic.loadUi("UIs/BaseCalc.ui",self)
        self.baseCalc = BaseCalc(self.labelResult, self.labelError)

        self.addEvents(ui, self.baseCalc.updateResult)

        self.btnBack.clicked.connect(self.loadMainUI)
        self.btnAllClear.clicked.connect(self.baseCalc.allClear)
        self.btnClear.clicked.connect(self.baseCalc.clearCalc)
        self.btnEqual.clicked.connect(self.baseCalc.evaluate)

    def loadAdvCalcUI(self):
        uic.loadUi("UIs/AdvancedCalc/AdvCalc.ui",self)
        self.btnDer.clicked.connect(self.loadDerUI)
        self.btnExt.clicked.connect(self.loadExtUI)
        self.btnInt.clicked.connect(self.loadIntUI)
        self.btnBack.clicked.connect(self.loadMainUI)
        self.btnLim.clicked.connect(self.loadLimUI)

    def loadExtUI(self):
        ui = uic.loadUi("UIs/AdvancedCalc/ext.ui", self)
        self.ExtCalc = ExtCalc(self.funkcja, self.wynik, self.labelError)
        self.addEvents(ui, self.ExtCalc.updateDisplay)
        self.btnAC.clicked.connect(self.ExtCalc.allClear)
        self.btnC.clicked.connect(self.ExtCalc.clear)
        self.btnBack.clicked.connect(self.loadMainUI)
        self.btnRun.clicked.connect(self.ExtCalc.evaluate)

    def loadIntUI(self):
        ui = uic.loadUi("UIs/AdvancedCalc/Int.ui", self)
        self.IntegralCalc = IntegralCalc(self.funkcja, self.wynik, ui, self.labelInfo)
        
        self.addEvents(ui, self.IntegralCalc.updateDisplay)
       
        self.btnAC.clicked.connect(self.IntegralCalc.allClear)
        self.btnC.clicked.connect(self.IntegralCalc.clear)
        self.btnBack.clicked.connect(self.loadMainUI)
        self.btnRun.clicked.connect(self.IntegralCalc.evaluate)

    def loadDerUI(self):
        ui = uic.loadUi("UIs/AdvancedCalc/Deriative.ui", self)
        self.Deriative = Deriative(self.funkcja, self.f1, self.f2, self.labelError, ui, self.fn)

        self.addEvents(ui, self.Deriative.updateDisplay)

        self.btnPoX.toggled.connect(lambda: self.Deriative.selectX())
        self.btnPoY.toggled.connect(lambda: self.Deriative.selectY())
        self.btnAC.clicked.connect(self.Deriative.allClear)
        self.btnC.clicked.connect(self.Deriative.clear)
        self.btnBack.clicked.connect(self.loadMainUI)
        self.btnRun.clicked.connect(self.Deriative.checkRadio)

    def loadMatrixMenuUI(self):
        uic.loadUi("UIs/MatrixCalc/matrixMenu.ui", self)
        self.btnOneMatrixCalc.clicked.connect(self.loadOneMatrixCalc)
        self.btnTwoMatrixCalc.clicked.connect(self.loadTwoMatrixCalc)
        self.btnBack.clicked.connect(self.loadMainUI)

    def loadOneMatrixCalc(self):
        ui = uic.loadUi("UIs/MatrixCalc/oneMatrixCalc.ui",self)
        self.oneMatrixCalc = OneMatrixCalc(ui)
        self.btnDet.clicked.connect(self.oneMatrixCalc.calcDet)
        self.btnComplement.clicked.connect(self.oneMatrixCalc.calcComplement)
        self.btnInverse.clicked.connect(self.oneMatrixCalc.calcInverse)
        self.btnCondition.clicked.connect(self.oneMatrixCalc.calcCondition)
        self.btnNorm.clicked.connect(self.oneMatrixCalc.calcNorm)
        self.btnRank.clicked.connect(self.oneMatrixCalc.calcRank)
        self.btnSum.clicked.connect(self.oneMatrixCalc.calcSum)
        self.btnTrace.clicked.connect(self.oneMatrixCalc.calcTrace)
        self.btnTranspose.clicked.connect(self.oneMatrixCalc.calcTranspose)
        self.btnBack.clicked.connect(self.loadMatrixMenuUI)


    def loadLimUI(self):
        ui = uic.loadUi("UIs/AdvancedCalc/Lim.ui", self)
        self.LimitCalc = Limitt(self.labelInput, self.labelError, ui)
        
        self.addEvents(ui, self.LimitCalc.updateDisplay)
       
        self.btnAllClear.clicked.connect(self.LimitCalc.allClear)
        self.btnClear.clicked.connect(self.LimitCalc.clear)
        self.btnBack.clicked.connect(self.loadAdvCalcUI)
        self.btnRun.clicked.connect(self.LimitCalc.evaluate)

    def loadTwoMatrixCalc(self):
        ui = uic.loadUi("UIs/MatrixCalc/twoMatrixCalc.ui",self)
        self.twoMatrixCalc = TwoMatrixCalc(ui)
        self.btnCalculate.clicked.connect(self.twoMatrixCalc.calculate)
        self.btnBack.clicked.connect(self.loadMatrixMenuUI)

    def loadFunctionCourse(self):
        ui = uic.loadUi("UIs/FunctionCourse.ui", self)
        self.functionCourse = FunctionCourse(ui)
        self.addEvents(ui, self.functionCourse.updateDisplay)
        
        self.btnBack.clicked.connect(self.loadMainUI)
        self.btnAllClear.clicked.connect(self.functionCourse.allClear)
        self.btnClear.clicked.connect(self.functionCourse.clear)
        self.btnRun.clicked.connect(self.functionCourse.createNewWindow)

        
    def addEvents(self, ui, function):
            buttons = ui.findChildren(QPushButton)
            btnValues = ["0","1","2","3","4","5","6","7","8","9","+","-","/","×","*",")","(",   \
                         ".","cos","e","π","^","sin","√","x","y", "n", "!"]
            for btn in buttons:
                value = btn.text()
                if value in btnValues:
                    if value=="×": value = "*"
                    if value=="cos" or value=="^" or value=="sin" or value=="√": value += "("
                    btn.clicked.connect(lambda ch, text=value: function(text))
  


app = QApplication(sys.argv)
window = App()
app.exec_()
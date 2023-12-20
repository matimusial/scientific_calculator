from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QComboBox
from PyQt5.QtGui import QTextDocument, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QTimer
from PyQt5.QtXml import QDomElement
from PyQt5 import uic
from math import *
from cmath import cos, sin, sqrt, pi
import sys
import numpy
from sympy import *

class Functions():

   def updateResult(self, val):
        if not self.validateInput(val): return
         
        self.result += val   
        self.updateLabel(self.result)

   def updateDisplay(self, val):
        if not self.validateInput(val): return
        if val == "*":
             if self.result[-1] == "(": return
             self.display += val
             self.result += "*"

        elif val == "e":
            if (self.result == "" or (self.result[-1].isdigit()) == False):
                self.result += "exp(1)"
                self.display += val
            elif ((self.result[-1].isdigit()) == True or self.result[-1] in [")","pi","x","y", "exp(1)"]):
                self.display += "*e"
                self.result += "*exp(1)"



        elif val == "^(":
            if self.result[-1] in ["**","*","("]: return
            self.display += val
            self.result += "**(" 
        elif val == "√(":
            self.display += val
            self.result += "sqrt("
        elif val == "x":
            if (self.result == "" or (self.result[-1].isdigit()) == False):
                self.result += "x"
                self.display +="x"
            elif ((self.result[-1].isdigit()) == True or self.result[-1] in [")","pi","x","y"]):
                self.display += "*x"
                self.result += "*x"

        elif val == "π":
            if (self.result == "" or (self.result[-1].isdigit()) == False):
                self.result += "pi"
                self.display +="π"
            elif ((self.result[-1].isdigit()) == True or self.result[-1] in [")","pi","x","y"]):
                self.display += "*π"
                self.result += "*pi"




        elif val == "n":
            if (self.result == "" or self.result[-1] != "n" or (self.result[-1].isdigit()) == False):
                self.result += "n"
                self.display +="n"
            elif ((self.result[-1].isdigit()) == True or self.result[-1] in [")","pi","n"]):
                self.display += "*n"
                self.result += "*n"


        elif val == "y":
            if (self.result == "" or (self.result[-1].isdigit()) == False):
                self.result += "y"
                self.display +="y"
            elif ((self.result[-1].isdigit()) == True or self.result[-1] in [")","pi","x","y"]):
                self.display += "*y"
                self.result += "*y"


        else:
            self.display += val
            self.result += val
        print(self.result)
        self.updateLabel(self.display)


   def updateLabel(self, value):
        self.label.setText(value)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

   def clear(self):
        if self.result == "": return
        if self.result[-2:] == "pi":
            self.display = self.display[:-1]
            self.result = self.result[:-2]
        elif self.result[-4:] =="cos(" :
            self.display = self.display[:-4]
            self.result = self.result[:-4]
        elif self.result[-4:] =="sin(" :
            self.display = self.display[:-4]
            self.result = self.result[:-4]
        elif self.result[-5:] =="sqrt(" :
            self.display = self.display[:-2]
            self.result = self.result[:-5]
        elif self.result[-3:] =="**(" :
            self.display = self.display[:-2]
            self.result = self.result[:-3]
        else:
            self.display = self.display[:-1]
            self.result = self.result[:-1]
        self.updateLabel(self.display)

    # weryfikacja dla inputu 
   def validateInput(self, val):
        #   1. pierwszy znak to operator (inny od minusa)
        #   2. poprzedni i kolejny znak to operatory
        #   3. poprzedni znak to nawias otwierajacy a kolejny to operator
        #   4. kolejny znak to nawias i nie przechodzi walidacji
        if (not self.result and val in ["/","*","+"]) \
        or (self.result and self.result[-1] in ["/","*","+","-"] and val in ["/","*","+"]) \
        or (self.result and self.result[-1] == "(" and val in ["/","*","+"])    \
        or (val in ["(",")"] and not self.validatePars(val)): return False

        #   dodaje 0 przed kropką jesli zostanie ona napisana na poczatku lub po operatorze
        if (not self.result or self.result[-1] in ["/","*","+","-"]) and val == ".": 
            self.result += "0"

        #   dodaje nawias otwierający jesli poprzedni znak to operator a kolejny to minus (w domyśle: zostanie wpisana liczba ujemna)
        if(self.result and self.result[-1] in ["/","*","+","-"] and val=="-"):
            self.result += "("
            
        if(self.result and self.result[-1].isdigit() and val in ["sin(", "cos(", "√("]):
            self.result += "*"
            self.display += "*"
        if(self.result and self.result[-1]=="x" and val=="x"):
            self.result += "*"
            self.display += "*"
        return True

    # osobna weryfikacja dla nawiasow
   def validatePars(self, val):
        openPars = self.result.count("(")
        closePars = self.result.count(")")
        
        #   1. poprzedni znak to nawias otwierajacy a kolejny to nawias zamykajacy
        #   2. wynik jest pusty a kolejny znak to nawias zamykajacy
        #   3. kolejny znak to nawias zamykajacy a wynik nie posiada otwierającego
        #   4. kolejny znak to nawias zamykający a liczba nawiasow otwierajacych i zamykajacych jest rowna (kazdy ma pare)
        if (val == ")" and self.result and self.result[-1] == "(") \
        or (val == ")" and not self.result) \
        or (val == ")" and self.result and "(" not in self.result)  \
        or (val == ")" and openPars == closePars): return False

        #   dodaje znak mnożenia jeśli poprzedni znak to nawias lub cyfra zamykający a kolejny to nawias otwierający
        if(val == "(" and self.result and (self.result[-1] == ")" or self.result[-1].isdigit())):
            self.result += "*"

        return True

    # pobiera to co aktualnie jest w labelu z wynikiem
   def getDataFromLabel(self):   
        doc = QTextDocument()
        doc.setHtml(self.label.text())
        text = doc.toPlainText()
        return text
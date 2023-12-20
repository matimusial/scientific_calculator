from Functions import *
import tokenize

class IntegralCalc(Functions):

    def __init__(self, label, wynik, ui, info):
        self.result = ""
        self.display = ""
        self.var1 = ""
        self.var2 = ""
        self.label = label
        self.wynik = wynik
        self.ui = ui
        self.info = info

        self.varValidator = QRegExpValidator(QRegExp('^(-?[0-9]+[.]?[0-9]+|oo|e|pi)$'))
        self.varUp = self.ui.findChild(QLineEdit, "varUp")
        self.varDown = self.ui.findChild(QLineEdit, "varDown")
        self.varUp.setValidator(self.varValidator)
        self.varDown.setValidator(self.varValidator)
        super().__init__()

    def evaluate(self):
        try:
            if self.result == "": return
            self.var1 = self.varDown.text()
            self.var2 = self.varUp.text() 
            print(self.var1,self.var2)
            x = Symbol("x")
            fun = sympify(self.result)
            if(self.var1=="e"):
                    self.var1="exp(1)" 
            if(self.var2=="e"):
                    self.var2="exp(1)"   
            if self.var1 == "" and self.var2 == "":
                self.info.setText("Całka nieoznaczona")
                QTimer.singleShot(8000, lambda: self.info.setText(""))
                integrateValue = integrate(fun,  x)
            elif self.var1 == "":
                self.info.setText("Dolny przedział całki nie został podany, przedział domyślny -oo")
                QTimer.singleShot(8000, lambda: self.info.setText(""))           
                integrateValue = integrate(fun, (x ,-inf, self.var2))
                integrateValue = round(float(integrateValue.evalf()),3)
            elif self.var2 == "":
                self.info.setText("Górny przedział całki nie został podany, przedział domyślny oo")
                QTimer.singleShot(8000, lambda: self.info.setText(""))

                integrateValue = integrate(fun, (x ,self.var1, inf))
                integrateValue = round(float(integrateValue.evalf()),3)
            else:

                integrateValue = integrate(fun, (x ,self.var1, self.var2))
                integrateValue = round(float(integrateValue.evalf()),3)
            
            self.result = ""
            self.display = ""
            self.setResult(self.RelaseResult(str(integrateValue)))
        except ZeroDivisionError:
            self.error.setText("Nie mozna dzielic przez 0")
        except SyntaxError:
            self.error.setText("Użyto nieprawidłowego formatu")

        except Exception:
            self.error.setText("Nasz kalkulator tego nie obliczy")

        except tokenize.TokenError:
            self.error.setText("Użyto nieprawidłowego formatu")

    def RelaseResult(self, value): 
        return value.replace("**","^").replace("sqrt", "√").replace("pi","π")

    def setResult(self, integrateValue):
        self.label.setText("")
        self.result = ""
        self.wynik.setText(integrateValue)
        self.wynik.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    
    def allClear(self):
        self.result = ""
        self.display = ""
        self.wynik.setText("")
        self.label.setText("")
        self.wynik.setText(self.display)
        self.updateLabel(self.display)

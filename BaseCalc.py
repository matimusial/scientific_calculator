from Functions import *

class BaseCalc(Functions):
    def __init__(self, label, error):
        self.result = ""
        self.label = label
        self.error = error
        self.display=""
        super().__init__()

    def evaluate(self):
        try:
            value = str(eval(self.result))
            self.setResult(value)
            self.result = value
        except ZeroDivisionError:
            self.error.setText("Nie mozna dzielic przez 0")
            QTimer.singleShot(4000, lambda: self.error.setText(""))
        except SyntaxError:
            self.error.setText("Użyto nieprawidłowego formatu")
            QTimer.singleShot(4000, lambda: self.error.setText(""))

    def setResult(self, value):
        self.label.setText(value)
        self.result = ""
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def clearCalc(self):
        if self.result == "": return
        self.result = self.result[:-1]
        self.updateLabel(self.result)

    def allClear(self):
        if self.result == "": return
        self.result = ""
        self.updateLabel(self.result)
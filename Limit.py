from Functions import *
from sympy import limit, Symbol, sympify, oo

class Limitt(Functions):
    def __init__(self, label, error, ui):
            self.result = ""
            self.display = ""
            self.label = label
            self.error = error
            self.ui = ui
            super().__init__()


    def evaluate(self):
        try:
            if self.result == "": return
            if "n" not in self.result: self.allClear()
            n = Symbol("n")
            stringg = limit(sympify(self.result),n,oo)
            if stringg == oo: stringg = "∞"
            self.label.setText(str(stringg))

        except SyntaxError:
            self.error.setText("Zły format")

        except Exception:
            self.error.setText("Nasz kalkulator tego nie obliczy")


    def clear(self):
        if self.result == "": return
        self.result = self.result[:-1]
        self.display = self.display[:-1]
        self.updateLabel(self.result)

    def allClear(self):
        if self.result == "": return
        self.result = ""
        self.display = ""
        self.updateLabel(self.result)
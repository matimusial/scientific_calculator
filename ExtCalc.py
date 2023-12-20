from Functions import *
import numpy as np
import matplotlib.pyplot as plt
import tokenize
from sympy.solvers import solve
from sympy.abc import x
from sympy import sympify

class ExtCalc(Functions):

    def __init__(self, label, function, error):
        self.result = ""
        self.display = ""
        self.label = label
        self.function = function
        self.error = error
        self.lista = []
        self.wynik = 0
        super().__init__()

   

    def evaluate(self):
            try:
                if self.result == "": return
                if "x" not in self.result: return
                def getDeepDotQuality(func, arg, val, n = 3):
                  dy = func.diff(arg)
                  dyn = dy.subs(arg, val)
                  if (dyn == 0):
                    return getDeepDotQuality(dy, arg, val, n+1)
                  elif (n % 2 == 1):
                    return 'ma punkt przegięcia'
                  elif (dyn > 0):
                    return 'jest minimum'
                  else:
                    return 'jest maximum'
                  return

                def getDotQuality(func, arg, val):
                  dy = func.subs(arg, val)
                  if (dy > 0):
                    return 'jest minimum'
                  elif (dy < 0):
                    return 'jest maximum'
                  else:
                    return getDeepDotQuality(func, arg, val)

                def findExtremums(func):
                  dy = func.diff(x)
                  ddy = dy.diff(x)
                  extremums = solve(dy, x)
                  string = ""
                  for val in extremums:
                    string += (('%s dla x=%s' % (getDotQuality(ddy, x, val), val))+("\n"))

                  self.function.setText(string)
                  return
                   
                findExtremums(sympify(self.result))

            except ZeroDivisionError:
                self.error.setText("Nie mozna dzielic przez 0")
            except SyntaxError:
                self.error.setText("Zły format")

            except tokenize.TokenError:
                self.error.setText("Użyto nieprawidłowego formatu")  

            except Exception:
                self.error.setText("Nasz kalkulator tego nie obliczy")

    def allClear(self):
        if self.result == "": return
        self.result = ""
        self.display = ""
        self.function.setText("")
        self.updateLabel(self.display)
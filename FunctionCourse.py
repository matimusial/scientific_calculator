import numpy as np
import sympy
import matplotlib.pyplot as plt
from sympy.calculus.util import continuous_domain
from Functions import *
from PyQt5.QtWidgets import QWidget
import tokenize

class FunctionCourse(Functions):
     def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.result = ""
        self.display = ""
        self.label = self.ui.findChild(QLabel, "labelInput")

     def createNewWindow(self):
        function = self.result
        self.w = CourseResult()
        self.w.save.clicked.connect(self.saveCourse)
        self.w.show()
        self.calculate(function)

     def allClear(self):
        self.result = ""
        self.display = ""
        self.label.setText("")
        self.updateLabel(self.display)
    
     def calculate(self, function):
         try:
            f = function
            x = sympy.Symbol('x')

            # Dziedzina (działa)
            f = sympy.sympify(f)
            dziedzina = continuous_domain(f, x, sympy.S.Reals)

            domainString=""
            for el in dziedzina.args:
                domainString+=f"{str(el).replace('Interval.open','')} ∪ "
            self.w.dziedzina.setText(f"\t{domainString[:-2] if domainString != '' else dziedzina}")
            # Miejsca zerowe (działa)
            miejsca_zerowe = sympy.solveset(f, x, domain=sympy.S.Reals)
            zeroweString = ""
            for idx, el in enumerate(miejsca_zerowe):
                el = round(float(el.evalf()), 2)
                zeroweString += f"({el},0), "
                if(idx==10): break
            self.w.zerowe.setText(f"\t{zeroweString[:-2]}")

            # Punkt przecięcia z osią Oy
            punkt_przeciecia = f.subs(x, 0, domain=sympy.S.Reals)
            self.w.oy.setText(f"\t(0, {punkt_przeciecia})")

            # Asymptoty
            asymptoty_pionowe = []

            for subset in dziedzina.args:
                for el in subset.args:
                    if(el==sympy.oo) or (el==-(sympy.oo)) or (el==True): continue
                    asymptoty_pionowe.append(el)

            asymptoty_pionowe = set(asymptoty_pionowe)

            # Granice na krańcach dziedziny
            granica1 = sympy.limit(f, x, sympy.oo)
            granica2 = sympy.limit(f, x, -(sympy.oo))

            granice_inf = (granica2, granica1)
            granice_pkt = []
            granice_nieciaglosci = []

            for el in asymptoty_pionowe:
                granica_lewo = sympy.limit(f, x, el, '-')
                granica_prawo = sympy.limit(f, x, el, '+')
                if granica_lewo == granica_prawo: granice_nieciaglosci.append(granica_lewo)

            napiss = "\tNa krańcach dziedziny: "+str(granice_inf)+"\tW punktach nieciągłości: "+str(granice_nieciaglosci)
            self.w.granica.setText(napiss)

            asymptota_pozioma = None
            if(granice_inf[0]==granice_inf[1] and granice_inf[0] not in[sympy.oo,-sympy.oo]): 
                asymptota_pozioma = granice_inf[0]

            asymptota_ukośna = None
            if(asymptota_pozioma is None):
                a = sympy.limit(f/x, x, sympy.oo)
                b = sympy.limit(f-a*x, x, sympy.oo)
                if(a not in [sympy.oo,-sympy.oo] and b not in [sympy.oo,-sympy.oo]):
                    asymptota_ukośna = f"y = {a}*x{b if b<0 else f'+{b}'}"

            pionoweString=""
            for el in asymptoty_pionowe:
                pionoweString += f"x = {el}, "
            
            pion = f"\tPionowe: {pionoweString[:-2] if pionoweString != '' else 'Brak'}"
            poziom = f"\tPoziome: {asymptota_pozioma if asymptota_pozioma is not None else 'Brak'}"
            ukos = f"\tUkośne: {asymptota_ukośna if asymptota_ukośna is not None else 'Brak'}"
            
            asymptotyString = pion+poziom+ukos
            self.w.asymptoty.setText(asymptotyString)

            # Przedziały monotoniczności
            expr = sympy.diff(f, x) # pochodna funkcji

            mono_intervals = sympy.solve(expr) # miejsca zerowe pochodnej

            increasing = [] # przedziały, w których funkcja jest rosnąca
            decreasing = [] # przedziały, w których funkcja jest malejąca

            for i in range(len(mono_intervals)):
                if i == 0:
                    if expr.subs(x, mono_intervals[i]).evalf() > 0:
                        increasing.append((-sympy.oo, mono_intervals[i]))
                    else:
                        decreasing.append((-sympy.oo, mono_intervals[i]))
                elif i == len(mono_intervals) - 1:
                    if expr.subs(x, mono_intervals[i]).evalf() > 0:
                        increasing.append((mono_intervals[i], sympy.oo))
                    else:
                        decreasing.append((mono_intervals[i], sympy.oo))
                else:
                    if expr.subs(x, mono_intervals[i]).evalf() > 0:
                        increasing.append((mono_intervals[i], mono_intervals[i + 1]))
                    else:
                        decreasing.append((mono_intervals[i], mono_intervals[i + 1]))
        
            mono = "Rozwiazania pochodnej: "+str(mono_intervals)+"\n"
            incre = "Rozwiazania rosnace: "+(str(increasing))+"\n"
            decre = "Rozwiazania malejace: "+str(decreasing)
            napisss = mono+incre+decre
            self.w.mon.setText(napisss)
            increaseInterval = (sympy.solve([f>0, x>0], x))
            decreaseInterval = (sympy.solve([f<0, x>0], x))

            incString = ""
            for interval in increaseInterval.args:
                for el in interval.args:
                    if len(el.args)>1:
                        #el = el.evalf()
                        if(str(el) not in incString): incString += "("+str(el)+") ∪ "
                    else:
                        interval = interval.evalf()
                        if(str(interval) not in incString): incString += "("+str(interval)+") ∪ "

            decString= ""
            for interval in decreaseInterval.args:
                for el in interval.args:
                    if len(el.args)>1:
                        el = el.evalf()
                        if(str(el) not in decString): decString += "("+str(el)+") ∪ "
                    else:
                        interval = interval.evalf()
                        if(str(interval) not in decString): decString += "("+str(interval)+") ∪ "

            frosnie = f"\tFunkcja rośnie w przedziale: {incString[:-2]} "
            fmaleje = f"\tFunkcja maleje w przedziale: {decString[:-2]}"
            napissss = frosnie+fmaleje
            self.w.mon.setText(napissss)


            # Ekstrema lokalne
           ekstrema_lokalne = sympy.solveset(sympy.diff(f, x), x, domain=sympy.S.Reals)

            
            if ekstrema_lokalne.args:
                eks1 = ekstrema_lokalne.args[0]
                if type(eks1) is not sympy.ImageSet and len(ekstrema_lokalne.args)>1:
                    eks2 = ekstrema_lokalne.args[1]

                    if f.subs(x, eks1) > f.subs(x, eks2): 
                        maxf = f"\tMaximum funkcji: ({round(eks1, 2)},{round(f.subs(x,eks1),2)})"
                        minf = f"\tMinimum funkcji: ({round(eks2, 2)},{round(f.subs(x,eks2),2)})"
                        xd = maxf+minf
                        self.w.ext.setText(xd)
                    if f.subs(x, eks1) < f.subs(x, eks2): 
                        maxf = f"\tMaximum funkcji: ({round(eks2, 2)},{round(f.subs(x,eks2),2)})"
                        minf = f"\tMinimum funkcji: ({round(eks1, 2)},{round(f.subs(x,eks1),2)})"
                        xd = maxf+minf
                        self.w.ext.setText(xd)
                        
                elif type(eks1) is not sympy.ImageSet and len(ekstrema_lokalne.args)==1:
                    eks = f"\tEkstremum funkcji: ({round(eks1, 2)},{round(f.subs(x,eks1),2)})"
                    self.w.ext.setText(eks)

                elif type(ekstrema_lokalne) is sympy.Union:
                    for idx, el in enumerate(ekstrema_lokalne):
                        val = el.evalf()
                        y = f.subs(x, val)
                        valStr = str(round(float(val),2)).replace("ImageSet(Lambda(_n, ","(").replace("_n","n").replace(", Integers)","")
                        napis_kol = f"({valStr}, {round(float(f.subs(x,val)),2)})"
                        self.w.ext.setText(napis_kol)
                        if(idx==10): break


            # Wyświetlenie wykresu
            self.fig = plt.figure()
            limit = 50
            f = sympy.lambdify(x,f)
            x_vals = np.linspace(-5, 5, 1000)
            y_vals = [f(x) for x in x_vals]

            plt.plot(x_vals, y_vals)
            plt.axhline(y=0, color='black', linewidth=0.5)
            plt.axvline(x=0, color='black', linewidth=0.5)

            # Dodanie punktów oznaczających miejsca zerowe, punkt przecięcia z osią Oy, ekstrema lokalne
            for idx, x in enumerate(miejsca_zerowe):
                plt.scatter(x, 0, color='red', s=10)
                if(idx == limit*2): break

            if ekstrema_lokalne.args:
                for idx, x in enumerate(ekstrema_lokalne):
                    x=float(round(x.evalf(),2))
                    plt.scatter(x, f(x), color='green', s=10)
                    if(idx==limit*2): break

            plt.scatter(0, punkt_przeciecia, color='blue', s=10)


            for el in asymptoty_pionowe:
                plt.axvline(x=el, color='blue', linewidth=0.5, zorder=99)


            if asymptota_pozioma is not None:
                if type(asymptota_pozioma) is sympy.AccumBounds:
                    for el in asymptota_pozioma.args:
                        plt.axhline(y=el, color='blue', linewidth=0.5, zorder=99)
                else:
                    plt.axhline(y=asymptota_pozioma, color='blue', linewidth=0.5, zorder=99)

            x = np.linspace(-limit, limit, 1000)
            y = f(x)
            plt.plot(x, f(x), color='pink', linewidth=1)
            if asymptota_ukośna is not None:
                g = eval(asymptota_ukośna.replace("y = ",""))
                plt.plot(x,g,color='orange', linewidth=0.5)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Wykres funkcji')
            plt.xlim(-limit, limit)
            plt.ylim(-limit, limit)
            plt.show()
         except ZeroDivisionError: 
             print("nie mozna dzielic przez zero")
             return
         except (TypeError, SyntaxError, tokenize.TokenError): 
             print("wprowadzono nieprawidłowy format")
             return
         except Exception:
             print("blad")
             return
     
     def saveCourse(self):
         self.fig.savefig("roman.png", dpi=400)


class CourseResult(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("UIs/CourseResult.ui",self)
        self.dziedzina = self.ui.findChild(QLabel, "label_Dziedzina")
        self.zerowe = self.ui.findChild(QLabel, "label_Zerowe")
        self.oy = self.ui.findChild(QLabel, "label_OY")
        self.granica = self.ui.findChild(QLabel, "label_Granice")
        self.asymptoty = self.ui.findChild(QLabel, "label_Asymptoty")
        self.mon = self.ui.findChild(QLabel, "label_Mon")
        self.ext = self.ui.findChild(QLabel, "label_Ext")
        self.back = self.ui.findChild(QPushButton,"btnBack")
        self.showCourse = self.ui.findChild(QPushButton,"btn_show")
        self.save = self.ui.findChild(QPushButton,"btn_save")
    
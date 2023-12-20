from Functions import *
import tokenize

class Deriative(Functions):
    def __init__(self, label, fprim, fbis, error, ui, fn):
        self.result = ""
        self.display = ""
        self.label = label
        self.fprim = fprim
        self.fbis = fbis
        self.fn = fn
        self.checkf = True
        self.error = error
        self.ui = ui
        self.klocekValidator = QRegExpValidator(QRegExp(r'^-?\d{1,3}$'))
        self.klocek = self.ui.findChild(QLineEdit, "lineEdit")
        self.klocek.setValidator(self.klocekValidator )
        super().__init__()

    def selectX(self):
        self.checkf = True
     

    def selectY(self):
        self.checkf = False
          

    def checkRadio(self):

        if ((self.klocek.text())==""):
            if self.checkf == True and self.result != "":
                self.evaluatex()
            elif self.checkf == False and self.result != "":
                self.evaluatey()
        else: 
            if self.checkf == True and self.result != "":
                self.evaluaten_x()
            elif self.checkf == False and self.result != "":
                self.evaluaten_y()

    def RelaseResult(self, value): 
        return value.replace("**","^").replace("sqrt", "√").replace("pi","π")

    def evaluaten_x(self):
            try:
                klocek_war = self.klocek.text()
                x = {'x': Symbol("x", real = True)}
                my_func = parse_expr(self.result,x)
                f1 = diff(my_func, x["x"], int(klocek_war))
                x = self.RelaseResult(str(f1))
                self.fn.setText(x)
                self.result = ""
            except ZeroDivisionError:
                self.error.setText("Nie mozna dzielic przez 0")
            except SyntaxError:
                self.error.setText("Użyto nieprawidłowego formatu")

            except tokenize.TokenError:
                self.error.setText("Użyto nieprawidłowego formatu")

            except Exception:
                self.error.setText("Nasz kalkulator tego nie obliczy")



    def evaluaten_y(self):
            try:
                klocek_war = self.klocek.text()
                y = {'y': Symbol("y", real = True)}
                my_func = parse_expr(self.result,y)
                f1 = diff(my_func, y["y"], int(klocek_war))
                x = self.RelaseResult(str(f1))
                self.fn.setText(x)
                self.result = ""
            except ZeroDivisionError:
                self.error.setText("Nie mozna dzielic przez 0")
            except SyntaxError:
                self.error.setText("Użyto nieprawidłowego formatu")

            except tokenize.TokenError:
                self.error.setText("Użyto nieprawidłowego formatu")

            except Exception:
                self.error.setText("Nasz kalkulator tego nie obliczy")






    def evaluatex(self):
        try:
            x = {'x': Symbol("x", real = True)}
            my_func = parse_expr(self.result,x)
            f1 = diff(my_func, x["x"])
            f2 = diff(f1,x["x"])
            self.setResult(self.RelaseResult(str(f1)), self.RelaseResult(str(f2)))
            self.result = ""

        except ZeroDivisionError:
            self.error.setText("Nie mozna dzielic przez 0")
        except SyntaxError:
            self.error.setText("Użyto nieprawidłowego formatu")

        except tokenize.TokenError:
            self.error.setText("Użyto nieprawidłowego formatu")

        except Exception:
            self.error.setText("Nasz kalkulator tego nie obliczy")


    def evaluatey(self):
        try:
            y = {'y': Symbol("y", real = True)}
            my_func = parse_expr(self.result,y)
            f1 = diff(my_func, y["y"])
            f2 = diff(f1,y["y"])
            self.setResult(self.RelaseResult(str(f1)), self.RelaseResult(str(f2)))
            self.result = ""

        except ZeroDivisionError:
            self.error.setText("Nie mozna dzielic przez 0")
        except SyntaxError:
            self.error.setText("Użyto nieprawidłowego formatu")

        except tokenize.TokenError:
            self.error.setText("Użyto nieprawidłowego formatu")

        except Exception:
            self.error.setText("Nasz kalkulator tego nie obliczy")

    def setResult(self, f1, f2):
        self.fprim.setText(f1)
        self.fbis.setText(f2)
        self.fprim.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.fbis.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    

    def allClear(self):
        if self.fprim == "":
            return
        self.result = ""
        self.display = ""
        self.fprim.setText("")
        self.fbis.setText("")
        self.fn.setText("")
        self.klocek.setText("")
        self.updateLabel(self.display)
from Functions import *

class Matrix(Functions):
    def __init__(self):
        super().__init__()
        self.matrixValidator = QRegExpValidator(QRegExp('^-?[0-9]+[.]?[0-9]+$'))
        
    def getMatrix(self, grid):
        matrix = []
        for i in range(self.dims):
            submatrix=[]
            for j in range(self.dims):
                cell = grid.itemAtPosition(i,j).widget()
                if(cell.text()==""):
                    self.updateLabel("Wypełnij wszystkie komórki macierzy")
                    return
                value = float(cell.text())
                submatrix.append(value)
            matrix.append(submatrix)
        return matrix

    def createInputMatrix(self, dims, grid):
        self.clearMatrixGrid(grid)
                 
        for row in range(dims):
            for col in range(dims):
                cell = QLineEdit("")
                #cell.setParent(self.matrixContainer)
                cell.adjustSize()
                cell.setValidator(self.matrixValidator)
                cell.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                grid.addWidget(cell, row, col)

    def createOutputMatrix(self, matrix):
        self.clearMatrixGrid(self.gridResult)

        for row in range(self.dims):
            for col in range(self.dims):
                val = str(round(matrix[row][col],2))
                cell = QLabel(val)
                cell.adjustSize()
                cell.setParent(self.ui)
                cell.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.gridResult.addWidget(cell, row, col)

    def changeMatrixDims(self, grid):
        self.dims = int(self.matrixDimsBox.currentText()[-1])
        self.createInputMatrix(self.dims, grid)
        self.matrixCells = self.matrixContainer.findChildren(QLineEdit)

    def clearMatrixGrid(self, grid):
        while(grid.count()):
            item = grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def setValidator(self):
        for cell in self.matrixCells:
            cell.setValidator(self.matrixValidator)

class OneMatrixCalc(Matrix):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.label = self.ui.findChild(QLabel,"label")
        self.matrixContainer = self.ui.findChild(QWidget, "matrix1widget")
        self.gridLayout = self.matrixContainer.findChild(QGridLayout, "gridLayout")
        self.gridResult = self.ui.findChild(QGridLayout, "gridLayout_2")
        self.matrixDimsBox = self.ui.findChild(QComboBox,"comboMatrixDims")
        self.matrixCells = self.ui.findChildren(QLineEdit)
        self.dims = int(self.matrixDimsBox.currentText()[-1])
        
        self.matrixDimsBox.currentTextChanged.connect(lambda: self.changeMatrixDims(self.gridLayout))
        self.setValidator()
          

    def updateLabel(self, value):
        self.label.setText(value)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def calcDet(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)
        result = "det(A) = " + str(round(numpy.linalg.det(matrix), 2))
        self.updateLabel(result)

    def calcNorm(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)
        result = "||A||₁ = " + str(round(numpy.linalg.norm(matrix, 1),2)) + "\n\n"
        result += "||A||₂ = " + str(round(numpy.linalg.norm(matrix, 2),2)) + "\n\n"
        result += "||A||∞ = " + str(round(numpy.linalg.norm(matrix, numpy.inf),2)) + "\n\n"
        result += "||A||f = " + str(round(numpy.linalg.norm(matrix, 'fro'),2)) + "\n\n"
        self.updateLabel(result)

    def calcRank(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)
        result = "rank(A) = " + str(numpy.linalg.matrix_rank(matrix))
        self.updateLabel(result)

    def calcTrace(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)
        result = "tr(A) = " + str(numpy.trace(matrix))
        self.updateLabel(result)

    def calcSum(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)
        result = "sum(A) = " + str(numpy.sum(matrix))
        self.updateLabel(result)

    def calcCondition(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return

        self.clearMatrixGrid(self.gridResult)
        result = "κ₁(A) = " + str(round(numpy.linalg.cond(matrix, 1), 2)) + "\n\n"
        result += "κ₂(A) = " + str(round(numpy.linalg.cond(matrix, 2), 2)) + "\n\n"
        result += "κ∞(A) = " + str(round(numpy.linalg.cond(matrix, numpy.inf), 2)) + "\n\n"
        result += "κf(A) = " + str(round(numpy.linalg.cond(matrix, 'fro'), 2)) + "\n\n"
        self.updateLabel(result)

    def calcInverse(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)

        if numpy.linalg.det(matrix) == 0:
            self.updateLabel("Macierz nie posiada odwrotności")
            return

        self.updateLabel("")
        inverseMatrix = numpy.linalg.inv(matrix)
        self.createOutputMatrix(inverseMatrix)         
        
    def calcComplement(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return
        self.clearMatrixGrid(self.gridResult)

        det = numpy.linalg.det(matrix)
        if det == 0:
            self.updateLabel("Macierz nie posiada dopełnienia")
            return
        inv = numpy.linalg.inv(matrix)
        adjugateMatrix = det*inv

        self.updateLabel("")
        self.createOutputMatrix(adjugateMatrix) 

    def calcTranspose(self):
        matrix = self.getMatrix(self.gridLayout)
        if not matrix: return

        self.updateLabel("")
        matrix = numpy.array(matrix)
        transposedMatrix = matrix.transpose()
        self.createOutputMatrix(transposedMatrix) 

class TwoMatrixCalc(Matrix): 
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.dims = 0
        self.gridFirst = self.ui.findChild(QGridLayout, "matrix1grid")
        self.gridSecond = self.ui.findChild(QGridLayout, "matrix2grid")
        self.gridResult = self.ui.findChild(QGridLayout, "matrix3grid")
        self.label = self.ui.findChild(QLabel, "labelError")
        self.matrixDimsBox = self.ui.findChild(QComboBox,"comboMatrix2")
        self.operands = self.ui.findChild(QComboBox,"comboOperands")

        self.matrixDimsBox.currentTextChanged.connect(self.create2Matrices)
        self.create2Matrices()
        

    def create2Matrices(self):
        self.clearMatrixGrid(self.gridResult)
        self.dims = int(self.matrixDimsBox.currentText()[-1])
        self.createInputMatrix(self.dims, self.gridFirst)
        self.createInputMatrix(self.dims, self.gridSecond)

    def calculate(self):
        self.updateLabel("")
        matrixFirst = self.getMatrix(self.gridFirst)
        matrixSecond= self.getMatrix(self.gridSecond)
        if (not matrixFirst) or (not matrixSecond): return

        matrixFirst = numpy.array(matrixFirst)
        matrixSecond = numpy.array(matrixSecond)
        operand = self.operands.currentText()

        if operand == "+": matrixResult = numpy.add(matrixFirst, matrixSecond)
        if operand == "-": matrixResult = numpy.subtract(matrixFirst, matrixSecond)
        if operand == "*": matrixResult = numpy.dot(matrixFirst, matrixSecond)
        self.createOutputMatrix(matrixResult) 

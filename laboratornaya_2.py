import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PySide6.QtGui import QColor

def possibleMoves(x, y):
    moves = {
        (x - 3, y),
        (x - 2, y - 1), (x - 2, y + 1),
        (x - 1, y - 2), (x - 1, y), (x - 1, y + 2),
        (x, y - 3), (x, y - 1), (x, y + 1), (x, y + 3),
        (x + 1, y - 2), (x + 1, y), (x + 1, y + 2),
        (x + 2, y - 1), (x + 2, y + 1),
        (x + 3, y)
    }
    return moves

def figureDislocation(x, y, matrix):
    matrix[x][y] = "#"
    for i, j in possibleMoves(x, y):
        if 0 <= i < len(matrix) and 0 <= j < len(matrix):
            matrix[i][j] = "*"
    return matrix

def otherFiguresDislocation(matrix, figures):
    for x, y in figures:
        figureDislocation(x, y, matrix)
    return matrix

def boardInitializer(N):
    return [["0" for _ in range(N)] for _ in range(N)]

def boardPrinter(matrix):
    for row in matrix:
        print(" ".join(row))

def recursia(N, L, solutions, currentSolution, figureCount, startRow=0, startCol=0):
    if figureCount == L:
        if tuple(sorted(currentSolution)) not in solutions:
            solutions.add(tuple(sorted(currentSolution)))
            if len(solutions) == 1:
                boardPrinter(otherFiguresDislocation(boardInitializer(N), tuple(sorted(currentSolution))))
        return

    for i in range(startRow, N):
        for j in range(startCol if i == startRow else 0, N):
            if (i, j) not in currentSolution and not possibleMoves(i, j).intersection(currentSolution):
                currentSolution.append((i, j))
                next_start_row = i if j == N - 1 else i
                next_start_col = j + 1 if j < N - 1 else 0
                recursia(N, L, solutions, currentSolution, figureCount + 1, next_start_row, next_start_col)
                currentSolution.pop()

class BigRombWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BigRombWindow")
        self.setGeometry(400, 150, 600, 600)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.placed_figure = set()
        
        self.boardName = QLabel("NxN:")
        self.boardSize = QSpinBox()
        self.boardSize.setMinimum(1)
        self.boardSize.setMaximum(20)
        
        self.labelOldFigures = QLabel("Сколько фигур поставленно:")
        self.oldFigureCount = QLineEdit()
        self.labelCoordinates = QLabel("Координаты фигуры:")
        self.lineCoordinates = QLineEdit()
        self.newFugureButton = QPushButton("Добавить фигуру")
        self.newFugureButton.clicked.connect(self.putFigure)
        self.inputButton = QPushButton("Импортировать данные из файла")
        self.inputButton.clicked.connect(self.dataInput)
        self.figureButton = QPushButton("Показать добавленные фигуры")
        self.figureButton.clicked.connect(self.coords)
        self.figureButton.setEnabled(False)
        
        self.newFigures = QLabel("Фигуры которые необходимо поставить:")
        self.rullerFugures = QSpinBox()
        self.rullerFugures.setMinimum(1)
        self.rullerFugures.setMaximum(399)
        
        self.numOfSolution = QLabel("Колличество решений:")
        self.time = QLabel("Время выполнения:")
        self.totalAnswer = QTableWidget()
        self.totalAnswer.horizontalHeader().setVisible(False)
        self.totalAnswer.verticalHeader().setVisible(False)
        self.totalAnswer.setColumnCount(0)
        self.totalAnswer.setRowCount(0)
        self.totalAnswer.verticalHeader().setDefaultSectionSize(50)
        self.totalAnswer.horizontalHeader().setDefaultSectionSize(50)

        self.readyButton = QPushButton("Готово")
        self.readyButton.clicked.connect(self.answer)
        
        self.clearButton = QPushButton("Очистить")
        self.clearButton.clicked.connect(self.clear)

        self.grid.addWidget(self.boardName, 0, 0)
        self.grid.addWidget(self.boardSize, 0, 1)
        self.grid.addWidget(self.labelOldFigures, 1, 0)
        self.grid.addWidget(self.oldFigureCount, 1, 1)
        self.grid.addWidget(self.labelCoordinates, 2, 0)
        self.grid.addWidget(self.lineCoordinates, 2, 1)
        self.grid.addWidget(self.inputButton, 2, 2)
        self.grid.addWidget(self.newFugureButton, 3, 0)
        self.grid.addWidget(self.figureButton, 3, 1)
        self.grid.addWidget(self.newFigures, 4, 0)
        self.grid.addWidget(self.rullerFugures, 4, 1)
        self.grid.addWidget(self.numOfSolution, 5, 0)
        self.grid.addWidget(self.time, 6, 0)
        self.grid.addWidget(self.totalAnswer, 7, 0)
        self.grid.addWidget(self.readyButton, 8, 0)
        self.grid.addWidget(self.clearButton, 9, 0)

    def putFigure(self):
        try:
            k = int(self.oldFigureCount.text())
            self.oldFigureCount.setReadOnly(True)
            x, y = map(int, self.lineCoordinates.text().split(","))
            self.placed_figure.add((x, y))
            if len(self.placed_figure) > 0:
                self.figureButton.setEnabled(True)
            if len(self.placed_figure) == k:
                self.oldFigureCount.setReadOnly(True)
                self.lineCoordinates.clear()
                self.lineCoordinates.setReadOnly(True)
        except ValueError:
            QMessageBox.warning(self, "Error", "Данные введены неверно")
            return
        self.lineCoordinates.clear()

    def dataInput(self):
        try:
            with open("input.txt", "r") as file:
                A, B, C = map(int, file.readline().split())
                self.boardSize.setValue(A)
                self.rullerFugures.setValue(B)
                self.oldFigureCount.setText(str(C))
                for i in file.readlines():
                    x, y = map(int, i.split())
                    self.placed_figure.add((x, y))
                if len(self.placed_figure) > 0:
                    self.figureButton.setEnabled(True)
                if len(self.placed_figure) == C:
                    self.lineCoordinates.clear()
                    self.oldFigureCount.setReadOnly(True)
                    self.lineCoordinates.setReadOnly(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def answer(self):
        try:
            A = self.boardSize.value()
            B = self.rullerFugures.value()
            placed_figure = self.placed_figure

            start_time = time.time()
            solutions = set()
            first_solution = boardInitializer(A)
            recursia(A, B, solutions, list(placed_figure), len(placed_figure))
            end_time = time.time()
            elapsed_time = end_time - start_time

            if solutions:
                self.numOfSolution.setText(f"Колличество решений: {len(solutions)}")
                self.time.setText(f"Время выполнения:\n{elapsed_time:.2f} сек")
                first_solution = otherFiguresDislocation(first_solution, list(solutions)[0])
                self.totalAnswer.setColumnCount(A)
                self.totalAnswer.setRowCount(A)
                for i in range(A):
                    for j in range(A):
                        item = QTableWidgetItem()
                        if first_solution[i][j] == "#":
                            item.setBackground(QColor("blue"))
                        elif first_solution[i][j] == "*":
                            item.setBackground(QColor("green"))
                        self.totalAnswer.setItem(i, j, item)
            else:
                QMessageBox.information(self, "Ответ", "Нет решений")
                with open("output.txt", "w") as file:
                    file.write("No solution")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear(self):
        self.placedFigure = set()
        self.oldFigureCount.setReadOnly(False)
        self.oldFigureCount.clear()
        self.lineCoordinates.setReadOnly(False)
        self.numOfSolution.setText("Колличество решений:")
        self.time.setText("Время выполнения:")
        self.totalAnswer.clear()

    def coords(self):
        QMessageBox.information(self, "Координаты", str(self.placedFigure))

if __name__ == "__main__":
    app = QApplication([])
    window = BigRombWindow()
    window.show()
    sys.exit(app.exec())
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class button(QPushButton):
    def __init__(self):
        super(button, self).__init__()
        self.txt = ""
        self.check = 0
        self.winLine = False
        self.vert_hor = False
        self.diag = None
        self.setAttribute(Qt.WA_StyledBackground)

        self.erase = False

    def paintEvent(self, event: QPaintEvent):
        c = QPoint(event.rect().center())
        paint = QPainter(self)
        paint.setRenderHint(QPainter.Antialiasing)
        if self.txt == "circle":
            pen = QPen(Qt.red, 5)
            paint.setPen(pen)

            w = event.rect().width()/2-pen.width()*2
            paint.drawEllipse(c, w, w)
        elif self.txt == "cross":
            pen = QPen(Qt.white, 5)
            paint.setPen(pen)
            r_end = QPoint(event.rect().width()-pen.width()*2, event.rect().height()-pen.width()*2)
            l_end = QPoint(0+pen.width()*2, event.rect().height()-pen.width()*2)
            paint.drawLine(QPoint(0+pen.width()*2,0+pen.width()*2), r_end)
            paint.drawLine(QPoint(event.rect().width()-pen.width()*2,0+pen.width()*2), l_end)
        
        if self.winLine:
            paint.setPen(QPen(Qt.green, 5))
            if self.diag == None:
                if not self.vert_hor:
                    paint.drawLine(QPoint(event.rect().center().x(), 0), QPoint(event.rect().center().x(), event.rect().height()), )
                else:
                    paint.drawLine(QPoint(0, event.rect().center().y()), QPoint(event.rect().width(), event.rect().center().y()))
            elif self.diag == 0:
                paint.drawLine(QPoint(0, 0), QPoint(event.rect().width(), event.rect().height()))
            else:
                paint.drawLine(QPoint(event.rect().width(), 0), QPoint(0, event.rect().height()))

        if self.erase:
            paint.fillRect(event.rect(), QColor(40,40,40))
    
    def d_circle(self):
        self.txt = "circle"
        self.check = 1
        self.update()
    def d_cross(self):
        self.txt = "cross"
        self.check = 2
        self.update()

class ticTacToe(QWidget):
    def __init__(self):
        super(ticTacToe, self).__init__()
        self.counter = True
        self.winLine = False
        self.winLine_start = QPoint()
        self.winLine_end = QPoint()
        self.erase = False
        
        # set window size and bg color
        self.setFixedSize(600, 600)
        self.setStyleSheet(u"background-color: rgb(35, 35, 35);")

        # make basic layout out of buttons
        self.ly = QGridLayout(self)
        self.makeDefLayout()
    

    def makeDefLayout(self):
        for i in range(3):
            for j in range(3):
                btn = button()
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setStyleSheet(u"background-color: rgb(40, 40, 40); border: 0px;")

                btn.clicked.connect(self.clickCell)

                self.ly.addWidget(btn, i, j, alignment=Qt.Alignment(0))

    def clickCell(self, event):
        if not self.winLine:
            sender: button = self.sender()
            sender.setStyleSheet(u"background-color: rgb(40,40,40); color: rgb(230, 230, 230); border: 0px;")

            if sender.check == 0:
                if self.counter:
                    sender.d_circle()
                    self.counter = False
                else:
                    sender.d_cross()
                    self.counter = True

            self.update()
            self.checkResult()
        
    def paintEvent(self, event: QPaintEvent):
        paint = QPainter(self)
        paint.setPen(QPen(Qt.green,5))
        if self.winLine:
            paint.drawLine(self.winLine_start, self.winLine_end)
        if self.erase:
            paint.fillRect(event.rect(), QColor(35,35,35))

    def winCoords(self, list: button, vh: bool, diag):
        self.winLine_start = list[0].mapToParent(list[0].rect().center())
        self.winLine_end = list[-1].mapToParent(list[-1].rect().center())

        self.winLine = True
        for l in list:
            l.winLine = self.winLine
            l.vert_hor = vh
            l.diag = diag
        self.update()

        rep = QMessageBox()
        rep.setText("Want to play again?")
        rep.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        res = rep.exec()

        if res == QMessageBox.Ok:
            self.playAgain()
        else:
            return

    def checkResult(self):
        # check horizontal
        for i in range(self.ly.rowCount()):
            circs = 0
            crosses = 0
            circ_cells = list()
            cross_cells = list()
            for j in range(self.ly.columnCount()):
                item: button = self.ly.itemAtPosition(i,j).widget()
                cellData = item.check
                if cellData == 1:
                    circ_cells.append(item)
                    circs += 1
                elif cellData == 2:
                    cross_cells.append(item)
                    crosses += 1

                if circs == 3:
                    print("Circles win!")
                    self.winCoords(circ_cells, True, None)
                    return
                elif crosses == 3:
                    print("Crosses win!")
                    self.winCoords(cross_cells, True, None)
                    return
        
        # check vertical
        for i in range(self.ly.columnCount()):
            circs = 0
            crosses = 0
            circ_cells = list()
            cross_cells = list()
            for j in range(self.ly.rowCount()):
                item: button = self.ly.itemAtPosition(j,i).widget()
                cellData = item.check
                if cellData == 1:
                    circ_cells.append(item)
                    circs += 1
                elif cellData == 2:
                    cross_cells.append(item)
                    crosses += 1
                
                if circs == 3:
                    print("Circles win!")
                    self.winCoords(circ_cells, False, None)
                    return
                elif crosses == 3:
                    print("Crosses win!")
                    self.winCoords(cross_cells, False, None)
                    return
        
        # check diagonal
        l_diag = [(0,0), (1,1), (2,2)]
        r_diag = [(0,2), (1,1), (2,0)]
        diag_check = [l_diag, r_diag]
        for i, dc in enumerate(diag_check):
            circs = 0
            crosses = 0
            circ_cells = list()
            cross_cells = list()
            for d in dc:
                item = self.ly.itemAtPosition(d[0], d[1]).widget()
                cellData: button = item.check
                if cellData == 1:
                    circ_cells.append(item)
                    circs += 1
                elif cellData == 2:
                    cross_cells.append(item)
                    crosses += 1

                if circs == 3:
                    print("Circles win!")
                    self.winCoords(circ_cells, False, i)
                elif crosses == 3:
                    print("Crosses win!")
                    self.winCoords(cross_cells, False, i)

    def playAgain(self):
        self.erase = True
        for i in range(self.ly.rowCount()):
            for j in range(self.ly.columnCount()):
                item: button = self.ly.itemAtPosition(i,j).widget()
                item.erase = True
                item.txt = ""
                item.check = 0
                item.winLine = False
                item.diag = None
                item.vert_hor = False
        self.counter = True
        self.winLine = False
        self.winLine_start = QPoint()
        self.winLine_end = QPoint()
        
        self.erase = False
        for i in range(self.ly.rowCount()):
            for j in range(self.ly.columnCount()):
                item: button = self.ly.itemAtPosition(i,j).widget()
                item.erase = False
        self.update()

if __name__ == '__main__':
    app = QApplication([])
    w = ticTacToe()
    w.show()
    app.exec()
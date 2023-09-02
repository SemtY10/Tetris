import sys
import random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.tboard = Board(self)
        self.statusbar = self.statusBar()
        self.tboard.start()
        self.resize(400,800)
        self.center()
        self.setWindowTitle("Tetris")
        self.show()
        
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())//2,(screen.height() - size.height())//2) 
        
class Board(QFrame):
    board_width = 10
    board_height = 22
    speed = 300
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
    
    def initBoard(self):
        self.timer = QBasicTimer()
        
        self.cur_x = 0
        self.cur_y = 0
        self.num_lines_removed = 0
        self.board = [] 
        
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()
        self.is_waiting_after_line = False
        
    def start(self):
        if self.isPaused:
            return
        
        self.isStarted = True
        self.is_waiting_after_line = False
        self.num_lines_removed = 0
        self.clearBoard()
        
        self.timer.start(Board.speed, self)
        
    def clearBoard(self):
        for i in range(Board.board_height * Board.board_width):
            self.board.append(Tetrominoe.no_shape)
            
class Tetrominoe(object):
    no_shape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SqureShape = 5
    LShape = 6
    MLShape = 7
    
class Shape (object):
    coords_table =(
        ((0,0),(0,0),(0,0),(0,0),),
        ((0,-1), (0,0), (-1,0), (-1,1)),
        ((0,1),(0,0),(1,0),(1,1)),
        ((0,-1),(0,0),(0,1),(0,2)),
        ((-1,0),(0,0),(1,0),(0,1)),
        ((0,0),(1,0),(0,1),(1,1)),
        ((-1,-1),(0,-1),(0,0),(0,1)),
        ((1,-1),(0,-1),(0,0),(0,1))
    )  
    
    def __init__(self):
        self.coords = [[0,0]for i in range(4)] #? == [[0,0],[0,0],[0,0],[0,0]]
        self.piece_shape = Tetrominoe.no_shape
        self.set_shape(Tetrominoe.no_shape)
        
    def shape(self):
        return self.piece_shape    
    
    def set_shape(self, shape):
        table = Shape.coords_table[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]
        self.piece_shape = shape        
                
    def set_randome_shape(self):
        self.set_shape(random.randint(1,7))
    
    def x(self, index):
        return self.coords [index][0]
    
    def y(self, index):
        return self.coords [index][1]
        
    def setX(self, index, x):
        self.coords[index][0] = x
        
    def setY(self, index, y):
        self.coords[index][1] = y
              
              
    def rotate_left(self):
        if self.piece_shape == Tetrominoe.SqureShape:
            return self
        
        result = Shape
        result.piece_shape = self.piece_shape       
        
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))
            
        return result      
    
    def rotate_right(self):
        if self.piece_shape == Tetrominoe.SqureShape:
            return self
        
        result = Shape
        result.piece_shape = self.piece_shape       
        
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))
            
        return result      
    
    
if __name__ == "__main__":
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
          
        
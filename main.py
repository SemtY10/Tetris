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
    
if __name__ == "__main__":
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
          
        
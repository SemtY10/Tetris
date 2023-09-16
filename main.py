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
        
        self.setFocusPolicy(Qt.StrongFocus)
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
        
        self.msg2Statusbar.emit(str(self.num_lines_removed))
        
        self.new_piece
        
        self.timer.start(Board.speed, self)
    
    def pause(self):
        if not self.isStarted:
            return
        
        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
            self.mg2Statusbar.emit(str("pauset"))
        else:
            self.timer.start(Board.speed,self)
            self.msg2Statusbar.emit(str(self.num_lines_removed))
            
        self.update()
        
    def clearBoard(self):
        for i in range(Board.board_height * Board.board_width):
            self.board.append(Tetrominoe.no_shape)
    
    def shape_at(self, x, y):
        return self.board[(y*Board.board_width)+x]
    
    def set_shape_at(self, x, y, shape):
         self.board[(y*Board.board_width)+x] = shape
         
    def square_height(self):
        return self.contentsRect().height() // Board.board_height
    
    def square_width(self):
        return self.contentsRect().height() // Board.board_width    
    
    def paint_event(self,event):
        painter = QPainter(self)
        rect = self.contentsRect()
        
        board_top = rect.bottom() - Board.board_height * self.square_height()
        
        for i in range(Board.board_height):
            for j in range (Board.board_width):
                shape = self.shape_at(j, Board.board_height - i - 1)    

                if shape!= Tetrominoe.no_shape:
                    self.draw_square(painter, rect.left() +j*self.square_width(), board_top +i*self.square_height(), shape)
                    
        if self.cur_piece.shape() != Tetrominoe.no_shape:
            for  i in range(4):
                x = self.cur_x + self.cur_piece.x(i)
                y = self.cur_y - self.cur_piece.y(i)
                self.draw_square(painter,rect.left() +x * self.square_width(), board_top + (Board.board_height - y - 1) * self.square_height(),self.cur_piece.shape())
    
    def try_move(self, new_piece, new_x, new_y):
        for i in range(4):
            x = new_x + new_piece.x(i)
            y = new_y + new_piece.y(i)
            if x< 0 or x>= Board.board_width or  y<0 or y>= Board.board_height:
                return False
            
            if self.shape_at(x, y) != Tetrominoe.no_shape:
                return False
            
        self.cur_piece = new_piece
        self.cur_x = new_x
        self.cur_y = new_y
        self.update()
        
    def draw_squere(self, painter, x, y, shape):
        color_table = [0x000000, 0xCC66666,0x66CC66,0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
        
        color = QColor(color_table[shape])
        painter.fillRect(x+1, y+1, self.square_width() - 2, self.square_height() - 2, color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x+self.square_width() - 1, y)
        
        painter.setPen(color.darker())
        painter.drawLine(x+1, y + self.square_height() - 1, x + self.square_width() - 1, y + self.square_height() - 1)
        painter.drawLine(self.square_width() - 1, y + self.square_height() - 1, x+self.square_width() - 1, y + 1)
    
    
    def key_pressed(self, event):
        if not self.isStarted or self.cur_piece.shape() == Tetrominoe.no_shape:
            super(Board, self).key_pressed(event)
            return
        
        key = event.key()
        if key ==Qt.Key_P:
            self.pause()
            
        if self.isPaused:
            return 
        
        elif key == Qt.Key_Left:
            self.try_move(self.cur_piece, self.cur_x-1, self.cur_y)
            
        elif key == Qt.Key_Right:
            self.try_move(self.cur_piece, self.cur_x+1, self.cur_y)  
        
        elif key == Qt.Key_Down:
            self.drop_down()       
            
        elif key == Qt.Key_Up:
            self.try_move(self.cur_piece.rotate_left(), self.cur_x, self.cur_y)  
            
        elif key == Qt.Key_Space:
            self.try_move(self.cur_piece.rotate_right(), self.cur_x, self.cur_y)
            
        elif key == Qt.Key_D:
            self.one_line_down()
            
        else:
            super(Board, self).keyPressEvent(event)
            
    def drop_down(self):
        new_y = self.cur_y
        while new_y > 0:
            if not self.try_move(self.cur_piece, self.cur_x, self.cur_y-1):
                break
            
            new_y -= 1
            
        self.piece_dropped()
        
    def piece_dropped(self):
        for i in range(4):
            x = self.cur_x + self.cur_piece.x(i)
            y = self.cur_y + self.cur_piece.y(i)
            self.set_shape_at(x, y, self.cur_piece.shape())
            
        self.remove_full_line()
        
        if not self.is_waiting_after_line:
            self.new_piece
            
    def one_line_down(self):
        if not self.try_move(self.cur_piece, self.cur_x, self.cur_y-1):
            self.piece_dropped
    
    def new_piece (self):
        self.cur_piece = Shape()
        self.cur_piece.set_randome_shape()
        self.cur_x = Board.board_width // 2 +1
        self.cur_y = Board.board_height - 1  + self.cur_piece.min_y()
        
        if not self.try_move(self.cur_piece, self.cur_x, self.cur_y):
            self.cur_piece.set_shape(Tetrominoe.no_shape)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Game over")
        
    msg2Statusbar = pyqtSignal(str)
    
        
                              
            
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
    
    def min_x(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])          
        return m
    def max_x(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0]) 
        return m
    def min_y(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1]) 
        return m
    def max_y(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1]) 
        return m      
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
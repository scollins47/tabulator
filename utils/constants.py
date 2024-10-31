from io import StringIO
MEASURE_LENGTH=4
NUM_STRINGS = 6

class Cursor:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
        self.buffer = []
        self.is_flushing = False
    
    def move_right(self) -> int:
        self.x += 1
        return self.x
    
    def to_write(self, c):
        self.buffer.append(c)
    
    def flush(self) -> str:
        self.is_flushing = True
        return self.buffer

    def move_left(self) -> int:
        if self.x > 1:
            self.x -=1
        else: self.x = 1
        return self.x

    def move_down(self) -> int:
        if self.y <= 5:
            self.y += 1
        return self.y
    
    def move_up(self) -> int:
        #buffer
        if self.y > 0:
            self.y -= 1
        return self.y
    
    def print_x(self) -> str:
        line = StringIO()
        line.write(" ")
        # line.write(" ") # buffer
        for i in range(self.x):
            line.write(" ")
        line.write("v")
        print(line.getvalue())

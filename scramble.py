import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from enum import Enum
import random
from functools import reduce
import numpy


class Color(Enum):
    White = 0,
    Yellow = 1,
    Green = 2,
    Blue = 3,
    Orange = 4,
    Red = 5

def color_img(color):
    if color == Color.White:
        file = "colors/white.png"
    elif color == Color.Yellow:
        file = "colors/yellow.png"
    elif color == Color.Green:
        file = "colors/green.png"
    elif color == Color.Blue:
        file = "colors/blue.png"
    elif color == Color.Red:
        file = "colors/red.png"
    elif color == Color.Orange:
        file = "colors/orange.png"

    return Gtk.Image.new_from_file(file)

class Turn(Enum):
    CLOCKWISE = 0,
    ANTICLOCKWISE = 1,
    DOUBLE = 2

class Move:
    turn_dict = {Turn.CLOCKWISE : "", Turn.ANTICLOCKWISE : "'", Turn.DOUBLE : "2"}

    def __init__(self,face, turn, layers):
        self.face = face
        self.turn = turn
        self.layers = layers

    def __str__(self):
        result = self.face
        if (self.layers == 2):
            result += "w"
        elif (self.layers > 2):
            result = str(self.layers) + result + "w"

        result += Move.turn_dict[self.turn]

        return result


class Scramble:
    def __init__(self, label =  None):
        self.scramble = []
        self.label = label if label else Gtk.Label()
        self.label.props.wrap = True
        self.visible = True
        self.reset()
        

    def generate(self):
        pass

    def __str__(self):
        return reduce(lambda acc, m: acc+m+" ", list(map(str,self.scramble)), "")

    def show(self):
        self.label.set_markup("<span font_desc='Ubuntu 25'>{}</span>".format(str(self)))
        self.visible = True

    def hide(self):
        self.label.set_text("")
        self.visible = False

    def switch_visible(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def reset(self):
        self.generate()
        self.show()

class ScrambleNxN(Scramble):
    FACES = ["U","D","F","B","L","R"]

    def __init__(self, cube_size, label = None):
        super().__init__(label)
        self.cube = Cube(cube_size)
        self.draw = Gtk.Table(rows = 3, columns = 4, homogeneous = True)

    def generate(self, length, max_layers, faces = None):
        last_face = ""
        self.scramble = []
        if not faces:
            faces = ScrambleNxN.FACES.copy()
        for _ in range(length):
            face = random.choice(faces)
            while face == last_face:
                face = random.choice(faces)
            turn = random.choice(list(Turn))
            layers = random.randint(1,max_layers)
            self.scramble.append(Move(face, turn, layers))
            last_face = face

        self.cube.draw_cube()
        self.draw.show_all()

    def scramble_cube(self):
        for move in self.scramble:
            self.cube.do_move(move)

    def face_table(self, face):
        size = self.cube.size

class Scramble2x2(ScrambleNxN):
    FACES = ["U", "R", "F"]

    def __init__(self, label = None):
        self.cube = Cube(2)
        self.draw = Gtk.Table(rows = 3, columns = 4, homogeneous = True)
        super().__init__(2,label)

    def generate(self):
        super().generate(10, 1, Scramble2x2.FACES)

    def scramble_cube(self):
        for move in self.scramble:
            self.cube.do_move(move)                

class Scramble3x3(ScrambleNxN):
    def __init__(self, label=None):
        self.cube = Cube(3)
        self.draw = Gtk.Table(rows = 3, columns = 4, homogeneous = True)
        super().__init__(3,label)
        self.cube.draw_cube()
        

    def generate(self):
        super().generate(20, 1)
        self.cube.draw_cube()


class Scramble4x4(ScrambleNxN):
    def __init__(self, label = None):
        self.cube = Cube(4)
        self.draw = Gtk.Table(rows = 3, columns = 4, homogeneous = True)
        super().__init__(4,label)
        #self.draw_scramble()
        self.cube.draw_cube()

    def generate(self):
        super().generate(40, 2)
        self.cube.draw_cube()


class Cube:    
    def __init__(self, size):
        self.size = size
        self.reset()
        self.draw = Gtk.Table(rows = 3, columns = 4, homogeneous = True)
        for i in range(4):
            self.draw.set_col_spacing(i,0)
        for i in range(3):
            self.draw.set_row_spacing(i,0)

    def face_table(self, face):
        result = Gtk.Table(rows = self.size, columns = self.size, homogeneous = False)
        
        for i in range(self.size):
            for j in range(self.size):
                result.attach(color_img(face[i][j]), j, j+1, i, i+1)

        return result

    def draw_cube(self):
        #self.draw = Gtk.Table(rows = 3, columns = 4, homogeneous = False)
        self.draw.attach(self.face_table(self.U),1,2,0,1)
        self.draw.attach(self.face_table(self.L),0,1,1,2)
        self.draw.attach(self.face_table(self.F),1,2,1,2)
        self.draw.attach(self.face_table(self.R),2,3,1,2)
        self.draw.attach(self.face_table(self.B),3,4,1,2)
        self.draw.attach(self.face_table(self.D),1,2,2,3)
        self.draw.show_all()

    def reset(self):
        self.U = self.init_face(Color.White)
        self.D = self.init_face(Color.Yellow)
        self.F = self.init_face(Color.Green)
        self.B = self.init_face(Color.Blue)
        self.L = self.init_face(Color.Orange)
        self.R = self.init_face(Color.Red)

    def init_face(self, color):
        return numpy.full((self.size, self.size), color)

    def do_move(self,move):
        if move.face == "F":
            if move.turn == Turn.CLOCKWISE:
                self.F_clockwise(move.layers)
            elif move.turn == Turn.ANTICLOCKWISE:
                self.F_anticlockwise(move.layers)
            else:
                self.F_double(move.layers)
        elif move.face == "B":
            if move.turn == Turn.CLOCKWISE:
                self.B_clockwise(move.layers)
            elif move.turn == Turn.ANTICLOCKWISE:
                self.B_anticlockwise(move.layers)
            else:
                self.B_double(move.layers)
        elif move.face == "U":
            if move.turn == Turn.CLOCKWISE:
                self.U_clockwise(move.layers)
            elif move.turn == Turn.ANTICLOCKWISE:
                self.U_anticlockwise(move.layers)
            else:
                self.U_double(move.layers)
        elif move.face == "D":
            if move.turn == Turn.CLOCKWISE:
                self.D_clockwise(move.layers)
            elif move.turn == Turn.ANTICLOCKWISE:  
                self.D_anticlockwise(move.layers)
            else:
                self.D_double(move.layers)
        elif move.face == "L":
            if move.turn == Turn.CLOCKWISE:
                self.L_clockwise(move.layers)
            elif move.turn == Turn.ANTICLOCKWISE:
                self.L_anticlockwise(move.layers)
            else:
                self.L_double(move.layers)
        elif move.face == "R":
            if move.turn == Turn.CLOCKWISE:
                self.R_clockwise(move.layers)
            elif move.turn == Turn.ANTICLOCKWISE:
                self.R_anticlockwise(move.layers)
            else:
                self.R_double(move.layers)


    def F_anticlockwise(self, layers):
        self.F = numpy.rot90(self.F)
        first = self.size-layers
        left = self.L[:,first:].copy()
        self.L[:,first:] = numpy.rot90(self.U[first:])
        self.U[first:] = numpy.rot90(self.R[:,:layers])
        self.R[:,:layers] = numpy.rot90(self.D[:layers])
        self.D[:layers] = numpy.rot90(left.copy())

    def U_anticlockwise(self, layers):
        self.rotate_x_anticlockwise()
        self.F_anticlockwise(layers)
        self.rotate_x_clockwise()

    def D_anticlockwise(self, layers):
        self.rotate_x_clockwise()
        self.F_anticlockwise(layers)
        self.rotate_x_anticlockwise()

    def L_anticlockwise(self, layers):
        self.rotate_y_anticlockwise()
        self.F_anticlockwise(layers)
        self.rotate_y_clockwise()

    def R_anticlockwise(self, layers):
        self.rotate_y_clockwise()
        self.F_anticlockwise(layers)
        self.rotate_y_anticlockwise()

    def B_anticlockwise(self, layers):
        self.rotate_y_double()
        self.F_anticlockwise(layers)
        self.rotate_y_double()

    def F_double(self, layers):
        for _ in range(2):
            self.F_anticlockwise(layers)

    def U_double(self, layers):
        for _ in range(2):
            self.U_anticlockwise(layers)

    def D_double(self, layers):
        for _ in range(2):
            self.D_anticlockwise(layers)

    def B_double(self, layers):
        for _ in range(2):
            self.B_anticlockwise(layers)

    def L_double(self, layers):
        for _ in range(2):
            self.L_anticlockwise(layers)

    def R_double(self, layers):
        for _ in range(2):
            self.R_anticlockwise(layers)

    def F_clockwise(self, layers):
        for _ in range(3):
            self.F_anticlockwise(layers)

    def U_clockwise(self, layers):
        for _ in range(3):
            self.U_anticlockwise(layers)

    def D_clockwise(self, layers):
        for _ in range(3):
            self.D_anticlockwise(layers)

    def B_clockwise(self, layers):
        for _ in range(3):
            self.B_anticlockwise(layers)

    def L_clockwise(self, layers):
        for _ in range(3):
            self.L_anticlockwise(layers)

    def R_clockwise(self, layers):
        for _ in range(3):
            self.R_anticlockwise(layers)

    def rotate_x_clockwise(self):
        self.L = numpy.rot90(self.L)
        self.R = numpy.rot90(self.R, 3)
        U_temp = self.U.copy()
        self.U = self.F.copy()
        self.F = self.D.copy()
        self.D = numpy.rot90(self.B.copy(), 2)
        self.B = numpy.rot90(U_temp.copy(), 2)

    def rotate_y_clockwise(self):
        self.U = numpy.rot90(self.U, 3)
        self.D = numpy.rot90(self.D)
        self.F, self.R, self.B, self.L = \
            self.R.copy(), self.B.copy(), self.L.copy(), self.F.copy()
        
    def rotate_z_clockwise(self):
        self.F = numpy.rot90(self.F, 3)
        self.B = numpy.rot90(self.B)
        U_temp = self.U.copy()
        self.U = numpy.rot90(self.L.copy(), 3)
        self.L = numpy.rot90(self.D.copy(), 3)
        self.D = numpy.rot90(self.R.copy(), 3)
        self.D = numpy.rot90(U_temp.copy(), 3)

    def rotate_x_anticlockwise(self):
        for _ in range(3):
            self.rotate_x_clockwise()

    def rotate_y_anticlockwise(self):
        for _ in range(3):
            self.rotate_y_clockwise()

    def rotate_z_anticlockwise(self):
        for _ in range(3):
            self.rotate_z_clockwise()

    def rotate_x_double(self):
        for _ in range(2):
            self.rotate_x_clockwise()

    def rotate_y_double(self):
        for _ in range(2):
            self.rotate_y_clockwise()

    def rotate_z_double(self):
        for _ in range(2):
            self.rotate_z_clockwise()

import threading
import random
from Tkinter import *
from ZomFrame import ZomFrame
import settings

CITY_SIZE = settings.CITY_SIZE
SCALE = 40
WIDTH = CITY_SIZE * SCALE
HEIGHT = CITY_SIZE * SCALE

zom_path = "./zom/eric_Zombie.zom"
hum_path = "./zom/extra_human.zom"


class ZomApp(Frame):
    def __init__(self):
        Frame.__init__(self)
        # Set up the main window frame as a grid
        self.master.title("Zombie Apocalypse Simulator")
        self.m_pause = False
        self.grid()
        self.triangles = []

        # Set up main frame for game as a grid
        frame1 = Frame(self)
        frame1.grid()

        # Add a canvas to frame1 as self.canvas member
        self.canvas = Canvas(frame1, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.grid(rowspan = 4)
        self.canvas.focus_set()
        # bind mouse click
        self.canvas.bind("<ButtonPress-1>", self.mouse_click)

        # Create buttons
        newGame = Button(frame1, text="New Game", command=self.new_game)
        newGame.grid(row=0, column=1, sticky=E)
        pause = Button(frame1, text="Pause", command=self.pause)
        pause.grid(row=0, column=2, sticky=E)

        # Create a label to show user his/her score
        self.month_label = Label(frame1)
        self.month_label.grid(row=1, column=1)
        self.zombie_label = Label(frame1)
        self.zombie_label.grid(row=2, column=1)
        self.human_label = Label(frame1)
        self.human_label.grid(row=2, column=2)
        # mem label
        self.mem0_label = Label(frame1)
        self.mem0_label.grid(row=3, column=1)
        self.mem1_label = Label(frame1)
        self.mem1_label.grid(row=3, column=2)

        self.ops_label = Label(frame1)
        self.ops_label.grid(row=0, column=3)

        # create city
        self.zomframe = ZomFrame()
        self.new_game()

    def pause(self):
        self.m_pause = not self.m_pause
        if not self.m_pause:
            self.move()

    def new_game(self):
        # FIXME: Fatal Error !!
        self.m_pause = False
        self.canvas.delete(ALL)
        self.draw_grids()
        self.triangles = []
        self.zomframe.new_game(zom_path, hum_path)
        self.move()

    def _move(self):
        while not self.m_pause:
            for triangle in self.triangles:
                self.canvas.delete(triangle)
            self.triangles = []
            #self.draw_grids()
            self.print_city()
            self.update_label()
            #self.canvas.update()
            self.canvas.after(88)
            self.zomframe.take_turn()

    def move(self):
        t = threading.Thread(target=self._move)
        #t.daemon = True
        t.start()

    def draw_grids(self):
        # draw grids
        for i in range(CITY_SIZE):
            self.canvas.create_line(i * SCALE, 0, i * SCALE, HEIGHT)
            self.canvas.create_line(0, i * SCALE, WIDTH, i * SCALE)

    def print_city(self):
        for zombie in self.zomframe.racoonCity.zombies:
            x = zombie.m_X
            y = zombie.m_Y
            facing = zombie.m_Facing
            self.draw_triangle(x, y, facing, "red")
        for human in self.zomframe.racoonCity.humans:
            x = human.m_X
            y = human.m_Y
            facing = human.m_Facing
            self.draw_triangle(x, y, facing, "green")

    def draw_triangle(self, x, y, facing, color):
        x = (x + 0.5) * SCALE
        y = (y + 0.5) * SCALE
        if facing == "Up":
            x1 = x
            y1 = y - SCALE * (4.0 / 9)
            x2 = x - SCALE * (1.0 / 3)
            y2 = y + SCALE * (2.0 / 9)
            x3 = x + SCALE * (1.0 / 3)
            y3 = y + SCALE * (2.0 / 9)
        elif facing == "Left":
            x1 = x - SCALE * (4.0 / 9)
            y1 = y
            x2 = x + SCALE * (2.0 / 9)
            y2 = y + SCALE * (1.0 / 3)
            x3 = x + SCALE * (2.0 / 9)
            y3 = y - SCALE * (1.0 / 3)
        elif facing == "Down":
            x1 = x
            y1 = y + SCALE * (4.0 / 9)
            x2 = x - SCALE * (1.0 / 3)
            y2 = y - SCALE * (2.0 / 9)
            x3 = x + SCALE * (1.0 / 3)
            y3 = y - SCALE * (2.0 / 9)
        elif facing == "Right":
            x1 = x + SCALE * (4.0 / 9)
            y1 = y
            x2 = x - SCALE * (2.0 / 9)
            y2 = y + SCALE * (1.0 / 3)
            x3 = x - SCALE * (2.0 / 9)
            y3 = y - SCALE * (1.0 / 3)
        else:
            return
        self.triangles.append(self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black"))

    def update_label(self):
        self.month_label['text'] = "month: " + str(self.zomframe.racoonCity.month)
        self.zombie_label['text'] = "zombies: " + str(len(self.zomframe.racoonCity.zombies))
        self.human_label['text'] = "humans: " + str(len(self.zomframe.racoonCity.humans))

    def mouse_click(self, event):
        x = event.x / SCALE
        y = event.y / SCALE
        self.mem0_label['text'] = "mem0: Null"
        self.mem1_label['text'] = "mem1: Null"
        self.ops_label['text'] = ""
        for human in self.zomframe.racoonCity.humans:
            if x == human.m_X and y == human.m_Y:
                self.mem0_label['text'] = "mem0:  " + str(human.m_Memory[0])
                self.mem1_label['text'] = "mem1:  " + str(human.m_Memory[1])
                ops = "ProgramCounter: " +  str(human.m_ProgramCounter) + "\n"
                for i, op in enumerate(human.m_Machine.m_Ops):
                    ops += str(i) + ": " + op.m_OpName + ", " + str(op.m_Param) + "\n"
                self.ops_label['text'] = ops
                break
        for zombie in self.zomframe.racoonCity.zombies:
            if x == zombie.m_X and y == zombie.m_Y:
                ops = "ProgramCounter: " +  str(zombie.m_ProgramCounter) + "\n"
                for i, op in enumerate(zombie.m_Machine.m_Ops):
                    ops += str(i) + ": " + op.m_OpName + ", " + str(op.m_Param) + "\n"
                self.ops_label['text'] = ops
                break



ZomApp().mainloop()
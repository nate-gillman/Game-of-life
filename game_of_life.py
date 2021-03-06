##   Nate Gillman
##   22 January 2017
##   Comp 112, Winter 2017 at Wesleyan University. Taught by Professor James Lipton
##   Final Project

## Nate Gillman's implementation of John Conway's "Game of Life"
## on a 35x40 matrix world. Enjoy!!

import tkinter as tk
import copy
import random

## this function is the only one defined outside of either of my classes
def count_neighbors(m, row, col):
    """
    m: matrix (list of equally sized lists), not necessarily square
    row: int within range(len(m)), signifying a row'th row in m
    col: int within range(len(m[0])), signifying the col'th column in 'm'
    the numbers are cardinal directions. if we're looking at x = m[row][col]:
            4 3 2
            5 x 1
            6 7 8
    return:int between 0 and 8, inclusive; = the number of living
    (i.e., non-zero) neighbors belonging to the (row,col)-entry of matrix m
    """
    count = 0
    if row in range(1,34) and col in range(1,39): #interior
        if m[row][col+1] == 1: #1
            count = count + 1
        if m[row-1][col+1] == 1: #2
            count = count + 1
        if m[row-1][col] == 1: #3
            count = count + 1
        if m[row-1][col-1] == 1: #4
            count = count + 1
        if m[row][col-1] == 1: #5
            count = count + 1
        if m[row+1][col-1] ==  1: #6
            count = count + 1
        if m[row+1][col] == 1: #7
            count = count + 1
        if m[row+1][col+1] == 1: #8
            count = count + 1
        return count
    elif row == 0 and col in range(1,39): #top row, no corners
        if m[row][col+1] == 1: #1
            count = count + 1
        if m[row][col-1] == 1: #5
            count = count + 1
        if m[row+1][col-1] ==  1: #6
            count = count + 1
        if m[row+1][col] == 1: #7
            count = count + 1
        if m[row+1][col+1] == 1: #8:
            count = count + 1
        return count
    elif row == 34 and col in range(1,39): #bottom row, no corners
        if m[row][col+1] == 1: #1
            count = count + 1
        if m[row-1][col+1] == 1: #2
            count = count + 1
        if m[row-1][col] == 1: #3
            count = count + 1
        if m[row-1][col-1] == 1: #4
            count = count + 1
        if m[row][col-1] == 1: #5
            count = count + 1
        return count
    elif col == 39 and row in range(1,34): #right column, no corners
        if m[row-1][col] == 1: #3
            count = count + 1
        if m[row-1][col-1] == 1: #4
            count = count + 1
        if m[row][col-1] == 1: #5
            count = count + 1
        if m[row+1][col-1] ==  1: #6
            count = count + 1
        if m[row+1][col] == 1: #7
            count = count + 1
        return count
    elif col == 0 and row in range(1,34): #left column, no corners
        if m[row][col+1] == 1: #1
            count = count + 1
        if m[row-1][col+1] == 1: #2
            count = count + 1
        if m[row-1][col] == 1: #3
            count = count + 1
        if m[row+1][col] == 1: #7
            count = count + 1
        if m[row+1][col+1] == 1: #8:
            count = count + 1
        return count
    elif row == 0 and col == 0: #top left corner
        if m[row][col+1] == 1: #1
            count = count + 1
        if m[row+1][col] == 1: #7
            count = count + 1
        if m[row+1][col+1] == 1: #8:
            count = count + 1
        return count
    elif row == 0 and col == 39: #top right corner
        if m[row][col-1] == 1: #5
            count = count + 1
        if m[row+1][col-1] ==  1: #6
            count = count + 1
        if m[row+1][col] == 1: #7
            count = count + 1
        return count
    elif row == 34 and col == 39: #bottom right corner
        if m[row-1][col] == 1: #3
            count = count + 1
        if m[row-1][col-1] == 1: #4
            count = count + 1
        if m[row][col-1] == 1: #5
            count = count + 1
        return count
    elif row == 34 and col == 0: #bottom left corner
        if m[row][col+1] == 1: #1
            count = count + 1
        if m[row-1][col+1] == 1: #2
            count = count + 1
        if m[row-1][col] == 1: #3
            count = count + 1
        return count

## this is the class that controls the logic behind the game
class game_of_life:
    
    def __init__(self):
        """
        creates a 35x40 zero matrix in the field 'matrix';
        that is, an 'empty world'
        does the same in the fields 'one_previous' and 'two_previous',
        which are used to store previous generations to form a color scheme;
        see "display_world()"
        the field 'gen_number', or the generation number, is likewise needed
        to develop the color scheme
        """
        self.gen_number = 0
        matrix = []
        for row in range(35):
            matrix.append([])
            for column in range(40):
                matrix[row].append(0)
        self.matrix = matrix
        self.one_previous = copy.deepcopy(matrix)
        self.two_previous = copy.deepcopy(matrix)

    ## the following 3 functions, "to_zero_[matrix/one_previous/two_previous]",
    ## are mutators that turn certain matrix fields into the zero matrix
        
    def to_zero_matrix(self):
        """
        result: mutates the field 'matrix' into the zero matrix
        """
        for row in range(35):
            for column in range(40):
                self.matrix[row][column] = 0

    def to_zero_one_previous(self):
        """
        result: mutates the field 'one_previous' into the zero matrix
        """
        for row in range(35):
            for column in range(40):
                self.one_previous[row][column] = 0

    def to_zero_two_previous(self):
        """
        result: turns the field 'two_previous' into the zero matrix
        """
        for row in range(35):
            for column in range(40):
                self.two_previous[row][column] = 0

    ## the following 7 methods, "to_[blinker/glider/die_hard/glider_gun/
    ## pulsar/almost_pulsar/random_configuration]" mutate the field
    ## self.matrix, turning the it into one of 7 initial configurations
    ## corresponding to the first 7 buttons
    
    def to_blinker(self):
        """
        result: mutates field 'matrix' into a 'blinker',
        which is one of the simplest period-2 oscillators
        """
        self.gen_number = 0
        self.to_zero_matrix()
        self.matrix[16][17] = 1
        self.matrix[17][17] = 1
        self.matrix[18][17] = 1

    def to_glider(self):
        """
        result: mutates self.matrix into a 'glider'
        """
        self.gen_number = 0
        self.to_zero_matrix()
        self.matrix[1][2] = 1
        self.matrix[2][3] = 1
        self.matrix[3][1] = 1
        self.matrix[3][2] = 1
        self.matrix[3][3] = 1

    def to_die_hard(self):
        """
        result: mutates field 'matrix' into 'die_hard' configuration,
        which is one of the simplest initial configurations that grows
        chaotically and then dies out after 130 generations
        """
        self.gen_number = 0
        self.to_zero_matrix()
        self.matrix[13][12]=1
        self.matrix[13][13]=1
        self.matrix[14][13]=1
        self.matrix[12][18]=1
        self.matrix[14][17]=1
        self.matrix[14][18]=1
        self.matrix[14][19]=1       

    def to_glider_gun(self):
        """
        mutator: turns self.matrix into a 'glider gun'
        fun fact: the discovery of the glider gun led to the proof that
        the Game of Life can function as a Turing machine (see Wikipedia)
        """
        self.gen_number = 0
        self.to_zero_matrix()
        #left block
        self.matrix[5][1] = 1
        self.matrix[6][1] = 1
        self.matrix[5][2] = 1
        self.matrix[6][2] = 1
        #left ship
        self.matrix[5][11] = 1
        self.matrix[6][11] = 1
        self.matrix[7][11] = 1
        self.matrix[4][12] = 1
        self.matrix[8][12] = 1
        self.matrix[3][13] = 1
        self.matrix[9][13] = 1
        self.matrix[3][14] = 1
        self.matrix[9][14] = 1
        self.matrix[6][15] = 1
        self.matrix[4][16] = 1
        self.matrix[8][16] = 1
        self.matrix[5][17] = 1
        self.matrix[6][17] = 1
        self.matrix[7][17] = 1
        #right ship
        self.matrix[6][18] = 1
        self.matrix[3][21] = 1
        self.matrix[4][21] = 1
        self.matrix[5][21] = 1
        self.matrix[3][22] = 1
        self.matrix[4][22] = 1
        self.matrix[5][22] = 1
        self.matrix[2][23] = 1
        self.matrix[6][23] = 1
        self.matrix[1][25] = 1
        self.matrix[2][25] = 1
        self.matrix[6][25] = 1
        self.matrix[7][25] = 1
        #right block
        self.matrix[3][35] = 1
        self.matrix[4][35] = 1
        self.matrix[3][36] = 1
        self.matrix[4][36] = 1

    def to_pulsar(self):
        """
        result: mutates field 'matrix' into a pulsar,
        which is a beautiful period-3 oscillator
        """
        self.gen_number = 0
        self.to_zero_matrix()
        #upper left
        self.matrix[11][13] = 1
        self.matrix[12][13] = 1
        self.matrix[13][13] = 1
        self.matrix[9][15] = 1
        self.matrix[9][16] = 1
        self.matrix[9][17] = 1
        self.matrix[11][18] = 1
        self.matrix[12][18] = 1
        self.matrix[13][18] = 1
        self.matrix[14][15] = 1
        self.matrix[14][16] = 1
        self.matrix[14][17] = 1
        #upper right
        self.matrix[11][20] = 1
        self.matrix[12][20] = 1
        self.matrix[13][20] = 1
        self.matrix[11][25] = 1
        self.matrix[12][25] = 1
        self.matrix[13][25] = 1
        self.matrix[9][21] = 1
        self.matrix[9][22] = 1
        self.matrix[9][23] = 1
        self.matrix[14][21] = 1
        self.matrix[14][22] = 1
        self.matrix[14][23] = 1
        #bottom left
        self.matrix[17][13] = 1
        self.matrix[18][13] = 1
        self.matrix[19][13] = 1
        self.matrix[17][18] = 1
        self.matrix[18][18] = 1
        self.matrix[19][18] = 1
        self.matrix[16][15] = 1
        self.matrix[16][16] = 1
        self.matrix[16][17] = 1
        self.matrix[21][15] = 1
        self.matrix[21][16] = 1
        self.matrix[21][17] = 1
        #bottom right
        self.matrix[17][20] = 1
        self.matrix[18][20] = 1
        self.matrix[19][20] = 1
        self.matrix[17][25] = 1
        self.matrix[18][25] = 1
        self.matrix[19][25] = 1
        self.matrix[16][21] = 1
        self.matrix[16][22] = 1
        self.matrix[16][23] = 1
        self.matrix[21][21] = 1
        self.matrix[21][22] = 1
        self.matrix[21][23] = 1

    def to_almost_pulsar(self):
        """
        result: mutates field 'matrix' into a pulsar with just one living
        cell replaced with a dead cell, which then goes crazy and eventually
        stabilizes; demonstrates the glorious chaos inherent in the
        Game of Life
        """
        self.gen_number = 0
        self.to_zero_matrix()
        #upper left
        self.matrix[11][13] = 1
        self.matrix[12][13] = 1
        self.matrix[13][13] = 1
        self.matrix[9][15] = 1
        self.matrix[9][16] = 1
        self.matrix[9][17] = 1
        self.matrix[11][18] = 1
        self.matrix[12][18] = 1
        self.matrix[13][18] = 1
        self.matrix[14][15] = 1
        self.matrix[14][16] = 1
        self.matrix[14][17] = 1
        #upper right
        self.matrix[11][20] = 1
        self.matrix[12][20] = 1
        self.matrix[13][20] = 1
        self.matrix[11][25] = 1
        self.matrix[12][25] = 1
        self.matrix[13][25] = 1
        self.matrix[9][21] = 1
        self.matrix[9][22] = 1
        self.matrix[9][23] = 1
        #the single cell in the pulsar that becomes dead in this perversion...
        #self.matrix[14][21] = 1
        self.matrix[14][22] = 1
        self.matrix[14][23] = 1
        #bottom left
        self.matrix[17][13] = 1
        self.matrix[18][13] = 1
        self.matrix[19][13] = 1
        self.matrix[17][18] = 1
        self.matrix[18][18] = 1
        self.matrix[19][18] = 1
        self.matrix[16][15] = 1
        self.matrix[16][16] = 1
        self.matrix[16][17] = 1
        self.matrix[21][15] = 1
        self.matrix[21][16] = 1
        self.matrix[21][17] = 1
        #bottom right
        self.matrix[17][20] = 1
        self.matrix[18][20] = 1
        self.matrix[19][20] = 1
        self.matrix[17][25] = 1
        self.matrix[18][25] = 1
        self.matrix[19][25] = 1
        self.matrix[16][21] = 1
        self.matrix[16][22] = 1
        self.matrix[16][23] = 1
        self.matrix[21][21] = 1
        self.matrix[21][22] = 1
        self.matrix[21][23] = 1

    def to_random_configuration(self,fraction_filled):
        """
        fraction_filled:float, between 0 and 1
        result: mutates field 'matrix', populating it randomly
        so that 'fraction_filled' is the approx. percentage of
        the world filled with live cells
        """
        self.gen_number = 0
        self.to_zero_matrix()
        for row in range(35):
            for col in range(40):
                x = random.randint(1,100)
                if x <= 100*fraction_filled:
                    self.matrix[row][col] = 1

    ## this is responsible for mutating self.matrix into the next generation
    def to_next_generation(self):
        """
        result: mutates field 'matrix' into the next generation,
        storing the current matrix in the field 'one_previous',
        and storing 'one_previous' in the field 'two_previous', if applicable
        """
        matrix_copy = copy.deepcopy(self.matrix) #to fix alaising issues
        if self.gen_number == 0:
            self.one_previous = copy.deepcopy(matrix_copy)
        elif self.gen_number >= 1:
            self.two_previous = copy.deepcopy(self.one_previous)
            self.one_previous = copy.deepcopy(matrix_copy)
        self.gen_number = self.gen_number + 1
        self.to_zero_matrix()
        for row in range(35):
            for col in range(40):
                x = count_neighbors(matrix_copy,row,col)
                if matrix_copy[row][col] == 1: #if alive...
                    if x == 2 or x == 3: #and if 2 or 3 live neighbors..
                        self.matrix[row][col] = 1 #then survives to next gen!!
                elif matrix_copy[row][col] == 0: #else, if dead...
                    if x == 3:#and if 3 live neighbors...
                        self.matrix[row][col] = 1#then alive in next gen!!

## takes care of the graphics
class gui:

    def __init__(self):
        """
        The action of the entire game goes on in this __init__ method
        """
        self.game = game_of_life()
        self.tkroot = tk.Tk()
        self.tkroot.geometry("1200x680+0+0")
        self.tkroot.configure(bg='light blue')
        self.tkroot.title("The Game of Life")
        
        ## creates the Canvas widget on which the game takes place
        self.canvas = tk.Canvas(self.tkroot)
        self.canvas.config(width=762,height=750,background='white')
        self.canvas.pack(side = tk.LEFT)

        def draw_grid_lines():
            """
            result: mutates field 'canvas', wiping it clean,
            then draws a 32x40 (rows x columns) grid on 'canvas'
            """
            self.canvas.delete('all')
            #first the vertical lines...
            for i in range(41):
                self.canvas.create_rectangle(19*i + 3,0, 19*i + 4, 668,\
                                             outline = 'grey')
            #and then the horizontal lines...
            for i in range(36):
                self.canvas.create_rectangle(0, 19*i + 3, 1000, 19*i + 4,\
                                             outline = 'grey')

        draw_grid_lines()

        ## creates a Frame widget for all the buttons
        self.frame = tk.Frame(self.tkroot)
        self.frame.pack(side = tk.RIGHT,padx=8)

        ## creates a Message widget for the game instructions
        self.message = tk.Message(self.frame)
        self.message.config(text = '                   \
     Welcome to The Game of Life!! \
                                                                   \
                                                    (as implemented by \
Nate Gillman for Comp 112 in Winter 2017, and basically as conceived of by John Conway)\n \n \
    The rules are simple: select an \
initial configuration (my personal favorite is "Pulsar"), \
then start the game, then restart when you get bored or when \
the game stabilizes, whichever happens first. Probably the latter. \
Additionally, you can choose how quickly the game evolves (the default is "Slow"). \
Also, note that the color of a first-generation cell is teal, \
the color of a second-generation cell is steel blue, and \
anything older than that is pale green. \n \
    As an added bonus, you can click on any square (before OR during play) to either kill \
or bring to life that cell. I highly recommend altering the \
initial configuration of Pulsar, either preserving the symmetry or \
not preserving the symmetry.\nEnjoy!! ')
        self.message.pack()

        ## the following 8 blocks of text create each of the 8 buttons,
        ## and hence each of the 8 possible game selections
        
        ## creates field 'button1': for selecting 'blinker'
        self.button1 = tk.Button(self.frame)
        self.button1.config(text='Click for "Blinker"')
        self.button1.pack()
        def action1():
            after_pick_sequence()
            self.game.to_blinker()
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button1.configure(command=action1)

        ## creates field 'button2': for selecting 'glider'
        self.button2 = tk.Button(self.frame)
        self.button2.config(text = 'Click for "Glider"')
        self.button2.pack()
        def action2():
            after_pick_sequence()
            self.game.to_glider()
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button2.configure(command=action2)

        ## creates field 'button3': for selecting 'die hard'
        self.button3 = tk.Button(self.frame)
        self.button3.config(text = 'Click for "Die Hard"')
        self.button3.pack()
        def action3():
            after_pick_sequence()
            self.game.to_die_hard()
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button3.configure(command=action3)

        ## creates field 'button4': for selecting 'glider gun'
        self.button4 = tk.Button(self.frame)
        self.button4.config(text = 'Click for "Glider Gun"')
        self.button4.pack()
        def action4():
            after_pick_sequence()
            self.game.to_glider_gun()
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button4.configure(command=action4)

        ## creates field 'button5': for selecting 'pulsar'
        self.button5 = tk.Button(self.frame)
        self.button5.config(text = 'Click for "Pulsar"')
        self.button5.pack()
        def action5():
            after_pick_sequence()
            self.game.to_pulsar()
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button5.configure(command=action5)

        ## creates field 'button6': for selecting 'not quite pulsar'
        self.button6 = tk.Button(self.frame)
        self.button6.config(text = 'Click for "(not quite) Pulsar"')
        self.button6.pack()
        def action6():
            after_pick_sequence()
            self.game.to_almost_pulsar()
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button6.configure(command=action6)

        ## creates field 'button7': for selecting 'random fill'
        self.button7 = tk.Button(self.frame)
        self.button7.config(text = 'Click for a random configuration')
        self.button7.pack()
        def action7():
            after_pick_sequence()
            self.game.to_random_configuration(.2) #I chose 20% filled
            self.canvas.bind("<Button-1>", update)
            display_world()
        self.button7.configure(command=action7)

        ## creates field 'DIY_button', which lets the user make
        ## a custom world by clicking on squares of their choosing
        self.DIY_button = tk.Button(self.frame)
        self.DIY_button.config(text = 'Click to make custom world')
        self.DIY_button.pack()
        #self.DIY_button.config(state='normal')
        def DIY():
            after_pick_sequence()
            self.game.to_zero_matrix()
            self.canvas.bind("<Button-1>", update)
            display_world()

        ## this is the function that every one of the
        ## 8 above world buttons references
        def update(event):
            """
            collects the x,y coordinates of the mouseclick,
            then maps that to the i,j entry of self.game.matrix,
            then changes state of that cell based on the click
            because modular arithmetic is awesome
            """
            self.x, self.y = event.x, event.y
            #print "(x,y) = ", event.x, event.y
            self.i = int((self.y-6)/19)
            self.j = int((self.x-6)/19)
            ## my way of making it easy for the player to un-select a square;
            ## I <3 MODULAR ARITHMETIC!!!! <3 <3 <3
            self.game.matrix[self.i][self.j] \
                = (self.game.matrix[self.i][self.j]+1)%2
            display_world()
        self.DIY_button.configure(command=DIY)
        
        ## creates field 'start_button'
        ## the start button disables the game and start buttons while
        ## enabling the restart button, takes speed input from radiobutton,
        ## moves the game along to the next generation,
        ## and then displays this next generation, all on a timer
        self.start_button = tk.Button(self.frame)
        self.start_button.config(text = 'Click to start the Game of Life!')
        self.start_button.pack()
        self.start_button.configure(state='disabled')
        def start():
            after_start_sequence()
            self.id = self.tkroot.after(self.speed,start)
            self.game.to_next_generation()
            display_world()
        self.start_button.configure(command=start)
        
        ## creates field 'restart_button', which resets the generation number
        ## field, wipes clean all the past generation matrices, re-enables
        ## all the game buttons while disabling the start and restart buttons,
        ## cancels the timer, and redraws a clean grid on the 'canvas'
        self.restart_button = tk.Button(self.frame)
        self.restart_button.config(text = 'Click to restart')
        self.restart_button.pack()
        self.restart_button.config(state='disabled')
        def restart():
            self.game.gen_number = 0
            self.game.to_zero_matrix()
            self.game.to_zero_one_previous()
            self.game.to_zero_two_previous()
            after_restart_sequence()
            self.canvas.unbind("<Button-1>")
            self.tkroot.after_cancel(self.id)
            draw_grid_lines()
        self.restart_button.configure(command=restart)

        ## the following 3 function "sequences" change the status of
        ## the buttons, based on which button was pressed
        
        def after_pick_sequence():
            """
            this changes the status of the buttons after
            the one of the 8 game buttons is selected
            """
            self.button1.config(state = "disabled")
            self.button2.config(state = "disabled")
            self.button3.config(state = "disabled")
            self.button4.config(state = "disabled")
            self.button5.config(state = "disabled")
            self.button6.config(state = "disabled")
            self.button7.config(state = "disabled")
            self.DIY_button.config(state = "disabled")
            self.start_button.config(state = "normal")
            self.restart_button.config(state="disabled")

        def after_start_sequence():
            """
            this changes the status of the buttons after
            the START button is pressed
            """
            self.button1.config(state = "disabled")
            self.button2.config(state = "disabled")
            self.button3.config(state = "disabled")
            self.button4.config(state = "disabled")
            self.button5.config(state = "disabled")
            self.button6.config(state = "disabled")
            self.button7.config(state = "disabled")
            self.DIY_button.config(state = "disabled")
            self.start_button.config(state = "disabled")
            self.restart_button.config(state="normal")

        def after_restart_sequence():
            """
            this changes the status of the buttons after
            RESTART button is pressed
            """
            self.button1.config(state = "normal")
            self.button2.config(state = "normal")
            self.button3.config(state = "normal")
            self.button4.config(state = "normal")
            self.button5.config(state = "normal")
            self.button6.config(state = "normal")
            self.button7.config(state = "normal")
            self.DIY_button.config(state = "normal")
            self.start_button.config(state = "disabled")
            self.restart_button.config(state="disabled")
       
        def display_world():
            """
            result: mutates 'self.canvas', painting the current
            self.game.matrix onto self.canvas,
            taking into account how "old" the (i,j)-entry is;
            i.e., for how many past consecutive generations has the
            (i,j)-entry of self.game.matrix been a 1
            """
            self.canvas.delete("all")
            draw_grid_lines()
            for i in range(35):
                for j in range(40):
                    if self.game.matrix[i][j] == 1:
                        if self.game.one_previous[i][j] == 1:
                            if self.game.two_previous[i][j] == 1:
                                self.canvas.create_rectangle(5+19*j,5+19*i,\
                                21+19*j,21+19*i,outline='pale green',\
                                fill='pale green')
                            else:
                                self.canvas.create_rectangle(5+19*j,5+19*i,\
                                21+19*j,21+19*i,outline='steel blue',\
                                fill='steel blue')
                        else:
                            self.canvas.create_rectangle(5+19*j,5+19*i,\
                            21+19*j,21+19*i,outline='cadet blue',\
                            fill='cadet blue')

        ## sets the default speed at 1000 ms,
        ## which is the same as 'Slow' speed
        self.speed = 1000
        
        ## creates the radiobutton so user can select speed
        def select():
            """
            result: mutates 'self.speed', storing in that field the value
            output of whichever radiobutton was pressed
            """
            self.speed = self.var.get()
        ## tells 'self.var', the field that the output of the buttons is
        ## stored in, to expect an variable of type Int
        self.var = tk.IntVar()
        ## the "Slow" radiobutton...
        self.R1 = tk.Radiobutton(self.frame, text = "Slow", variable = self.var,\
                                 value = 1000, command=select)
        self.R1.pack(anchor = tk.W)
        ## the "Medium" radiobutton...
        self.R2 = tk.Radiobutton(self.frame, text = "Medium", variable = self.var,\
                                 value = 300, command=select)
        self.R2.pack(anchor = tk.W)
        ## the "Fast" radiobutton...
        self.R3 = tk.Radiobutton(self.frame, text = "Fast", variable = self.var,\
                                 value = 150, command=select)
        self.R3.pack(anchor = tk.W)
        ## the "Super duper fast" radiobutton...
        self.R4 = tk.Radiobutton(self.frame, text = "Super duper fast",\
                                 variable = self.var, value = 50, command=select)
        self.R4.pack(anchor = tk.W)
                 
        ## enters into the "self.tkroot" window
        self.tkroot.mainloop()

## begins the GUI event!!!
gui()

from pynput import keyboard 
import signal 
import sys
from time import sleep
import utils.constants as constants
from utils.constants import Cursor
from io import StringIO


global cursor
global enter_mode
global ascii_table
"""
need to lock on an ascii table, or at least read from one.
with that, events should be fired asynchronously and caught 
by decoupled functions controlling a single, global ascii 2d array

option two

master/slave relation ship with threads or even processes 



___________________________________________________________________
  e|-0---0------/7--7----2-3-2--0----------------------------------
> B|----------------------3----------------------------------------
  D|---------------------------------------------------------------
  G|---2-2-----0---------------------------------------------------
  A|---------------------0-----------------------------------------
  E|-0--------------------------0----------------------------------
"""

def read_from_file(filename):
    f = open(filename, 'r')
    ascii_table
    for line in filename:
        for char in line:
            ascii_table[0]


def on_press(key):
    global enter_mode
    try:
        if enter_mode:
            try: cursor.to_write(key.char) 
            except AttributeError as ex: pass
        if key == keyboard.Key.space:
            if enter_mode == True:
                enter_mode = False
                print("Written")
            else: 
                print("Adding to buffer...")
                enter_mode = True
        if key == keyboard.Key.left:
            cursor.move_left()
        if key == keyboard.Key.backspace:
            ascii_table[cursor.y][cursor.x] = '-'
        if key == keyboard.Key.right:
            cursor.move_right()
        if key == keyboard.Key.down:
            cursor.move_down()
        if key == keyboard.Key.up:
            cursor.move_up()
        if key == keyboard.Key.enter:
            cursor.flush()
            print_ascii(ascii_table=ascii_table)
        
        if key.char == 'q':
            print("quitting...")
    except AttributeError as ex:
        pass
    except Exception as e:
        print(f"""
    DEBUG OUTPUT 
        CURSOR X: {cursor.x}, CURSOR Y: {cursor.y} 
        problem child: ascii_table[{cursor.y}][{cursor.x}]

""")
        raise(e)


def print_line(multiple_of_measure_length=0):
    print(multiple_of_measure_length * constants.MEASURE_LENGTH)

def print_line(num_chars):
    print(num_chars * "_")

def setup(tab: StringIO) -> tuple[list[list[str]], str]:
    lines = [[" ", " ", "e|", "-","-","-","-" ],
             [" ", " ", "B|", "-","-","-","-",], 
             [" ", " ", "D|", "-","-","-","-",], 
             [" ", " ", "G|", "-","-","-","-",], 
             [" ", " ", "A|", "-","-","-","-",], 
             [" ", " ", "E|", "-","-","-","-",]]
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            tab.write(lines[i][j])
        tab.write('\n')
    return lines, tab.getvalue()

def print_ascii(ascii_table: list[list[str]] = None) -> None:
    temp = StringIO()
    for i in range(len(ascii_table)):
        # to get the cursor in the right place
        if i == cursor.y:
            ascii_table[cursor.y][0] = '>'
        else:
            ascii_table[i][0] = ' '
        # -----------for-additions-----------------------
        
        if cursor.is_flushing:
            if len(ascii_table[cursor.y]) < 2 - cursor.x:
                add_empty_bar(ascii_table, 10)
            
            print(len(cursor.buffer))
            if len(cursor.buffer) == 1 and not cursor.buffer[0].isnumeric():
                ascii_table[cursor.y][cursor.x + 1] = cursor.buffer[i]
                ascii_table[cursor.y][cursor.x + 2] = '|'
            for i in range(len(cursor.buffer)):
                ascii_table[cursor.y][cursor.x + 1] = cursor.buffer[i]
                cursor.x += 1
            cursor.buffer = []
            cursor.is_flushing = False

        #----------"printing" the frets-------------------
        for j in range(len(ascii_table[0])):
            temp.write(ascii_table[i][j])
        temp.write('\n')

    printer(temp.getvalue())


def printer(printable: str):
    print(printable)


def add_empty_bar(ascii:list[list[str]], n_bars:int=1):
    if n_bars < 1:
        return ascii
    for i in range(len(ascii)):
        for j in range(n_bars):
            ascii[i].append('-')
    return ascii


def main():

    tab = StringIO()
    printer("""
            Press SPACEBAR to enter "enter mode"
            wherein you can type any number of characters (ex. 14)
            press SPACEBAR when you're done to add it to the buffer.

            To actually print the tab, press ENTER to write whatever -
            - is in your buffer to the tab

            ps. resize to the top of this msg for the best experience
            Press any button to begin....
            """)
    old_pos = cursor.x
    old_posy = cursor.y
    while True:
        if old_pos == cursor.x and old_posy == cursor.y: continue
        else:
            if cursor.x > len(ascii_table[0]):
                add_empty_bar(ascii_table, 4)

            old_pos = cursor.x
            old_posy = cursor.y

        print()
        print()
        cursor.print_x()
        print_line(len(ascii_table[0]) + 1)
        print_ascii(ascii_table)
        print(f'\n IN BUFFER: {"".join(cursor.buffer)}')
        if enter_mode: print(f'Writing...') 




if __name__ == '__main__':
    ascii_table, _ = setup(StringIO())

    cursor = Cursor(0, 2)
    enter_mode = False
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    main()

from pynput import keyboard # type: ignore
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
"""

def on_press(key):
    global enter_mode
    try:
        if key == keyboard.Key.space:
            if enter_mode == True:
                enter_mode = False
            else: 
                enter_mode = True
            print(enter_mode)
        if key == keyboard.Key.left:
            cursor.move_left()
        if key == keyboard.Key.right:
            cursor.move_right()
        if key == keyboard.Key.down:
            cursor.move_down()
        if key == keyboard.Key.up:
            cursor.move_up()
        if key == keyboard.Key.enter:
            cursor.flush()
        if enter_mode:
            try:
                if key.char:
                    cursor.to_write(key.char)
            except AttributeError:
                pass

        if key.char == 'q':
            print("quitting...")
    except AttributeError as ex:
        pass


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

def print_ascii(ascii: list[list[str]]) -> None:
    temp = StringIO()
    for i in range(len(ascii)):
        # to get the cursor in the right place
        if i == cursor.y:
            ascii[cursor.y][0] = '>'
        else:
            ascii[i][0] = ' '
        # -----------------------------------

        if cursor.is_flushing:
            ascii[cursor.y][cursor.x] = "".join(cursor.buffer)
            cursor.buffer = []
            cursor.is_flushing = False

        #----------writing the frets-------------------
        for j in range(len(ascii[0])):
            temp.write(ascii[i][j])
        temp.write('\n')

    printer(temp.getvalue())


def printer(printable: str):
    print(printable)


def add_empty_bar(ascii):
    for i in range(len(ascii)):
        ascii[i].append('-')
    return ascii


def main():
    tab = StringIO()
    ascii_tab, printable_tab = setup(tab)
    printer("""
            Press space to enter "enter mode"
            wherein you can type any number of characters (ex. 14)
            press space when you're done to print it to the tab.

            Press any button to begin....
            """)
    old_pos = cursor.x
    old_posy = cursor.y
    while True:
        if old_pos == cursor.x and old_posy == cursor.y: continue
        else:
            if cursor.x > len(ascii_tab[0]):
                add_empty_bar(ascii=ascii_tab)
            old_pos = cursor.x
            old_posy = cursor.y

        print()
        print()
        cursor.print_x()
        print_line(len(ascii_tab[0]) + 1)
        print_ascii(ascii_tab)
        print(f'\n IN BUFFER: {"".join(cursor.buffer)}')
        if enter_mode: print(f'Writing...') 




if __name__ == '__main__':
    ascii_table, _ = setup(StringIO())

    cursor = Cursor(0, 0)
    enter_mode = False
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    main()

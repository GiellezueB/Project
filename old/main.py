# main file
# luca nederhorst
# digital forensics tool

import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv
from tkinter import *
from PIL import ImageTk, Image
from matplotlib.pyplot import text
# from Main import pipeline
# import Object_Detection
# from Object_Detection import Simulation
from tkinter import filedialog


# create window
window = tk.Tk()
window.configure(background='gray')

# create title of window
window.title('TimEx Tool')

# get screen dimension to create size of window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = int(screen_width/1.5)
window_height = int(screen_height/1.5)

# center point of window
center_x = int(screen_width/2 - window_width/1.5)
center_y = int(screen_height/2 - window_height/2)

window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# window is not resizeable
window.resizable(False, False)


# create input grid area for implementing different widgets/entry boxes
window.columnconfigure((0, 1, 2, 3, 4), weight=1)
window.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)


# create title and input entry's
title = tk.Label(
    text='TimEx',
    foreground='black',
    background='gray',
    font=('Times', 30, 'bold')
)
title.grid(row=1, column=2)


# create input for csv
# entry_label = tk.Label(
#    text="load document (.csv):",
#    foreground='black',
#    background='gray',
#    font=('Times', 15, 'bold')
# )
#entry_label.grid(row=3, column=0, pady=2, padx=0, sticky=E)

# function for browsing files on computer


def file_searcher():
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select a csv file",
        filetypes=((("Text files",
                     "*.txt*"),
                    ("all files",
                    "*.*")))
    )
    print(file_path)


# def copy_file_path():
#    print(csv_file_path)


search_button = tk.Button(
    window,
    text='Browse Files',
    font=('Times', 15, 'bold'),
    command=file_searcher,
)


search_button.grid(
    row=3,
    column=2,
    sticky=S,
    pady=2
)


exit_button = tk.Button(
    window,
    text="Exit",
    font=('Times', 15, 'bold'),
    command=exit
)
exit_button.grid(
    row=4,
    column=2,
    sticky=N,
    pady=2
)


# listbox to visualize data
# listbox_label = tk.Label(
#    text="csv data:",
#    foreground='black',
#    background='gray',
#    font=('Times', 15, 'bold')
# )
#listbox_label.grid(row=2, column=2, sticky=SW)
#listbox = tk.Listbox(window)
#listbox.grid(row=3, column=2, sticky=NW)


window.mainloop()

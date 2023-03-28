import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import filedialog

class Widget():
    def __init__(self):
        # create window
        self.window = tk.Tk()
        self.filepath = None
        
        self.init_window()
        
    def init_window(self):
        self.window.configure(background='gray')

        # create title of window
        self.window.title('TimEx Tool')

        # get screen dimension to create size of window
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        window_width = int(self.screen_width/1.5)
        window_height = int(self.screen_height/1.5)

        # center point of window
        center_x = int(self.screen_width/2 - window_width/1.5)
        center_y = int(self.screen_height/2 - window_height/2)

        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # window is not resizeable
        self.window.resizable(False, False)

        # create input grid area for implementing different widgets/entry boxes
        self.window.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.window.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # create title and input entry's
        title = tk.Label(text='TimEx', foreground='black', background='gray', font=('Times', 30, 'bold'))
        title.grid(row=1, column=2)
        
        # Get filepath
        self.filepath = tk.StringVar()
        
        # create search buttons
        search_button = tk.Button(
            self.window,
            text='Browse Files',
            font=('Times', 15, 'bold'),
            command=self.file_searcher)
        search_button.grid(
            row=3,
            column=2,
            sticky=tk.S,
            pady=2)

        # create run buttons
        run_button = tk.Button(
            self.window,
            text="Run",
            font=('Times', 15, 'bold'),
            command=self.file_searcher)
        run_button.grid(
            row=4,
            column=2,
            sticky=N,
            pady=2)

    def file_searcher(self):
        filepath = filedialog.askopenfilename(initialdir="/",
                                               title="Select a csv file",
                                               filetypes=((("CSV files", "*.csv*"), 
                                                           ("all files", "*.*"))))
        
        self.filepath = filepath
        self.data = pd.read_csv(filepath)
        self.window.destroy()

class newWidget():
    def __init__(self):
        notebook = ttk.Notebook()
    
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x300')
    root.title('Notebook demo')
    
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)
    
    frame1 = ttk.Frame(notebook, width=400, height=280)
    frame2 = ttk.Frame(notebook, width=400, height=280)
    
    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    
    notebook.add(frame1, text='General information')
    notebook.add(frame2, text='Profile')
    
    root.mainloop()
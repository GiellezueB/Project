import tkinter as tk
import pandas as pd
import tkinter.filedialog as fd

import tksheet
from tkinter import ttk

class MainWidget():
    def __init__(self):
        self.root = tk.Tk()
        
        self.filepath = None

        self.ranking_calculated = False        
        self.data_loaded = False
        
        self.data = pd.DataFrame()
        
        self.build_root()
        self.build_notebook()
        
    def build_root(self):
        # First build the window
        self.root.title('TimEx')
        
        # Get screen dimension to create size of window
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.window_width = int(self.screen_width/1.5)
        self.window_height = int(self.screen_height/1.5)

        # Center point of window
        center_x = int(self.screen_width/2 - self.window_width/1.5)
        center_y = int(self.screen_height/2 - self.window_height/2)

        self.root.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
    def build_notebook(self):
        # Next build the notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.enable_traversal()
        
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # Next add the frames
        self.frm_data = self.FRM_Data()
        self.frm_options = self.FRM_Options()
        self.frm_ranking = self.FRM_Ranking()
        
        self.notebook.add(self.frm_data, text='Data')
        self.notebook.add(self.frm_options, text='Options')
        self.notebook.add(self.frm_ranking, text='Ranking')
        
    def run(self):
        self.root.mainloop()

    def FRM_Data(self):
        frm = ttk.Frame(self.notebook, width = self.window_width, height = self.window_height - 20)
        frm.pack(fill='both', expand=True)
    
        # create title and input entry's
        title = tk.Label(
            text='TimEx',
            foreground='black',
            background='gray',
            font=('Times', 30, 'bold')
        )
        title.pack()

        search_button = tk.Button(
            frm,
            text='Browse Files', font=('Times', 15, 'bold'),
            command=self.file_searcher)
        search_button.pack()
                
        return frm
        
    def FRM_Options(self):
        frm = ttk.Frame(self.notebook, width = self.window_width, height = self.window_height - 20)
        frm.pack(fill='both', expand=True)
        
        btn_prev = tk.Button(frm, text="Show Data preview", command=self.show_data)    
        btn_ranking = tk.Button(frm, text="Calculate Ranking", command=self.show_ranking)
        
        btn_prev.pack()
        btn_ranking.pack()
        
        return frm
    
    def FRM_Ranking(self):
        frm = ttk.Frame(self.notebook, width = self.window_width, height = self.window_height - 20)
        frm.pack(fill='both', expand=True)
        return frm
        
    def file_searcher(self):
        filepath = fd.askopenfilename(initialdir="/",
                                      title="Select a csv file",
                                      filetypes=((("CSV files", "*.csv*"), 
                                                  ("all files", "*.*"))))
        
        self.filepath = filepath
        self.data = pd.read_csv(self.filepath)

    def show_data(self):
        dw = DataWidget(data=self.data).show_data()

    def show_ranking(self):
        self.notebook.select(2)
        
class DataWidget():
    def __init__(self, data):
        self.data = list(data.itertuples(index=False, name=None))
        
        self.root = tk.Tk()
        self.window_width = 1000
        self.window_height = 500 
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        self.frame = tk.Frame()
        self.sheet = tksheet.Sheet(self.root, data = self.data, width=self.window_width, height=self.window_height)
        self.sheet.enable_bindings()
        self.sheet.grid(row=0, column=0, sticky="nswe")
    
    def show_data(self):
        self.root.mainloop()
        
if __name__ == '__main__':
    w = MainWidget()
    w.run()
# main file
# luca nederhorst
# digital forensics tool
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import pandas as pd
import tksheet
import os

from tkinter import filedialog, ttk
from tkinter import *

from tkinter.ttk import *
from help.data import EventData


class Timex():
    def __init__(self, mbs_api):
        self.mbs_api = mbs_api
        
        self.raw_data = None
        self.filtered_data = None
        self.event_data = None
        self.routing_data = None
        self.ranking_data_hp = None
        self.ranking_data_hd = None
        self.ranking_data = None
        self.possible_combinations = None  
        self.crime_idx = None
        self.file_label = None
        
        self.age = 20
        
        self._init_build()
        
    def _init_build(self):
        self._build_window()
        self._build_step_one()
        self._build_step_two()
        self._build_step_three()
        self._build_step_four()
        self._build_step_five()
        
        self._build_exit()
        
    def _build_window(self):
        # create window
        self.root = tk.Tk()
        self.root.configure(background='lightgray')

        # create title of window
        self.root.title('TimEx Tool')

        # get screen dimension to create size of window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width/2)
        window_height = int(screen_height/1.2)

        # center point of window
        center_x = int(screen_width/2 - window_width/1.5)
        center_y = int(screen_height/2 - window_height/2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # window is not resizeable
        self.root.resizable(False, False)

        # create input grid area for implementing different widgets/entry boxes
        self.root.columnconfigure((0, 1, 2), weight=1)
        self.root.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # create title TimEx
        title = tk.Label(
            text='TimEx',
            foreground='#0A025E',
            background='lightgray',
            font=('System', 20, 'bold'))

        title.grid(
            row=0,
            column=1,
            columnspan=2)

    def _build_step_one(self):
        # step 1: Import file
        def file_searcher():
            file_path = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Select a csv file",
                filetypes=((("CSV files",
                            "*.csv*"),
                            ("all files",
                            "*.*"))))
            self.raw_data = pd.read_csv(file_path)
            self.file_label.config(text=file_path.split("/")[-1])
            
            self.get_event_data()
            
            self.preview_data_button['state'] = 'active'
            self.calculate_ranking_button['state'] = 'active'
            self.foot_checkbutton['state'] = 'active'
            self.bike_checkbutton['state'] = 'active'
            self.car_checkbutton['state'] = 'active'
            
        def preview_file_data():
            DataWidget(data=self.event_data.data).show_data()

        step1 = tk.Label(
            text="Step 1) Import csv file",
            foreground="#0A025E",
            background="lightgray",
            font=('System', 11))
        step1.grid(row=1, column=1, sticky=NW, pady=5)
        
        search_button = tk.Button(
            self.root,
            text='Import from files',
            font=('Times', 11),
            command=file_searcher)
        search_button.grid( row=1, column=1, sticky=W, pady=10, padx=20)
        
        self.preview_data_button = tk.Button(
            self.root,
            text="Preview file data",
            font=("Times", 11),
            state=DISABLED,
            command=preview_file_data)
        self.preview_data_button.grid( row=1, column=1, sticky=E, pady=15, padx=20)
        
        self.file_label = tk.Label(
            text=self.file_label)
        self.file_label.grid(row=1, column=1, sticky=S, pady=15, padx=20)

    def _build_step_two(self):
        # step 2: Filter data on:
        step2 = tk.Label(text="Step 2) Filter data imported file on:",
                        foreground="#0A025E",
                        background="lightgray",
                        font=('System', 11))
        step2.grid( row=2, column=1, sticky=NW, pady=5)

        # filter 1: transport
        include_transport = tk.Label(text="Include following transport:",
                                    foreground="black",
                                    background="lightgray",
                                    font=('Times', 9))
        include_transport.grid(row=2,column=1,sticky=W,pady=2,padx=10)
        
        self.filter_foot = tk.IntVar()
        self.foot_checkbutton = tk.Checkbutton(
            self.root,
            text="By foot",
            background='lightgray',
            variable=self.filter_foot,
            state=DISABLED)
        self.foot_checkbutton.select()
        self.foot_checkbutton.grid(row=2, column=1, sticky=SW, pady=10, padx=20)

        self.filter_bike = tk.IntVar()
        self.bike_checkbutton = tk.Checkbutton(
            self.root,
            text="By bike",
            background='lightgray',
            variable=self.filter_bike,
            state=DISABLED)
        self.bike_checkbutton.select()
        self.bike_checkbutton.grid(row=2, column=1, sticky=S, pady=10, padx=20)

        self.filter_car = tk.IntVar()
        self.car_checkbutton = tk.Checkbutton(
            self.root,
            text="By car",
            background='lightgray',
            variable=self.filter_car,
            state=DISABLED)
        self.car_checkbutton.select()
        self.car_checkbutton.grid(row=2, column=1, sticky=SE, pady=10, padx=20)

        # filter 2: minimum number of events
        eventamount_label = tk.Label(text="Minimal number of events in route:",
                                    foreground="black",
                                    background="lightgray",
                                    font=('Times', 9))
        eventamount_label.grid(row=2,column=2,sticky=W,pady=2,padx=10)

        eventamount = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.filter_eventamount = ttk.Combobox(
            self.root,
            values=eventamount,
            text='event amount')
        self.filter_eventamount.current(3)
        self.filter_eventamount.grid( row=2, column=2, sticky=SW, pady=10, padx=20)

    def _build_step_three(self):
        def show_ranking():
            DataWidget(data=self.ranking_data).show_data()
            
        step3 = tk.Label(text="Step 3) Ranking",
                        foreground="#0A025E",
                        background="lightgray",
                        font=('System', 11))
        step3.grid(row=3,column=1,sticky=NW,pady=5)

        self.use_histTraf = tk.IntVar()
        histTraf_checkbutton = tk.Checkbutton(
            self.root,
            text="Include historical traffic information",
            background='lightgray',
            var=self.use_histTraf)
        histTraf_checkbutton.select()
        histTraf_checkbutton.grid(row=3,column=1,sticky=W,padx=20)
        
        age_label = tk.Label(text="Age of the suspect",
                             foreground="black",
                             background="lightgray",
                             font=('Times', 9))
        age_label.grid(row=3,column=2,sticky=W,pady=2,padx=10)
        
        self.ent_age = tk.Entry(
            self.root
        )
        self.ent_age.grid(row=3, column=2, sticky=SW, pady=10, padx=20)
        self.ent_age.insert(-1, 20)

        self.calculate_ranking_button = tk.Button(
            self.root,
            text='Calculate ranking',
            font=('Times', 11),
            state=DISABLED,
            command=self.get_ranking_data)
        self.calculate_ranking_button.grid(row=4,column=1,sticky=SW,pady=15,padx=20)

        # show ranking
        self.show_ranking_button = tk.Button(
            self.root,
            text='Show ranking',
            font=('Times', 11),
            state=DISABLED,
            command=show_ranking)
        self.show_ranking_button.grid(row=4,column=1,sticky=SE,pady=15,padx=20)
        
        # export ranking
        self.export_ranking_button = tk.Button(
            self.root,
            text='Export ranking',
            foreground='darkgreen',
            font=('Times', 11),
            width=12,
            state=DISABLED,
            command=self.export_ranking)
        self.export_ranking_button.grid( row=4, column=2, sticky=S, pady=15)

    def _build_step_four(self):
        # step 5: Choose route from ranking to visualize
        step5 = tk.Label(text="Step 4) Choose route from ranking to visualize",
                 foreground="#0A025E",
                 background="lightgray",
                 font=('System', 11))
        step5.grid(row=5,column=1,sticky=NW,pady=5)

        routes = []
        self.route_combobox = ttk.Combobox(
            self.root,
            values=routes)
        self.route_combobox.grid(row=5,column=1,sticky=W,pady=5,padx=20)

        self.export_route_vis_button = tk.Button(
            text="Export route visualization",
            font=('Times', 11),
            command=self.export_route_vis,
            state=DISABLED)
        self.export_route_vis_button.grid(row=5, column=1, sticky=E, pady=5, padx=20)
        
        self.export_route_button = tk.Button(
            self.root,
            text='Export route data',
            foreground='darkgreen',
            font=('Times', 11),
            width=12,
            command=self.export_route_data,
            state=DISABLED)
        self.export_route_button.grid(row=5,column=2,pady=20)

    def _build_step_five(self):
        def show_dist():            
            self.get_plot(output='show')
            
        def export_dist():            
            self.get_plot(output='save')
            
        # step 6: Hp and Hd graphics
        step6 = tk.Label(text="Step 6) Visualize probability per hypothesis",
                        foreground='#0A025E',
                        background='lightgray',
                        font=('System', 11)
                        )
        step6.grid(row=6,column=1,sticky=NW,pady=5)

        self.h_val_label = tk.Label(
            text="Hp: Hd: ")
        self.h_val_label.grid(row=6, column=1, sticky=W, pady=15, padx=20)
        
        self.show_distribution_button = tk.Button(
            text="Show Hp/Hd",
            font=('Times', 11),
            state=DISABLED,
            command=show_dist)
        self.show_distribution_button.grid(row=6, column=1, sticky=E, pady=5, padx=20)
        
        self.export_plot_button = tk.Button(
            self.root,
            text='Export plot',
            foreground='darkgreen',
            font=('Times', 11),
            width=12,
            state=DISABLED,
            command=export_dist)
        self.export_plot_button.grid(row=6,column=2,pady=20)
        
    def _build_exit(self):
        # exit Timex
        def exit():
            self.root.quit()

        exit_button = tk.Button(
            self.root,
            text="Exit TimEx",
            foreground='darkred',
            font=('Times', 11),
            command=exit)
        exit_button.grid(row=7, column=1, columnspan=2)

    def export_csv(self, data):
        fn = filedialog.asksaveasfile(
                initialdir="/",
                title=f"Select a CSV file",
                filetypes=((("CSV files",
                            "*.csv"),
                            ("all files",
                            "*.*"))))
        
        if fn:    
            fn = fn.name if fn.name.endswith('.csv') else fn.name + ".csv"
            data.to_csv(fn, lineterminator='\n')
            
    def export_ranking(self):
        self.export_csv(self.ranking_data)
        
    def export_route_data(self):
        selected_route = list(self.route_combobox.get())
        data = self.event_data.data.loc[selected_route]
        
        data_shifted = data.shift(-1).add_prefix('end_')
        temp = pd.concat([data.add_prefix('start_'), data_shifted], axis=1)    
        temp = temp.rename(columns={'timestamp': 'start_timestamp', 'location': 'start_location'})
        temp = temp.dropna(subset=['end_timestamp', 'end_location']) 
        temp = temp[['start_timestamp', 'start_location', 'end_timestamp', 'end_location']]
        self.export_csv(temp)
        
    def export_route_vis(self):
        fn = filedialog.asksaveasfile(
            initialdir="/",
            title=f"Select an HTML file",
            filetypes=((("HTML files",
                        "*.html"),
                        ("all files",
                        "*.*"))))
        if fn:
            fn = fn.name if fn.name.endswith('.html') else fn.name + ".html"

            selected_route = list(self.route_combobox.get())
            data = self.event_data.data.loc[selected_route]
            coords = list(data['location_coords'])
            timestamps = list(data['timestamp'])
            locations = list(data['location'])
            
            self.mbs_api.plot_directions(coords, timestamps, locations, fn)
        
    def get_plot(self, output="show"):
        plt.clf()
        
        bins = np.linspace(0, 1, 100)
        plt.hist(self.ranking_data_hp['probability'], bins, alpha=0.5, label='Hp')
        plt.hist(self.ranking_data_hd['probability'], bins, alpha=0.5, label='Hd')
            
        plt.xlabel('Probability score')
        plt.ylabel('Frequency')
            
        plt.legend(loc='upper right')
        
        if output == 'show':
            plt.show()
        
        elif output == 'save':
            fn = filedialog.asksaveasfile(
            initialdir="/",
            title=f"Select a PNG file",
            filetypes=((("PNG files",
                        "*.png*"),
                        ("all files",
                        "*.*"))))
        
            if fn:
                fn = fn.name if fn.name.endswith('.png') else fn.name + ".png"
                
            plt.savefig(fn)
            
    def get_event_data(self):
        self.filtered_data = self.raw_data.copy()
        if self.filter_foot.get() == 0:
            self.filtered_data = self.filtered_data[self.filtered_data['transportmode'] != 'By foot']
        if self.filter_bike.get() == 0:
            self.filtered_data = self.filtered_data[self.filtered_data['transportmode'] != 'By bike']
        if self.filter_car.get() == 0:
            self.filtered_data = self.filtered_data[self.filtered_data['transportmode'] != 'By car']

        self.event_data = EventData(data=self.filtered_data, mbs_api=self.mbs_api)
        
    def get_ranking_data(self):
        self.crime_idx = self.event_data.data[self.event_data.data['method'] == 'Delict'].index.values[0]
        self.age = int(self.ent_age.get())
        
        if self.use_histTraf.get() == 1:
            self.routing_data = self.event_data.get_possible_routes(age=self.age, include_historical_traffic=True)
        else:
            self.routing_data = self.event_data.get_possible_routes(age=self.age, include_historical_traffic=False)
            
        self.possible_combinations = self.event_data.get_possible_combinations(min_length=int(self.filter_eventamount.get()))   
        self.ranking_data = self.event_data.get_ranking()
        
        self.ranking_data_hp = self.ranking_data[self.ranking_data['combination'].str.contains(self.crime_idx)]
        self.ranking_data_hd = self.ranking_data[~self.ranking_data['combination'].str.contains(self.crime_idx)]
        
        hp_mean, hp_var = self.ranking_data_hp['probability'].mean(), self.ranking_data_hp['probability'].var()
        hd_mean, hd_var = self.ranking_data_hd['probability'].mean(), self.ranking_data_hd['probability'].var()
        
        self.route_combobox['values'] = ["".join(c) for c in self.possible_combinations]
        self.route_combobox.current(0)
        
        self.h_val_label.config(text=f"Hp: {hp_mean:.2f} ({hp_var:.2f}). Hd: {hd_mean:.2f} ({hd_var:.2f})")
        
        self.show_ranking_button['state'] = 'active'
        self.show_distribution_button['state'] = 'active'
        
        self.export_ranking_button['state'] = 'active'
        self.export_route_button['state'] = 'active'
        self.export_route_vis_button['state'] = 'active'
        self.export_plot_button['state'] = 'active'
        
    def run(self):
        self.root.mainloop()
        
class DataWidget():
    def __init__(self, data):
        self.data = list(data.itertuples(index=False, name=None))
        
        self.root = tk.Tk()
        self.window_width = 1000
        self.window_height = 500 
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        self.frame = tk.Frame()
        self.sheet = tksheet.Sheet(self.root, data = self.data,
                                   width=self.window_width, height=self.window_height)
        self.sheet.headers(data.columns)        
        self.sheet.row_index(data.index)
        self.sheet.grid(row=0, column=0, sticky="nswe")
    
    def show_data(self):
        self.root.mainloop()

if __name__ == '__main__':
    print("{0:.2f}".format(0.333333))
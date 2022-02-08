import tkinter as tk
from tkinter import filedialog
from Scripts.PopUpManager import *
from Scripts.FacultyAssigner import FacultyAssigner


class BuildGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.destination = None
        self.input_file = None
        self.input_entry = tk.Entry(self.window)
        self.destination_entry = tk.Entry(self.window)
        self.progress = tk.Label(self.window)

    def setup(self):
        self.create_window()
        self.configure_window()
        self.create_menu()
        self.set_label()
        self.create_entry()
        self.set_buttons()

    def mainloop(self):
        self.window.mainloop()

    def set_label(self):
        self.progress.grid(row=5, column=2, columnspan=2, sticky='nsew')
        self.progress.config(text='Start Assigning...')

    def create_window(self):
        self.window.title('Faculty Assigner')
        self.window.geometry('640x480+400+200')
        self.window['padx'] = 8
        self.window['pady'] = 8

    def configure_window(self):
        self.window.rowconfigure(0, weight=20)
        self.window.rowconfigure(1, weight=5)
        self.window.rowconfigure(2, weight=30)
        self.window.rowconfigure(3, weight=5)
        self.window.rowconfigure(4, weight=100)
        self.window.rowconfigure(5, weight=3)
        self.window.rowconfigure(6, weight=20)
        self.window.rowconfigure(7, weight=10)
        self.window.columnconfigure(0, weight=20)
        self.window.columnconfigure(1, weight=40)
        self.window.columnconfigure(2, weight=20)
        self.window.columnconfigure(3, weight=40)
        self.window.columnconfigure(4, weight=40)
        self.window.columnconfigure(5, weight=20)

    def create_menu(self):
        def destroy():
            self.window.destroy()

        def open_about():
            about_us_popup(self.window)

        menu = tk.Menu(self.window)

        file_menu = tk.Menu(self.window, tearoff=0)
        file_menu.add_command(label='New Source', command=self.open_source)
        file_menu.add_command(label='New Destination', command=self.choose_destination)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=destroy)

        help_menu = tk.Menu(self.window, tearoff=0)
        help_menu.add_command(label='How To Use')
        help_menu.add_command(label='About', command=open_about)

        menu.add_cascade(label='File', menu=file_menu)
        menu.add_cascade(label='Help', menu=help_menu)
        menu.add_command(label='Exit', command=destroy)

        self.window.config(menu=menu)

    def open_source(self):
        self.input_file = filedialog.askopenfilename()
        text = tk.StringVar()
        text.set(self.input_file)
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, text.get())

    def choose_destination(self):
        self.destination = filedialog.askdirectory()
        text = tk.StringVar()
        text.set(self.destination)
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, text.get())

    def create_entry(self):
        self.input_entry.grid(row=1, column=3, columnspan=2, rowspan=1, sticky='nsew')
        self.destination_entry.grid(row=3, column=3, columnspan=2, rowspan=1, sticky='nsew')

    def set_buttons(self):
        input_btn = tk.Button(self.window, text='Input', command=self.open_source)
        destination_btn = tk.Button(self.window, text='Destination', command=self.choose_destination)
        input_btn.grid(row=1, column=1, sticky='nsew')
        destination_btn.grid(row=3, column=1, sticky='nsew')

        calculate_btn = tk.Button(self.window, text='Calculate', command=self.calculate)
        calculate_btn.grid(row=6, column=1, columnspan=4, sticky='nsew')

    def done(self):
        self.destination_entry.delete(0, tk.END)
        self.input_entry.delete(0, tk.END)
        self.progress.config(text='Assignment Done!')

    def calculate(self):
        if self.destination is None:
            error_popup(self.window, 'Save Destination not selected')
        elif self.input_file is None:
            error_popup(self.window, 'Input File not selected')
        else:
            self.progress.config(text='Processing')
            run = FacultyAssigner(self.input_file, self.destination, self.window, self.done)
            run.runner()

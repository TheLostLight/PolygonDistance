import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import MyPolygon
import GeneratePolygon
import ReadFile as ReadPolygon
from MyCollision import findSunnyDistance
from DrawDiagram import makeFile

class PolygonGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Create Polygon-Line Diagrams")
        self.main_frame = MainFrame(self)
        self.current_frame = self.main_frame
        self.gen_frame = GenerationFrame(self)
        self.res_frame = ResultsFrame(self)
        self.current_frame.pack()

    def switchToTargetFrame(self, target_frame):
        self.current_frame.pack_forget()
        target_frame.pack()
        self.current_frame = target_frame

    def loadResults(self):

        with filedialog.askopenfile() as open_file:
            try:
                data = ReadPolygon.readPolygonFile(open_file)
            except RuntimeError:
                messagebox.showerror(title="Error reading polygon!", message="There was an error parsing file. Check format...")
                return
        
        self.switchToTargetFrame(self.res_frame)
        polygon = MyPolygon.Polygon(data[0])
        self.res_frame.result_set = (polygon, data[1], findSunnyDistance(polygon, data[1]))
        self.res_frame.status.set('Completed!')
        self.res_frame.switchButtons(tk.NORMAL)


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        tk.Button(self, text="Generate Polygon", command=lambda: master.switchToTargetFrame(master.gen_frame)).pack()
        tk.Button(self, text="Load File", command=master.loadResults).pack()
        tk.Button(self, text="Exit", command=quit).pack()

class GenerationFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        num_vcmd = self.register(self.checkDigit)
        bounds_frame = tk.Frame(self)
        bounds_frame.pack()
        tk.Label(bounds_frame, text="Min X Value (recommended 500):").grid(row = 0)
        tk.Label(bounds_frame, text="Max X Value (recommended 1500):").grid(row = 0, column = 1)
        self.min_x = tk.StringVar()
        self.min_x.set('500')
        min_x_entry = tk.Entry(bounds_frame, validate='key', validatecommand=(num_vcmd, '%S'), textvariable=self.min_x)
        min_x_entry.grid(row = 1, column = 0)
        self.max_x = tk.StringVar()
        self.max_x.set('1500')
        max_x_entry = tk.Entry(bounds_frame, validate='key', validatecommand=(num_vcmd, '%S'), textvariable=self.max_x)
        max_x_entry.grid(row = 1, column = 1)
        tk.Label(bounds_frame, text="Min Y Value (recommended 500):").grid(row = 2, column = 0)
        tk.Label(bounds_frame, text="Max Y Value (recommended 1500):").grid(row = 2, column = 1)
        self.min_y = tk.StringVar()
        self.min_y.set('500')
        min_x_entry = tk.Entry(bounds_frame, validate='key', validatecommand=(num_vcmd, '%S'), textvariable=self.min_y)
        min_x_entry.grid(row = 3, column = 0)
        self.max_y = tk.StringVar()
        self.max_y.set('1500')
        max_x_entry = tk.Entry(bounds_frame, validate='key', validatecommand=(num_vcmd, '%S'), textvariable=self.max_y)
        max_x_entry.grid(row = 3, column = 1)

        verts_frame = tk.Frame(self)
        verts_frame.pack()

        tk.Label(verts_frame, text="# of vertices:").pack(side=tk.LEFT)
        n_vertices = tk.StringVar()
        tk.Entry(verts_frame, validate='key', validatecommand=(num_vcmd, '%S'), textvariable=n_vertices).pack()
        

        b_frame = tk.Frame(self)
        b_frame.pack()
        self.gen_button = tk.Button(b_frame, text="Save to File", command=self.saveGeneration)
        self.gen_button['state'] = tk.DISABLED
        self.gen_button.pack()
        tk.Button(b_frame, text='return', command=lambda: master.switchToTargetFrame(master.main_frame)).pack()

        self.arguments = (n_vertices, self.min_x, self.max_x, self.min_y, self.max_y)

        for var in self.arguments:
            var.trace_add("write", self.validateEntry)


    def checkDigit(self, entry):
        return entry.isdigit()

    def validateEntry(self, *args):
        for val in self.arguments:
            if len(val.get()) < 1:
                self.gen_button['state'] = tk.DISABLED
                return

        self.gen_button['state'] = tk.NORMAL

    def saveGeneration(self):
        bounds = (int(self.arguments[1].get()), int(self.arguments[2].get()), int(self.arguments[3].get()), int(self.arguments[4].get()))
        with filedialog.asksaveasfile(parent=self, initialdir=os.getcwd()) as open_file:
            try:
                GeneratePolygon.printRandomPolygonToFile(open_file, int(self.arguments[0].get()), bounds)
            except RuntimeError:
                messagebox.showerror(title="Generation Error!", message="There was an error generating the polygon...")

class ResultsFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.master = master
        self.result_set = None

        self.status = tk.StringVar()
        self.status.set("Computing...")

        tk.Label(self, textvariable=self.status).pack()

        b_frame = tk.Frame(self)
        b_frame.pack()

        show_button = tk.Button(b_frame, text="Show Diagram", command=self.showResults)
        show_button.pack(side=tk.LEFT)
        save_button = tk.Button(b_frame, text="Save to PNG", command=self.saveResults)
        save_button.pack(side=tk.LEFT)
        tk.Button(b_frame, text="Return", command=self.returnToMain).pack(side=tk.LEFT)

        self.button_gates = [show_button, save_button]

        self.switchButtons(tk.DISABLED)

    def returnToMain(self):
        self.switchButtons(tk.DISABLED)
        self.master.switchToTargetFrame(self.master.main_frame)
        self.status.set('Calculating...')

    def switchButtons(self, b_state):
        for b in self.button_gates:
            b['state'] = b_state

    def showResults(self):
        makeFile(*self.result_set)

    def saveResults(self):
        file_path = filedialog.asksaveasfilename()

        if not file_path.endswith(('.png', '.PNG')):
            file_path += '.png'

        makeFile(*self.result_set, file_path=file_path)
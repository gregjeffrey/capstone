import tkinter as tk
from tkinter import ttk
import dbConnect
import pymysql
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import datetime
from PIL import Image, ImageTk

class gui:
    def __init__(self, master):
        self.master = master
        master.title("GOATS GUI")

        self.winHeight = 600
        self.winWidth = 1200
        master.geometry(str(self.winWidth) + 'x' + str(self.winHeight))

        self.cursor = dbConnect.connect().cursor()

        self.colors = colors = ["#2EF004", "#5DEF03", "#8AEE03", "#B8ED02",
            "#E5EB02", "#EAC201", "#E99301", "#E76500", "#E63600", "#E50800"]

        self.imageLoc = "testImages/hl_plants_20171117.jpg"
        self.graphLoc = "1"

        self.tabs = self.form_notebook()

        self.grid_db_data()
        refOne = tk.Button(self.tabs[0], text="Refresh", command=self.refreshOne)
        refOne.place(relx=.9, rely=.9)

        self.draw_graph()
        refTwo = tk.Button(self.tabs[1], text="Refresh", command=self.refreshTwo)
        refTwo.place(relx=.9, rely=.9)

        self.draw_image()
        refThree = tk.Button(self.tabs[2], text="Refresh", command=self.refreshThree)
        refThree.place(relx=.9, rely=.9)


    def form_notebook(self):
        tabControl = ttk.Notebook(self.master)

        tab1 = ttk.Frame(tabControl, width=self.winWidth, height=self.winHeight)
        tabControl.grid(row=0, column=0, sticky="ew")
        tabControl.add(tab1, text='Grid')

        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Line Graphs')

        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Image Request')

        return[tab1, tab2, tab3]

    def grid_db_data(self):
        #get grid data
        self.cursor.execute('call get_grid_info()')
        info = self.cursor.fetchall()

        # parse db data into useable grid data
        width = 0
        height = 0
        maxChar = 0
        names = {}
        for row in info:
            if row["x_coord"] + 1 > width:
                width = row["x_coord"] + 1
            if row["y_coord"] + 1 > height:
                height = row["y_coord"] + 1
            ind = str(row["x_coord"]) + "," + str(row["y_coord"])
            names[ind] = {}
            names[ind]["plant"] = row["plant_type"]
            if len(names[ind]["plant"]) > maxChar:
                maxChar = len(names[ind]["plant"])
            names[ind]["bg"] =  self.colors[int(row["health_change"] /
                len(self.colors))]

        #help calculate cnter-formatting for grid
        midx = float(width-1.0)/2.0
        midy = float(height-1.0)/2.0

        for i in range(height):
            for j in range(width):
                ind = str(i)+ "," + str(j)
                if ind in names:
                    b = tk.Label(self.tabs[0], text=names[ind]["plant"],
                        bg=names[ind]["bg"], relief="solid", width=maxChar)
                    b.grid(row=i, column=j)
                    relationx =  (j-midx)*.1+.5
                    relationy =  (i-midy)*.075+.5
                    b.place(relx=relationx, rely=relationy, anchor="c")

    def get_measurements(self):
        self.cursor.execute('call get_ndvi_over_time(' + str(self.graphLoc) + ')')
        info = self.cursor.fetchall()
        times = []
        vals = []
        for measurement in info:
            t = measurement['tstamp']
            times.append(t)
            vals.append(measurement['ndvi_val'])
        return [times, vals]

    def draw_graph(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        data = self.get_measurements()
        a.plot(data[0], data[1])

        canvas = FigureCanvasTkAgg(f, self.tabs[1])
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self.tabs[1])
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_image(self):
        if self.imageLoc is not None:
            pil_img = Image.open(self.imageLoc)
            self.img = ImageTk.PhotoImage(pil_img)
            l = tk.Label(self.tabs[2], image=self.img)
            l.grid(row=1, column=1)

    def refreshOne(self):
        self.tabs[0].grid_forget()
        self.grid_db_data()
        return 1

    def refreshTwo(self):
        self.tabs[1].grid_forget()
        self.draw_graph()
        return 1

    def refreshThree(self):
        self.tabs[2].grid_forget()
        self.draw_image()
        return 1

root = tk.Tk()
my_gui = gui(root)
root.mainloop()


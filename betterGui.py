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
        self.w, self.h = self.master.winfo_screenwidth()-100, self.master.winfo_screenheight()-100
        self.master.geometry("%dx%d+0+0" % (self.w, self.h))
        self.master.state("zoomed")


        self.cursor = dbConnect.connect().cursor()

        self.colors = colors = ["#2EF004", "#5DEF03", "#8AEE03", "#B8ED02",
            "#E5EB02", "#EAC201", "#E99301", "#E76500", "#E63600", "#E50800"]

        self.imageLoc = None
        self.imageLocationOptions = self.setLocations()
        self.imageMeasurementOptions = ["None"]
        self.imageLabel = None
        self.imagesFromMeasurements= {"None": None}
        self.graphDataOptions = ["Health", "Insects"]
        self.graphDataLocations = self.setLocations()[1:]
        self.graphLoc = self.graphDataLocations[0]
        self.graphType = self.graphDataOptions[0]
        self.data = [[],[]]
        self.graphCanvas = None
        self.graph_toolbar = None
        self.figure = None
        self.ax = None

        self.tabs = self.form_notebook()

        self.grid_db_data()
        self.refOne = tk.Button(self.tabs[0], text="Refresh", command=self.refreshOne)
        self.refOne.place(relx=.9, rely=.9)

        self.draw_graph()
        self.refTwo = tk.Button(self.tabs[1], text="Refresh", command=self.refreshTwo)
        self.refTwo.place(relx=.9, rely=.9)

        self.graphDataMenu = ttk.Combobox(self.tabs[1], values=self.graphDataOptions, state="readonly")
        self.graphDataMenu.current(0)
        self.graphDataMenu.pack()

        self.graphDataMenuLocation = ttk.Combobox(self.tabs[1], values=self.graphDataLocations, state="readonly")
        self.graphDataMenuLocation.current(0)
        self.graphDataMenuLocation.pack()

        self.subTwo = tk.Button(self.tabs[1], text="Submit", command=self.update_graph)
        self.subTwo.pack()

        self.draw_image()
        self.refThree = tk.Button(self.tabs[2], text="Refresh", command=self.refreshThree)
        self.refThree.place(relx=.9, rely=.9)

        self.imageLocationOptionMenu = ttk.Combobox(self.tabs[2], values=self.imageLocationOptions, state="readonly")
        self.imageLocationOptionMenu.current(0)
        self.imageLocationOptionMenu.grid(row=2, column=1)
        self.subThree = tk.Button(self.tabs[2], text="Submit", command=self.resetImageLocationOptions)
        self.subThree.place(y=25)

        self.imageMeasurementOptionMenu = ttk.Combobox(self.tabs[2], values=self.imageMeasurementOptions, state="disabled")
        self.imageMeasurementOptionMenu.current(0)
        self.imageMeasurementOptionMenu.grid(row=2, column=1)
        self.imageMeasurementOptionMenu.place(y=50)
        self.subThreeTwo = tk.Button(self.tabs[2], text="Submit", command=self.resetImageMeasurementOptions)
        self.subThreeTwo.place(y=75)
        self.subThreeTwo.config(state='disabled')


    def form_notebook(self):
        tabControl = ttk.Notebook(self.master)

        tab1 = ttk.Frame(tabControl, width=self.w, height=self.h)
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
        self.cursor.execute('call get_graph_data(' + str(self.graphLoc) + ')')
        info = self.cursor.fetchall()
        times = []
        vals = []
        for measurement in info:
            t = measurement['tstamp']
            times.append(t)
            if self.graphType == "Health":
                vals.append(measurement['ndvi_val'])
            else:
                vals.append(measurement['insects_present'])
        return [times, vals]

    def draw_graph(self):
        self.figure = Figure(figsize=(5,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.data = self.get_measurements()
        self.ax.plot(self.data[0], self.data[1])

        self.graphCanvas = FigureCanvasTkAgg(self.figure, self.tabs[1])
        self.graphCanvas.show()
        self.graphCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.graph_toolbar = NavigationToolbar2TkAgg(self.graphCanvas, self.tabs[1])
        self.graph_toolbar.update()
        self.graphCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graph(self):
        self.graphLoc = self.graphDataMenuLocation.get()
        self.graphType = self.graphDataMenu.get()
        self.data = self.get_measurements()
        self.ax.clear()
        self.ax.plot(self.data[0], self.data[1])
        self.graphCanvas.draw()

    def setLocations(self):
        ops = ["None"]
        self.cursor.execute("call get_locations()")
        for loc in self.cursor.fetchall():
            ops.append(str(loc["location_no"]))
        return ops

    def setImageMeasurementOptions(self):
        ops = ["None"]
        images = {"None": None}
        if not(str(self.imageLocationOptionMenu.get())) == "None":
            self.cursor.execute("call get_images(" + str(self.imageLocationOptionMenu.get()) + ")")
            for loc in self.cursor.fetchall():
                ops.append(loc["tstamp"].strftime("%Y-%m-%d %H:%M:%S"))
                images[ops[-1]] = loc["image"]
        return ops, images

    def draw_image(self):
        if self.imageLoc is not None:
            pil_img = Image.open(self.imageLoc)
            self.img = ImageTk.PhotoImage(pil_img)
            self.imageLabel = tk.Label(self.tabs[2], image=self.img)
            self.imageLabel.grid(row=1, column=1)
            self.imageLabel.place(x=((self.w)/2 - (self.img.width())/2), y=((self.h)/2 - (self.img.height())/2))


    def resetImageLocationOptions(self):
        self.imageLoc = self.getImageLoc()
        self.imageMeasurementOptions, self.imagesFromMeasurements = self.setImageMeasurementOptions()
        self.imageMeasurementOptionMenu.config(values=self.imageMeasurementOptions)
        self.imageMeasurementOptionMenu.current(0)
        if len(self.imageMeasurementOptions) > 1:
            self.imageMeasurementOptionMenu.config(state='readonly')
            self.subThreeTwo.config(state='normal')
        else:
            self.imageMeasurementOptionMenu.config(state='disabled')
            self.subThreeTwo.config(state='disabled')
        self.refreshThree()

    def resetImageMeasurementOptions(self):
        self.imageLoc = self.getImageLocFromMeasurement()
        self.refreshThree()

    def getImageLoc(self):
        locNo = self.imageLocationOptionMenu.get()
        if not(locNo == "None"):
            self.cursor.execute("call get_last_saved_pic(" + str(locNo) + ")")
            return self.cursor.fetchall()[0]["last_pic_saved"]
        return None

    def getImageLocFromMeasurement(self):
        tstamp = self.imageMeasurementOptionMenu.get()
        return self.imagesFromMeasurements[tstamp]


    def refreshOne(self):
        self.tabs[0].grid_forget()
        self.grid_db_data()
        return 1

    def refreshTwo(self):
        self.update_graph()

    def refreshThree(self):
        self.tabs[2].grid_forget()
        if self.imageLabel is not None:
            self.imageLabel.destroy()
            self.imageLabel = None
        self.draw_image()
        return 1

root = tk.Tk()
my_gui = gui(root)
root.mainloop()


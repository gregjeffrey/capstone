#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Matt
#
# Created:     29/01/2018
# Copyright:   (c) Matt 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import dbConnect
import pymysql

def connect_db(hostname, username, password ,database, charset, cursorType):
    return dbConnect.connect(hostname=hostname, username=username,
        password=password, database=database, charset = charset,
        cursorType = cursorType)

def grid_db_data(cursor, gradientColors, frame):
    #get grid data
    cursor.execute('call get_grid_info()')
    info = cursor.fetchall()

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
        names[ind]["bg"] =  gradientColors[int(row["health_change"] /
            len(gradientColors))]

    #help calculate cnter-formatting for grid
    midx = float(width-1.0)/2.0
    midy = float(height-1.0)/2.0

    for i in range(height):
        for j in range(width):
            ind = str(i)+ "," + str(j)
            if ind in names:
                b = tk.Label(frame, text=names[ind]["plant"],
                    bg=names[ind]["bg"], relief="solid", width=maxChar)
                b.grid(row=i, column=j)
                relationx =  (j-midx)*.1+.5
                relationy =  (i-midy)*.075+.5
                b.place(relx=relationx, rely=relationy, anchor="c")

def get_measurements(cursor, location_id):
    return 1

def main():
    #***************************************
    #variables that can change
    hostname="162.241.217.12"
    username="nuinstig_goat"
    password="kzzgBq_o]uVF"
    database="nuinstig_goats"
    charset = "utf8mb4"
    cursorType = pymysql.cursors.DictCursor
    colors = ["#2EF004", "#5DEF03", "#8AEE03", "#B8ED02", "#E5EB02", "#EAC201",
        "#E99301", "#E76500", "#E63600", "#E50800"]
    winHeight = 400
    winWidth = 800
    #****************************************
    #start the GUI
    win = tk.Tk()
    win.title("GOATS GUI")
    win.geometry(str(winWidth) + 'x' + str(winHeight))
    tabControl = ttk.Notebook(win)
    tab1 = ttk.Frame(tabControl, width=winWidth, height=winHeight)
    tabControl.grid(row=0, column=0, sticky="ew")
    tabControl.add(tab1, text='Grid')
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text='Line Graphs')
    tab3 = ttk.Frame(tabControl)
    tabControl.add(tab3, text='Image Request')
    cursor = connect_db(hostname, username, password, database, charset, cursorType)
    grid_db_data(cursor, colors, tab1)


    win.mainloop()

main()
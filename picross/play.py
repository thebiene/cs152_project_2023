#program to initialize a picross drawing window
import tkinter as tk
from tkinter import filedialog
import variables as var
from picross import PicWindow
import os

def start(): #create TK window to get inputs for a picross window

  def choose_file(): #opens a file explorer to select a picross file
    filename = tk.filedialog.askopenfilename(initialdir=os.getcwd(),title = "Select a File",
                filetypes = (("text files","*.txt"), ("all files","*.*")))
    print(filename)
    play_from_save(filename)

  def play_new(): #opens a blank picross window, size determined by the scales
    array = [ [ 0 for width_ in range(col_scale.get()) ] for height_ in range(row_scale.get()) ]
    picross = PicWindow(row_scale.get(), col_scale.get(), array, resolution)
    root.destroy()
    picross.play()

  def play_from_save(filename): #opens input file as a picross window
    f = open(filename, "r")
    rows = []
    finished = False
    i = 0
    while not finished:
      new_line = f.readline()
      if new_line.strip() == '':
        finished = True
      else:
        i += 1
        print(i, new_line)
        rows.append(new_line)
    array = [ [ 0 if x == '0' else 1 for x in line.strip() ] for line in rows ]
    picross = PicWindow(len(array), len(array[0]), array, resolution)
    root.destroy()
    picross.play()

  root = tk.Tk()
  resolution = [root.winfo_screenwidth(), root.winfo_screenheight()]
  root.winfo_toplevel().title("PICROSS")
  frame = tk.Frame()
  frame.pack(padx=50, pady=50)
  header = tk.Label(frame, text='Select grid size', font=('TkDefaultFont', 26))
  header.pack(pady=(0,26))
  row_scale = tk.Scale(frame, relief=tk.FLAT, label='number of rows:', from_=5, to=var.max_grid_count, orient='horizontal', length=(800), tickinterval=5, font=('TkDefaultFont', 16))
  row_scale.pack(pady=(0,50))
  col_scale = tk.Scale(frame, relief=tk.FLAT, label='number of columns:',  from_=5, to=var.max_grid_count, orient='horizontal', length=(800), tickinterval=5, font=('TkDefaultFont', 16))
  col_scale.pack(pady=(0,50))
  b = tk.Button(frame, text="create empty grid", font=('TkDefaultFont', 26), padx=20, pady=10, command=play_new)
  b.pack()
  b2 = tk.Button(frame, text="choose grid from files", font=('TkDefaultFont', 26), padx=20, pady=10, command=choose_file)
  b2.pack()
  root.mainloop()



if __name__ == "__main__":
  start()
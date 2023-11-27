#makes a window to draw in a picross grid
import tkinter as tk
import variables as var
from PIL import ImageGrab
offset = 20


class PicWindow:

  def __init__(self, rows, cols, array): #initial variables
    self.rows = rows
    self.cols = cols
    self.array = array
    self.boxes = [ [ None for j in row ] for row in array ]
    self.sqrw = min(1000//max(rows,cols), 100)
    self.winw = self.sqrw*cols+offset*2
    self.winh = self.sqrw*rows+offset*2
  
  def play(self): #creates window/starts the program
    self.win = tk.Tk()
    self.create_window()
    self.win.mainloop()

  def create_window(self): #creates the TK window and its widgets
    self.win.winfo_toplevel().title("PICROSS")
    self.win.resizable(False,False)
    self.canv = tk.Canvas(self.win, height=self.winh, width=self.winw)
    self.filename = tk.StringVar()
    textentry = tk.Entry(self.win, textvariable = self.filename)
    savebutton = tk.Button(self.win, text="SAVE", font=('TkDefaultFont', 16), padx=20, pady=10, command=self.save)
    self.canv.pack()
    textentry.pack(pady=(0,offset),padx=offset,side="right")
    savebutton.pack(side='right')
    self.create_grid()

  def create_grid(self): #creates the interactive picross grid
    for vi in range(self.rows):
      for hi in range(self.cols):
        color = var.empty if self.array[vi][hi] == 0 else var.fill
        x1, y1 = hi*self.sqrw+offset, vi*self.sqrw+offset
        x2, y2 = x1+self.sqrw, y1+self.sqrw
        box = self.canv.create_rectangle(x1, y1, x2, y2, fill=color)
        self.boxes[vi][hi] = box
        self.canv.tag_bind(box, "<Button-1>", lambda _, z=(vi, hi): self.button_1(z))
        self.canv.tag_bind(box, "<Button-3>", lambda _, z=(vi, hi): self.button_3(z))
        # canvas.tag_bind(box, "<B1-Motion>", lambda event, z=box: drag_action(event, z))
    for vi in range(self.rows):
      for hi in range(self.cols):
        if vi%5==0 and hi%5==0:
          x1, y1 = hi*self.sqrw+offset, vi*self.sqrw+offset
          x2, y2 = self.sqrw*min(hi+5, self.cols)+offset, self.sqrw*min(vi+5, self.rows)+offset
          outline = self.canv.create_rectangle(x1, y1, x2, y2, width=3)
          print(x1, y1, x2, y2)

  def save(self): #saves current drawing as a txt file
    filename = self.filename.get().strip(' ')
    if filename != '':
      #save file as filename
      print('save as', filename)
      f = open(f"{filename}.txt", "w")#create new file, overwrite if filename exists
      for row in self.array:
        for item in row:
          f.write(str(item))
        f.write('\n')
      f.write('\n')

  def button_1(self, z): #left mouse button, toggles square color to filled
    x, y = z[0], z[1]
    box = self.boxes[x][y]
    color = self.canv.itemcget(box, "fill")
    if color == var.fill:
      self.canv.itemconfig(box, fill=var.empty)
      self.array[x][y] = 0
    else:
      self.canv.itemconfig(box, fill=var.fill)
      self.array[x][y] = 1
    print(x, y, self.array[x][y])
  
  def button_3(self, z): #right mouse button, toggles square color to crossed out
    x, y = z[0], z[1]
    box = self.boxes[x][y]
    color = self.canv.itemcget(box, "fill")
    if color == var.checked:
      self.canv.itemconfig(box, fill=var.empty)
      self.array[x][y] = 0
    else:
      self.canv.itemconfig(box, fill=var.checked)
      self.array[x][y] = 0
    print(x, y, self.array[x][y])


if __name__ == "__main__": #if this program is run on its own it will default to an empty 15x15 grid.
  picross = PicWindow(15, 15, [ [ 0 for i in range(15) ] for j in range(15) ])
  picross.play()

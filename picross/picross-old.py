#makes a window to draw in a picross grid
import tkinter as tk
import variables as var
offset = var.offset
# max_window_width=80%of_screenwidth
# min_square_width=5% of screenwidth

class PicWindow:

  def __init__(self, rows, cols, array, resolution): #initial variables
    self.rows = rows
    self.cols = cols
    self.array = array
    self.boxes = [ [ None for j in row ] for row in array ]
    self.scrw, self.scrh = resolution[0], resolution[1]
    default_sqrw = min(self.scrw, self.scrh)//20
    max_sqrw = min((self.scrw//10*8)//cols,(self.scrh//10*8)//rows)
    self.sqrw = min(max_sqrw, default_sqrw)
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
    displaybutton = tk.Button(self.win, text="DISPLAY", font=('TkDefaultFont', 16), padx=20, pady=10, command=self.puzzle_window)
    self.canv.pack()
    textentry.pack(pady=(0,offset),padx=offset,side="right")
    savebutton.pack(side='right')
    displaybutton.pack(side='left',padx=offset)
    self.create_grid()

  def number_sets(self): #creates the sets of numbers that will be displayed for each row and col in the final puzzle (in string format)
    row_sets=[]
    col_sets=[]
    for i in range(len(self.array)):
      l=[]
      current=0
      for j in range(len(self.array[i])):
          if self.array[i][j] == 1:
            current+=1
          else:
            if current !=0:
              l.append(current)
              current=0
      if current !=0:
        l.append(current)
      row_sets.append(l)
    for j in range(len(self.array[0])):
      l=[]
      current=0
      for i in range(len(self.array)):
        if self.array[i][j] == 1:
            current+=1
        else:
          if current !=0:
            l.append(current)
            current=0
      if current !=0:
        l.append(current)
      col_sets.append(l)
    row_str=[]
    for item in range(len(row_sets)):
      i=str(row_sets[item])
      i=i.replace('[','')
      i=i.replace(']','')
      i=i.replace(',','')
      row_str.append(i)
    col_str=[]
    for item in range(len(col_sets)):
      i=str(col_sets[item])
      i=i.replace('[','')
      i=i.replace(']','')
      i=i.replace(',','\n')
      i=i.replace(' ','')
      col_str.append(i)
    return(row_str, col_str)

  def puzzle_window(self): # should create a new window with playable/printable puzzle
    # next: automatic printing?
    # next: with very large # row/col it gets fucked up, numbers out of boxes, spacing all weird, idk
    row_str, col_str=PicWindow.number_sets(self)
    row_div=2.5
    col_div=2.5

    max_row=len(max(row_str, key=len))
    max_col=len(max(col_str, key=len))
    row_room=max(self.sqrw,round(max_row*self.sqrw/row_div))
    col_room=max(self.sqrw,round(max_col*self.sqrw/col_div))

    self.window=tk.Toplevel(self.win)
    self.window.resizable(False,False)
    disp_sqrw=self.sqrw
    if self.winh+col_room+offset*2 <= self.scrh*9/10 and self.winw+row_room+offset*2 <= self.scrw*9/10:
      self.puzzle=tk.Canvas(self.window, height=self.winh+col_room+offset*2, width=self.winw+row_room+offset*2)
    else:
      while(disp_sqrw*self.rows+col_room+offset*2 >= self.scrh*8.5/10 or disp_sqrw*self.cols+row_room+offset*2 >= self.scrw*8.5/10):
        disp_sqrw -=1
        row_room=max(disp_sqrw,round((max_row+1)*disp_sqrw/row_div))
        col_room=max(disp_sqrw,round((max_col+1)*disp_sqrw/col_div))

      self.puzzle=tk.Canvas(self.window, height=round(disp_sqrw*self.rows+col_room+offset*2), width=round(disp_sqrw*self.cols+row_room+offset*2))

    font_size=round(disp_sqrw/2)
    
    # original grid
    for vi in range(self.rows):
      for hi in range(self.cols):
        #color = var.empty if self.array[vi][hi] == 0 else var.fill
        x1, y1 = hi*disp_sqrw+offset+row_room, vi*disp_sqrw+offset+col_room
        x2, y2 = x1+disp_sqrw, y1+disp_sqrw
        box = self.puzzle.create_rectangle(x1, y1, x2, y2)#, fill=color)
        self.boxes[vi][hi] = box
    for vi in range(self.rows):
      for hi in range(self.cols):
        if vi%5==0 and hi%5==0:
          x1, y1 = hi*disp_sqrw+offset+row_room, vi*disp_sqrw+offset+col_room
          x2, y2 = disp_sqrw*min(hi+5, self.cols)+offset+row_room, disp_sqrw*min(vi+5, self.rows)+offset+col_room
          outline = self.puzzle.create_rectangle(x1, y1, x2, y2, width=3)
          outline_l = self.puzzle.create_rectangle(offset, y1, x1, y2, width=3)
          outline_t = self.puzzle.create_rectangle(x1, offset, x2, y1, width=3)
    # new grids/text
    for vi in range(self.rows):
      y1=vi*disp_sqrw+offset+col_room
      y2=y1+disp_sqrw
      nboxv = self.puzzle.create_rectangle(offset, y1, offset+row_room, y2)
    for vi in range(self.cols):
      x=vi*disp_sqrw+offset+row_room
      self.puzzle.create_text(x+disp_sqrw/2, offset*3/4+col_room, text=col_str[vi], font=("Courier",font_size), anchor='s')
    for hi in range(self.cols):
      x1=hi*disp_sqrw+offset+row_room
      x2=x1+disp_sqrw
      nboxh = self.puzzle.create_rectangle(x1, offset, x2, offset+col_room)
    for hi in range(self.rows):
      y=hi*disp_sqrw+offset+col_room
      self.puzzle.create_text(offset*3/4+row_room, y+disp_sqrw/2, text=row_str[hi], font=("Courier",font_size), anchor='e')
    self.puzzle.pack()


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
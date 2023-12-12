#makes a window to draw in a picross grid
import tkinter as tk
import variables as var
from PIL import ImageGrab
offset = var.offset

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
    self.mouse_color = None
  
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
    
  def create_grid(self): #creates the interactive picross grid
    for vi in range(self.rows):
      for hi in range(self.cols):
        color = var.empty if self.array[vi][hi] == 0 else var.fill
        x1, y1 = hi*self.sqrw+offset, vi*self.sqrw+offset
        x2, y2 = x1+self.sqrw, y1+self.sqrw
        box = self.canv.create_rectangle(x1, y1, x2, y2, fill=color)
        self.boxes[vi][hi] = box
        self.canv.tag_bind(box, "<Button-1>", lambda _, z=(hi, vi): self.button_1(z))
        self.canv.tag_bind(box, "<B1-Motion>", self.button_1_drag)
        self.canv.tag_bind(box, "<Button-3>", lambda _, z=(hi, vi): self.button_3(z))
        self.canv.tag_bind(box, "<B3-Motion>", self.button_3_drag)
        # canvas.tag_bind(box, "<B1-Motion>", lambda event, z=box: drag_action(event, z))
    for vi in range(self.rows):
      for hi in range(self.cols):
        if vi%5==0 and hi%5==0:
          x1, y1 = hi*self.sqrw+offset, vi*self.sqrw+offset
          x2, y2 = self.sqrw*min(hi+5, self.cols)+offset, self.sqrw*min(vi+5, self.rows)+offset
          outline = self.canv.create_rectangle(x1, y1, x2, y2, width=3)

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
    box = self.boxes[y][x]
    color = self.canv.itemcget(box, "fill")
    if color == var.fill:
      self.canv.itemconfig(box, fill=var.empty)
      self.array[y][x] = 0
      self.mouse_color = var.empty
    else:
      self.canv.itemconfig(box, fill=var.fill)
      self.array[y][x] = 1
      self.mouse_color = var.fill
  
  def button_1_drag(self, event):
    if event.x > offset and event.y > offset and event.y < self.sqrw*self.rows+offset and event.x < self.sqrw*self.cols+offset:
      x, y = (event.x-offset)//self.sqrw, (event.y-offset)//self.sqrw
      box = self.boxes[y][x]
      self.canv.itemconfig(box, fill=self.mouse_color)
      self.array[y][x] = 0 if (self.mouse_color == var.empty) else 1
  
  def button_3(self, z): #right mouse button, toggles square color to crossed out
    x, y = z[0], z[1]
    box = self.boxes[y][x]
    color = self.canv.itemcget(box, "fill")
    if color == var.checked:
      self.canv.itemconfig(box, fill=var.empty)
      self.array[y][x] = 0
      self.mouse_color = var.empty
    else:
      self.canv.itemconfig(box, fill=var.checked)
      self.array[y][x] = 0
      self.mouse_color = var.checked

  def button_3_drag(self, event):
    if event.x > offset and event.y > offset and event.y < self.sqrw*self.rows+offset and event.x < self.sqrw*self.cols+offset:
      x, y = (event.x-offset)//self.sqrw, (event.y-offset)//self.sqrw
      box = self.boxes[y][x]
      self.canv.itemconfig(box, fill=self.mouse_color)
      self.array[y][x] = 0

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
      if len(l) == 0:
        l.append(0)
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
      if len(l) == 0:
        l.append(0)
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

  def puzzle_window(self): #creates a new window with printable puzzle
    room_n = 1.3
    row_str, col_str = self.number_sets()
    max_row, max_col = 0, 0
    font_size = self.sqrw//3
    for i in row_str:
      x = i.replace(" ", "").replace("\n", "")
      max_row = max(max_row,len(x))
    for i in col_str:
      x = i.replace(" ", "").replace("\n", "")
      max_col = max(max_col,len(x))
    row_room = max(self.sqrw, (self.sqrw//room_n)*(max_row-1))
    col_room = max(self.sqrw, (self.sqrw//room_n)*(max_col-1))
    #w, h = offset*2 + row_room + self.sqrw*self.cols, offset*2 + col_room + self.sqrw*self.rows
    self.window=tk.Toplevel(self.win)
    #self.window.geometry(f"{int(w)}x{int(h)}")
    self.window.resizable(False,False)
    disp_sqrw=self.sqrw
    if self.winh+col_room+offset*2 <= self.scrh*9/10 and self.winw+row_room+offset*2 <= self.scrw*9/10:
      w, h = offset*2 + row_room + disp_sqrw*self.cols, offset*2 + col_room + disp_sqrw*self.rows
      self.puzzle=tk.Canvas(self.window, height=h, width=w, background='white')
    else:
      while(disp_sqrw*self.rows+col_room+offset*2 >= self.scrh*8.5/10 or disp_sqrw*self.cols+row_room+offset*2 >= self.scrw*8.5/10):
        disp_sqrw -=1
        row_room=max(disp_sqrw,round((disp_sqrw//room_n)*(max_row-1)))
        col_room=max(disp_sqrw,round((disp_sqrw//room_n)*(max_col-1)))
      w, h = offset*2 + row_room + disp_sqrw*self.cols, offset*2 + col_room + disp_sqrw*self.rows
      self.puzzle=tk.Canvas(self.window, height=h, width=w, background='white')
    font_size=disp_sqrw//2
    self.puzzle=tk.Canvas(self.window, height=h, width=w, background='white')
    for vi in range(self.rows):
      for hi in range(self.cols):
        x1, y1 = hi*disp_sqrw+offset+row_room, vi*disp_sqrw+offset+col_room
        x2, y2 = x1+disp_sqrw, y1+disp_sqrw
        box = self.puzzle.create_rectangle(x1, y1, x2, y2)
    for vi in range(self.rows):
      for hi in range(self.cols):
        if vi%5==0 and hi%5==0:
          x1, y1 = hi*disp_sqrw+offset+row_room, vi*disp_sqrw+offset+col_room
          x2, y2 = disp_sqrw*min(hi+5, self.cols)+offset+row_room, disp_sqrw*min(vi+5, self.rows)+offset+col_room
          outline = self.puzzle.create_rectangle(x1, y1, x2, y2, width=3)
    for row in range(self.rows):
      x1, y1 = offset, offset+row*disp_sqrw+col_room
      x2,y2 = x1+row_room, y1+disp_sqrw
      nboxv = self.puzzle.create_rectangle(x1, y1, x2, y2)
      if row%5==0:
        y2 = min(row+5,self.rows)*disp_sqrw+offset+col_room
        outline = self.puzzle.create_rectangle(x1, y1, x2, y2, width=3)
    for col in range(self.cols):
      x, y = col*disp_sqrw+offset+row_room+disp_sqrw/2, offset+col_room/2
      self.puzzle.create_text(x, y, text=col_str[col], font=("Courier",font_size))
    for col in range(self.cols):
      x1,y1=offset+col*disp_sqrw+row_room, offset
      x2,y2 = x1+disp_sqrw, y1+col_room
      nboxh = self.puzzle.create_rectangle(x1, y1, x2, y2)
      if col%5==0:
        x2 = min(col+5,self.cols)*disp_sqrw+offset+row_room
        outline = self.puzzle.create_rectangle(x1, y1, x2, y2, width=3)
    for row in range(self.rows):
      x, y = offset+row_room/2, row*disp_sqrw+offset+col_room+disp_sqrw/2
      self.puzzle.create_text(x, y, text=row_str[row], font=("Courier",font_size))
    self.puzzle.pack()
    self.puzzle.bind('<Visibility>', self.save_puzzle_image())
  
  def save_puzzle_image(self):
    filename = self.filename.get().strip(' ')
    #self.puzzle_window()
    self.window.update_idletasks()
    x1, y1 = self.window.winfo_rootx(), self.window.winfo_rooty()
    x2, y2 = x1+self.window.winfo_width(), y1+self.window.winfo_height()
    print(self.window.geometry())
    print(x1, y1, x2, y2)
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    image.save(f"{filename}.jpg")


if __name__ == "__main__": #if this program is run on its own it will default to an empty 15x15 grid.
  picross = PicWindow(15, 15, [ [ 0 for i in range(15) ] for j in range(15) ], [1920,1080])
  picross.play()

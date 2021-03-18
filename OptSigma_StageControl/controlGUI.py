import tkinter as tk
import sys, os, time
import StageControl
import tkinter.font as tkFont
import threading
from functools import partial

class GUI:
    def __init__(self):
       self.setpos = 0

       root = tk.Tk()
       root.title('Stage Control')
       root.geometry('300x350')

       frame0 = tk.Frame(root, relief='groove')
       frame1 = tk.Frame(root, relief='groove')
       frame2 = tk.Frame(root, relief='groove')
       frame3 = tk.Frame(root, relief='groove')

       self.SetPosBox = tk.Entry(frame1, width=16, font=("Arial","16"))
       self.SetPosBox.insert(tk.END,'0')
   
       self.statustxt = tk.StringVar()
       self.statustxt.set('open device %s' % name)
       Statusbar = tk.Label(root, textvariable=self.statustxt, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Open Sans","12"))
   
       self.Bt_home = tk.Button(frame1, text = u'Home'          , width=16, font=("Open Sans","16"))
       self.Bt_read = tk.Button(frame1, text = u'Read'          , width=16, font=("Open Sans","16"))
       self.Bt_move = tk.Button(frame1, text = u'Move to', width=16, font=("Open Sans","16"), command=partial(self.MoveClick, 9999))
       self.Bt_mov1 = tk.Button(frame2, text = u'-50', width=4, font=("Open Sans","12"), command=partial(self.MoveRClick, -50))
       self.Bt_mov2 = tk.Button(frame2, text = u'-10', width=4, font=("Open Sans","12"), command=partial(self.MoveRClick, -10))
       self.Bt_mov3 = tk.Button(frame2, text = u'+10', width=4, font=("Open Sans","12"), command=partial(self.MoveRClick, 10))
       self.Bt_mov4 = tk.Button(frame2, text = u'+50', width=4, font=("Open Sans","12"), command=partial(self.MoveRClick, 50))
       self.Bt_stop = tk.Button(frame3, text = u'Stop'          , width=16, font=("Open Sans","16"))
       self.Bt_clos = tk.Button(frame3, text = u'Close'         , width=16, font=("Open Sans","16"))
       self.Bt_home.bind('<1>',self.HomeClick)
       self.Bt_read.bind('<1>',self.Read)
       self.Bt_stop.bind('<1>',self.Stop)
       self.Bt_clos.bind('<1>',self.Close)

       frame1.pack(pady=0)
       self.Bt_home.pack()
       self.Bt_read.pack()
       self.SetPosBox.pack()
       self.Bt_move.pack()
   
       frame2.pack(pady=0)
       self.Bt_mov1.pack(side='left')
       self.Bt_mov2.pack(side='left')
       self.Bt_mov3.pack(side='left')
       self.Bt_mov4.pack(side='left')
   
       frame3.pack(pady=10)
       self.Bt_stop.pack()
       self.Bt_clos.pack(side=tk.BOTTOM)
       Statusbar.pack(side=tk.BOTTOM, fill=tk.X)
   
       root.mainloop()

    def Bt_Disable(self):
        self.Bt_home.configure(state="disabled")
        self.Bt_read.configure(state="disabled")
        self.Bt_move.configure(state="disabled")
        self.Bt_mov1.configure(state="disabled")
        self.Bt_mov2.configure(state="disabled")
        self.Bt_mov3.configure(state="disabled")
        self.Bt_mov4.configure(state="disabled")
        self.Bt_clos.configure(state="disabled")

    def Bt_Enable(self):
        self.Bt_home.configure(state="normal")
        self.Bt_read.configure(state="normal")
        self.Bt_move.configure(state="normal")
        self.Bt_mov1.configure(state="normal")
        self.Bt_mov2.configure(state="normal")
        self.Bt_mov3.configure(state="normal")
        self.Bt_mov4.configure(state="normal")
        self.Bt_clos.configure(state="normal")

    def Close(self, event):
        sys.exit()
        ser.Close()

    def Read(self, event):
        val, status = ser.Read()
        val = ser.step2mm(int(val))
        now = time.strftime('%H:%M:%S')
        self.statustxt.set("position = %.3lf mm (%s)" % (val, now))

    def Home(self):
        self.Bt_Disable()
        ser.Home()
        self.statustxt.set("Going to Home position")
        ser.WaitBusy()
        val, status = ser.Read()
        val = ser.step2mm(int(val))
        now = time.strftime('%H:%M:%S')
        self.statustxt.set("position = %.3lf mm (%s)" % (val, now))
        self.Bt_Enable()

    def Move(self):
        self.Bt_Disable()
        if float(self.setpos) >= 0 and float(self.setpos) <= 240:
          status = ser.Move(float(self.setpos))
          self.statustxt.set(status)
          ser.WaitBusy()
          val, status = ser.Read()
          val = ser.step2mm(int(val))
          now = time.strftime('%H:%M:%S')
          self.statustxt.set("position = %.3lf mm (%s)" % (val, now))
          self.Bt_Enable()
        else:
          self.statustxt.set("range over")
          self.Bt_Enable()

    def MoveR(self):
        self.Bt_Disable()
        status = ser.MoveR(float(self.setpos))
        self.statustxt.set(status)
        ser.WaitBusy()
        val, status = ser.Read()
        val = ser.step2mm(int(val))
        now = time.strftime('%H:%M:%S')
        self.statustxt.set("position = %.3lf mm (%s)" % (val, now))
        self.Bt_Enable()

    def Stop(self, event):
        ser.Stop()
        self.statustxt.set("Stopped")

    def HomeClick(self, event):
        thread = threading.Thread(target=self.Home)
        thread.start()

    def MoveClick(self, pos):
        self.setpos = self.SetPosBox.get()
        thread = threading.Thread(target=self.Move)
        thread.start()

    def MoveRClick(self, pos):
        self.setpos = pos
        thread = threading.Thread(target=self.MoveR)
        thread.start()

if __name__ == '__main__':
    ser = StageControl.StageControl()
    if len(sys.argv) != 2:
      print('TYPE  ./controlGUI /dev/ttyUSB0')
      sys.exit()
    if not os.path.exists(sys.argv[1]):
      print('FILE %s does not exist' % sys.argv[1])
      sys.exit()

    name = sys.argv[1]
    ser.Open(name)
    gui = GUI()


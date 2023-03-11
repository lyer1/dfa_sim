from tkinter import *

STATE_RADIUS, STATE_INNER_CIRCLE_DIF = 70, 7
DIMENSION = [1000, 800]
Q_NO = [0]

#shortening variables
sicd = STATE_INNER_CIRCLE_DIF

win= Tk()
win.geometry(str(DIMENSION[0])+"x"+str(DIMENSION[1]))

c= Canvas(win, width = DIMENSION[0], height = DIMENSION[1])
c.pack()


def callback(e, qno = Q_NO):
   x= e.x
   y= e.y
   c.create_oval(x, y, x + STATE_RADIUS, y + STATE_RADIUS)
   c.create_oval(x + sicd, y + sicd, x + STATE_RADIUS - sicd, y + STATE_RADIUS - sicd)
   c.create_text(x + sicd * 5, y + sicd * 5, text = f"q{(Q_NO[0])}", fill="black", font=('Helvetica 20 italic'))
   Q_NO[0] += 1

win.bind('<Button-1>',callback)
win.mainloop()


from tkinter import *
import random


class Ball():
    def __init__(self):
        self.radius=30
        self.sx=10 #speed x
        self.sy=10  #speed y
        self.maxs=20
        self.s_up=1.1
        self.id = c.create_oval(width/2-self.radius/2,
                                    height/2-self.radius/2,
                                    width/2+self.radius/2,
                                    height/2+self.radius/2, fill="white")
    def bounce(self,action):
        if action == "strike":
            self.sy = random.randrange(-10, 10)
            if abs(self.sx) < self.maxs:
                self.sx *= -self.s_up
            else:
                self.sx = -self.sx
        else:
            self.sy = -self.sy

    def spawn(self):
        c.coords(self.id, width/2-self.radius/2,
                 height/2-self.radius/2,
                 width/2+self.radius/2,
                 height/2+self.radius/2)
        self.sx = -(self.sx * -10) / abs(self.sx)
            
    def move(self):
        ball_left, ball_top, ball_right, ball_bot = c.coords(self.id)
        ball_center = (ball_top + ball_bot) / 2
        if ball_right + self.sx < width-left_pad.width and ball_left + self.sx > left_pad.width:
            c.move(self.id,self.sx,self.sy)
        elif ball_right == width-left_pad.width or ball_left == left_pad.width:
            if ball_right > width / 2:
                if c.coords(right_pad.id)[1] <= ball_center <= c.coords(right_pad.id)[3]:
                     self.bounce("strike")
                else:
                    left_pad.update_score()
                    ball.spawn()
            else:
                if c.coords(left_pad.id)[1] <= ball_center <= c.coords(left_pad.id)[3]:
                    self.bounce("strike")
                else:
                    right_pad.update_score()
                    ball.spawn()
        else:
            if ball_right > width / 2:
                c.move(self.id, width-left_pad.width-ball_right, self.sy)
            else:
                c.move(self.id, -ball_left+left_pad.width, self.sy)
        if ball_top + self.sy < 0 or ball_bot + self.sy > height:
            self.bounce("ricochet")

class Pad():
    def __init__(self,side):
        self.width=10
        self.height=100
        self.speed=0
        self.score=0
        if side=="left":
            self.text=c.create_text(width/4, height/4,
                         text=self.score,
                         font="Arial 20",
                         fill="white")
            self.id=c.create_line(self.width/2, 0, self.width/2, self.height, width=self.width, fill="white")
        else:
            self.text=c.create_text(width-width/4, height/4,
                         text=self.score,
                         font="Arial 20",
                         fill="white")
            self.id=c.create_line(width-self.width/2, 0, width-self.width/2, self.height, width=self.width, fill="white")

    def move(self):
        c.move(self.id, 0, self.speed)
        if c.coords(self.id)[1]<0:
            c.move(self.id, 0, -c.coords(self.id)[1])
        elif c.coords(self.id)[3]>height:
            c.move(self.id, 0, height - c.coords(self.id)[3])

    def stop(self):
        self.speed=0
            

    def update_score(self):
        self.score+=1
        c.itemconfig(self.text,text=self.score)


    
def movement(event):
    if event.keysym=="w":
        left_pad.speed= -pad_speed
    elif event.keysym == "s":
        left_pad.speed = pad_speed
    elif event.keysym == "Up":
        right_pad.speed = -pad_speed
    elif event.keysym == "Down":
        right_pad.speed = pad_speed

def stop_pad(event):
    if event.keysym in "ws":
        left_pad.speed = 0
    elif event.keysym in ("Up", "Down"):
        right_pad.speed = 0

def main():
    ball.move()
    left_pad.move()
    right_pad.move()
    root.after(30, main)
    
if __name__=='__main__':
    width=1000
    height=600
    pad_speed=20
    
    root = Tk()
    root.title("Теннис")
    c = Canvas(root, width=width, height=height, background="#000000")
    c.pack()

    left_pad=Pad("left")
    right_pad=Pad("right")

    c.create_line(width/2, 0, width/2, height, fill="white")
     
    ball = Ball()

    c.focus_set()
    c.bind("<KeyPress>", movement)
    c.bind("<KeyRelease>", stop_pad)
    
    main()
    root.mainloop()
    
    

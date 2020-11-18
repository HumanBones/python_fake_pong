class Player:

    def __init__(self,x,y,color="#ffffff",width=8,height=16,speed=4):
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed


    def start():
        pass

    def update(self,vx=0,vy=0):
        self.x += vx * self.speed
        self.y += vy * self.speed
class Ball:

    def __init__(self,x,y,color="#ffffff",size=16, speed=2):
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.vx = -1
        self.vy = -1

    def start():
        pass

    def update(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        

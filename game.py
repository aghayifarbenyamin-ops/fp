from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty,NumericProperty,ReferenceListProperty#این دو تایی که اضافه کردم برای این هستن
#که توپ به دیوار میخوره برگرده
from kivy.vector import Vector
from random import randint

class PongGame(Widget):
    turn=0
    ball=ObjectProperty(None)
    player1=ObjectProperty(None)
    player2=ObjectProperty(None)
    def update(self,arg):
        self.ball.move()
        if self.turn in [1,0]:
            if self.player1.push_ball(self.ball):
                self.turn=2
        if self.turn in [2,0]:
            if self.player2.push_ball(self.ball):
                self.turn=1
        #بررسی این که به گوشه ها برخورد کرد
        if 0>=self.ball.y or self.ball.top>=self.height:
            self.ball.velocity_y*=-1
        if -55>=self.ball.x:
            self.player2.score+=1
            self.serve_ball()
        if  self.ball.right>=self.width+55:
            self.player1.score+=1
            self.serve_ball()
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4,0).rotate(randint(0,360))
    def on_touch_move(self, touch):
        if touch.x<self.width/3:
            self.player1.center_y=touch.y
        elif touch.x>2*self.width/3:
            self.player2.center_y=touch.y
        return super().on_touch_move(touch)

class PongBall(Widget):
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(1)
    velocity = ReferenceListProperty(velocity_x,velocity_y)#فکر کنم تغییر در این موجب تغییر در بالایی ها میشه و برعکس
    def move(self):
        self.pos = Vector(self.pos) + Vector(self.velocity)

class PongPaddle(Widget):
    score=NumericProperty(0)
    def push_ball(self,ball):
        if self.collide_widget(ball):
            v=Vector(ball.velocity)
            v.x*=-1.1
            v.y*=1.1
            ball.velocity=v

            return True
        return False
            
class GameApp(App):
    def build(self):
        game=PongGame()
        game.serve_ball()
        # Clock.schedule_interval(tabe,doretanavob(s))
        Clock.schedule_interval(game.update,1/60)
        return game
    
GameApp().run()
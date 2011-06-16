from Tkinter import *
from PIL import Image,ImageTk
from start import Application
from mr_x import MrX
from police import Police
import os
import time

GUI_DIR = os.path.join(os.path.dirname(__file__),"gui")

class SY_GUI(object):

    """
    Original "London.jpg" Bildgroesse in Pixel
    """
    original_Width = 1639
    original_Height = 1228

    def __init__(self, picture_Width=1639,picture_Height=1228,picture="london.jpg"):
        
        self.app = Application(Police,MrX,log_core=40,log_mrx=40,log_police=40)
        
        #self.num_of_players = len(police_Array) + 1
        self.police = self.app.polices
        #self.total_player = len(police_Array) + 1

        self.misterX = self.app.x
            
        self.visible_moves_mrX = (3,8,13,18)
        self.num_of_moves = 1

        self.color_array = ["red", "green", "blue", "cyan", "magenta","white", "black"]
        self.mrX_color = "yellow"

        """
        Initialisierung von Tk
        """        
        self.root = Tk()
        self.root.bind("<Return>",self.draw)

        """
        Will man ein kleineres Bild als das Originalbild verwenden, kann man die Angaben in folgenden Variablen
        mitgeben --> picture_Widht,picture_Height
        """
        self.scale(1200,700)

        
        """
        Laedt alle Stationen in den 'stations' Array
        #e.g. stations[1] bezieht sich auf Punkt 1 auf dem Spielbrett
        """
        self.stations = self.load_stations()

        """
            -----------------------
            Erstellen des Canvas
            -----------------------
        """

        self.myCanvas = Canvas(self.root, width=1200,height=700)
        #self.myCanvas.bind("<Button-1>",self.alert)
        self.myCanvas.pack()


        """
            -----------------------
            Laden des Bildes
            -----------------------
        """ 

        self.image = self.load_image(os.path.join(GUI_DIR,picture))
        photo = ImageTk.PhotoImage(self.image)
        self.myCanvas.image = photo


        """
        anchor option setzt 0 0 koordinate nach oben links (NW), so dass
        ganzes bild angezeigt wird
        """
        self.myCanvas.create_image(0,0,image=photo,anchor=NW)


        """
        #punkt 1      
        s = self.stations[7]
        #s.punkt = self.myCanvas.create_oval(s.x1,s.y1,s.x2,s.y2,fill="black")
        s.punkt = self.draw_circle(s)
        #self.stations[7].punkt = self.draw_circle(self.stations[7])
        """

        """
            -----------------------
            Zeichnen der Startpositionen
            -----------------------
        """ 
        
        if self.police:
            count = 0
            for p in self.police:
                color = count % (len(self.color_array)-1)
                
                s = self.stations[p.get_position()]
                s.punkt = self.draw_circle(s,self.color_array[color])

                count += 1

            s = self.stations[self.misterX.get_position()]
            
            s.punkt = self.draw_star(s,self.mrX_color)
         
        self.root.mainloop()

    def alert(self,event):
        print "hallo du"

        
    def draw_circle(self,station,color="black"):
        s = station
        x = s.centerX
        y = s.centerY

        x1 = x - 10
        y1 = y - 10
        x2 = x + 10
        y2 = y + 10

        #circle = self.myCanvas.create_oval(s.x1,s.y1,s.x2,s.y2,fill=color)
        circle = self.myCanvas.create_oval(x1,y1,x2,y2,fill=color)
        return circle

    
    def draw_star(self,station,color="yellow"):
        s = station

        x = s.centerX
        y = s.centerY

        x1 = x-15 ; y1 = y+20; x2 = x;    y2 = y-20
        x3 = x+15 ; y3 = y+20; x4 = x-20; y4 = y-5
        x5 = x+20; y5 = y-5  ;x6 = x1; y6 = y1
        
        star = self.myCanvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,fill=color)
        return star
    
    
    def load_stations(self):
        station_file = open(os.path.join(GUI_DIR,'stations.txt'),'r')
        station_list = station_file.readlines()
        del station_list[0]
        station_file.close()

        stations = [None]

        for s in station_list:
            x1 = int(int(s.split(" ")[1]) * self.xRatio)
            y1 = int(int(s.split(" ")[2]) * self.yRatio)
            name = "Station " + s.split(" ")[0]

            stations.append(self.Station(x1,y1,name))
                            
        return stations
        
        
    def move(self,von,nach,color="black",misterX=False):

        v = self.stations[von].punkt
        n = self.stations[nach]
        
        self.myCanvas.delete(v)
        self.myCanvas.delete(n.punkt)
        
        if v:
            if misterX:
                n.punkt = self.draw_star(n,color)
            else:
                n.punkt = self.draw_circle(n,color)

        self.stations[von].punkt= None

    """
    Will  man ein kleineres Bild als das Originalbild brauchen
    dann muessen die Koordinaten der Punkte geaendert werden
    """
    def scale(self,xPixel,yPixel):
        self.xWidth = xPixel
        self.yHeight = yPixel

        self.xRatio = float(self.xWidth) / SY_GUI.original_Width 
        self.yRatio = float(self.yHeight) / SY_GUI.original_Height 


    def load_image(self,imagePath):
        return Image.open(imagePath)

    
    def draw(self, event=None):
        from start import EndOfGame
        try:
            self.app.play_round()
        except EndOfGame, e:
            print e
            exit()
            
        player = self.app.active_player

        
        if player != 0:
            von = self.police[player - 1].get_old_position()
            nach = self.police[player - 1].get_position()
            
            self.move(von,nach,self.color_array[player-1])
            self.num_of_moves += 1
        else:
            von = self.misterX.get_old_position()
            nach = self.misterX.get_position()

            if self.misterX.is_visible():
                self.move(von,nach,"yellow",True)
            else:
                self.move(von,nach,"black",True)
            self.num_of_moves += 1
    
    
    class Station(object):
        def __init__(self,x,y,name):
            self.centerX = x
            self.centerY = y
            self.name = name
            self.punkt = None

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name

    #dummy Class zum Test
class Player(object):
    def __init__(self, moves):
        self.moves = moves


gui = SY_GUI()
"""
q = Player([1,18,43,1,18])
w = Player([3,11,22,3,11])
e = Player([5,16,28,5,16])
r = Player([7,17,42,7,17])
police = [q,w,e]
mrX = r  
"""
#x = SY_GUI(police,mrX)
"""
root = Tk()
myapp = SY_GUI(police,mrX)
root.mainloop()



if __name__ == '__main__':
    q = Player([1,18,43,1,18])
    w = Player([3,11,22,3,11])
    e = Player([5,16,28,5,16])
    r = Player([7,17,42,7,17])
    police = [q,w,e]
    mrX = r

    x = SY_GUI(police,mrX)
    time.sleep(6)
    print "after sleep"
"""

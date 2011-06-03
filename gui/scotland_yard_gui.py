from Tkinter import *
from PIL import Image,ImageTk

class SY_GUI(object):

    """
    Original "London.jpg" Bildgroesse in Pixel
    """
    original_Width = 1639
    original_Height = 1228

    def __init__(self, police_Array=None, mister_X=None, picture_Width=1639,picture_Height=1228,picture="london.jpg"):

        if police_Array:
            self.num_of_players = len(police_Array) + 1
            self.police = police_Array
            #self.total_player = len(police_Array) + 1

        if mister_X:
            self.misterX = mister_X
            
        self.visible_moves_mrX = (3,8,13,18)
        self.num_of_moves = 1

        self.color_array = ["white", "black", "red", "green", "blue", "cyan", "magenta"]
        self.mrX_color = "yellow"

        """
        Initialisierung von Tk
        """        
        self.root = Tk()

        """
        Will man ein kleineres Bild als das Originalbild verwenden, kann man die Angaben in folgenden Variablen
        mitgeben --> picture_Widht,picture_Height
        """
        self.scale(1200,700)

        
        """
        http://infohost.nmt.edu/tcc/help/pubs/tkinter/canvas.html#create_oval
        jeder Punkt auf dem Spielbrett braucht eine x1/y1 Angabe. Dieser Punk
        befindet sich in der mitte (siehe link). x2 = x1+20, y2 = x2+20

        punkt 8 = 88/52
        """
        #e.g. station_arr[1] refers to station nr. 1 on the board
        self.stations = self.load_stations()

        #self.myParent = parent

        self.myCanvas = Canvas(self.root, width=1200,height=700)
        self.myCanvas.pack()

        """
            -----------------------
            Laden des Bildes
            -----------------------
        """ 

        #self.image = Image.open("london.jpg")
        self.image = self.load_image(picture)
        photo = ImageTk.PhotoImage(self.image)
        self.myCanvas.image = photo

        """
        #anchor option setzt 0 0 koordinate nach oben links (NW), so dass
        #ganzes bild angezeigt wird
        """
        self.myCanvas.create_image(0,0,image=photo,anchor=NW)

        """
        #punkt 1      
        s = self.stations[7]
        #s.punkt = self.myCanvas.create_oval(s.x1,s.y1,s.x2,s.y2,fill="black")
        s.punkt = self.draw_circle(s)
        #self.stations[7].punkt = self.draw_circle(self.stations[7])
        """
        # Zeichnen der Startpositionen
        
        if self.police:
            count = 0
            for p in self.police:
                color = count % (len(self.color_array)-1)
                
                s = self.stations[p.moves[0]]
                s.punkt = self.draw_circle(s,self.color_array[color])

                count += 1

            s = self.stations[self.misterX.moves[0]]
            #s.punkt = self.draw_circle(s,self.mrX_color)
            s.punkt = self.draw_star(s,self.mrX_color)
         
        
        """
        label = Label(self.myContainer1, image=photo)
        label.image = photo
        label.pack()
        """

    # Diese Funktion wird gebraucht um die Kreise, welche die Polizisten und Mr.X darstellt
    # zu zeichnen
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
        """
        x1 = x-5 ; y1 = y+10; x2 = x;    y2 = y-10
        x3 = x+5 ; y3 = y+10; x4 = x-10; y4 = y-2.5
        x5 = x+10; y5 = y-2.5;x6 = x1; y6 = y1
        """
        x1 = x-15 ; y1 = y+20; x2 = x;    y2 = y-20
        x3 = x+15 ; y3 = y+20; x4 = x-20; y4 = y-5
        x5 = x+20; y5 = y-5  ;x6 = x1; y6 = y1
        
        star = self.myCanvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,fill=color)
        return star
    
    
    def load_stations(self):
        station_file = open('stations.txt','r')
        station_list = station_file.readlines()
        del station_list[0]
        station_file.close()

        stations = [None]

        for s in station_list:
            x1 = int(int(s.split(" ")[1]) * self.xRatio)
            y1 = int(int(s.split(" ")[2]) * self.yRatio)
            name = "Station " + s.split(" ")[0]

            stations.append(self.Station(x1,y1,name))
            #stations.append(self.Station(int(s.split(" ")[1]),int(s.split(" ")[2]),"Station " + s.split(" ")[0]))
            
            #stations.append(self.Station(int("12"),int("13")))
                            
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
                #n.punkt = self.myCanvas.create_oval(n.x1,n.y1,n.x2,n.y2,fill=color)
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
    
    def draw(self):
        player = self.num_of_moves % self.num_of_players

        if player != 0:
            von = self.police[player - 1].moves[-2]
            nach = self.police[player - 1].moves[-1]

            """nur fuer die tests"""
            del self.police[player - 1].moves[-2]
            del self.police[player - 1].moves[-1]
            """nur fuer die tests"""
            
            self.move(von,nach,self.color_array[player-1])
            self.num_of_moves += 1
        else:
            von = self.misterX.moves[-2]
            nach = self.misterX.moves[-1]

            """nur fuer die tests"""
            del self.misterX.moves[-2]
            del self.misterX.moves[-1]
            """nur fuer die test"""
            
            self.move(von,nach,"yellow",True)
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
            
        
q = Player([1,18,43,1,18])
w = Player([3,11,22,3,11])
e = Player([5,16,28,5,16])
r = Player([7,17,42,7,17])
police = [q,w,e]
mrX = r  

"""
root = Tk()
myapp = SY_GUI(root)
root.mainloop()
"""
#if __name__ == '__main__':

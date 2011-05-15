from Tkinter import *
from PIL import Image,ImageTk

class SY_GUI(object):

    """
    Original "London.jpg" Bildgroesse in Pixel
    """
    original_Width = 1639
    original_Height = 1228

    def __init__(self, police_Array=None, mister_X=None, picture_Width=1639,picture_Height=1228,picture="london.jpg"):


        """
        Initialisierung von Tk
        """        
        self.root = Tk()

        """
        Will man ein kleineres Bild als das Originalbild verwenden, kann man die Angaben in folgenden Variablen
        mitgeben --> picture_Widht,picture_Height und picture
        """
        self.scale(picture_Width,picture_Height,picture)

        
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


        #punkt 1
        #self.punkt = self.myCanvas.create_oval(130,15,150,35,fill="black")      
        s = self.stations[1]
        s.punkt = self.myCanvas.create_oval(s.x1,s.y1,s.x2,s.y2,fill="black")

        """
        label = Label(self.myContainer1, image=photo)
        label.image = photo
        label.pack()
        """
    def load_stations(self):
        station_file = open('stations.txt','r')
        station_list = station_file.readlines()
        del station_list[0]
        station_file.close()

        stations = [None]

        for s in station_list:
            x1 = int(s.split(" ")[1])
            y1 = int(s.split(" ")[2])
            name = "Station " + s.split(" ")[0]

            stations.append(self.Station(x1,y1,name))
            #stations.append(self.Station(int(s.split(" ")[1]),int(s.split(" ")[2]),"Station " + s.split(" ")[0]))
            
            #stations.append(self.Station(int("12"),int("13")))
                            
        return stations
        
        
    def move(self,von,nach):

        v = self.stations[von].punkt
        n = self.stations[nach]
        
        self.myCanvas.delete(v)
        
        if v:
            n.punkt = self.myCanvas.create_oval(n.x1,n.y1,n.x2,n.y2,fill="black")

        self.stations[von].punkt= None

    """
    Will man ein kleineres Bild als das Originalbild brauchen
    dann muessen die Koordinaten der Punkte geaendert werden
    """
    def scale(self,xPixel,yPixel, image):
        self.xWidth = xPixel
        self.yHeight = yPixel

        self.xRatio = SY_GUI.original_Width / float(self.xWidth)
        self.yRatio = SY_GUI.original_Height / float(self.yHeight)
        
        if image:
            self.image = self.load_image(image)


    def load_image(self,imagePath):
        return Image.open(imagePath)

    def draw(self):
        pass

    
    class Station(object):
        def __init__(self,x,y,name):
            self.x1 = x - 10
            self.y1 = y - 10
            self.x2 = x + 10
            self.y2 = y + 10
            self.name = name
            self.punkt = None

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name
        

"""
root = Tk()
myapp = SY_GUI(root)
root.mainloop()
"""
if __name__ == '__main__':
    gui = SY_GUI()    
                            

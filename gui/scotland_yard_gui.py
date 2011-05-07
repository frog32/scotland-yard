from Tkinter import *
from PIL import Image,ImageTk

class SY_GUI(object):
    def __init__(self):

        self.root = Tk()
        """
        http://infohost.nmt.edu/tcc/help/pubs/tkinter/canvas.html#create_oval
        jeder Punkt auf dem Spielbrett braucht eine x1/y1 Angabe. Dieser Punk
        befindet sich oben links (siehe link). x2 = x1+20, y2 = x2+20

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

        image = Image.open("london.jpg")
        photo = ImageTk.PhotoImage(image)
        self.myCanvas.image = photo

        """
        #anchor option setzt 0 0 koordinate nach oben links, so dass
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
            stations.append(self.Station(int(s.split(" ")[1]),int(s.split(" ")[2]),"Station " + s.split(" ")[0]))
            
            #stations.append(self.Station(int("12"),int("13")))
                            
        return stations
        
        
    def move(self,von,nach):
        
        v = self.stations[von].punkt
        n = self.stations[nach]
        
        self.myCanvas.delete(v)
        n.punkt = self.myCanvas.create_oval(n.x1,n.y1,n.x2,n.y2,fill="black")

    class Station(object):
        def __init__(self,x1,y1,name):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x1 + 20
            self.y2 = y1 + 20
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
                            

from Tkinter import *
from PIL import Image,ImageTk

class SY_GUI(object):
    def __init__(self,parent):

        self.root = Tk()
        """
        http://infohost.nmt.edu/tcc/help/pubs/tkinter/canvas.html#create_oval
        jeder Punkt auf dem Spielbrett braucht eine x1/y1 Angabe. Dieser Punk
        befindet sich oben links (siehe link). x2 = x1+20, y2 = x2+20

        punkt 8 = 88/52
        """
        #e.g. station_arr[1] refers to station nr. 1 on the board
        self.stations = load_stations()
        self.myParent = parent

        self.myCanvas = Canvas(parent, width=1200,height=700)
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
        self.myCanvas.create_oval(130,15,150,35,fill="black")      
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

        for s = station_list:
            stations.append(Station(int(s.split(" ")[1]),int(s.split(" ")[2]))

        return stations
        
        
    def move(self,von,nach):
        pass

    class Station(object):
        def __init__(self,x,y):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x1 + 20
            self.y2 = y1 + 20

"""
root = Tk()
myapp = SY_GUI(root)
root.mainloop()
"""
if __name__ == '__main__':
                            

from Tkinter import *
from PIL import Image,ImageTk

class MyApp:
    def __init__(self,parent):
        self.myParent = parent

        self.myCanvas = Canvas(parent, width=1200,height=700)
        self.myCanvas.pack()
        
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

root = Tk()
myapp = MyApp(root)
root.mainloop()

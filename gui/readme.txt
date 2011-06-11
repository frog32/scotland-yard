- Um das GUI brauchen zu können muss man die 'PIL', die Python Image Library, installiert haben.

  Natürlich braucht man dazu zuerst Python.

  PIL kann von 'http://www.pythonware.com/products/pil/' bezogen werden.

  Auf meinem PC sind Python 2.7 und PIL 1.1.7 installiert.


- Der ganzen Code der grafischen Darstellung befindet sich im File "scotland_yard_gui.py". Die meisten Funktionen
  und Code-Abschnitte sollten selbsterklaerend oder dokumentiert sein.



Verwendung des GUIs
-------------------

- Öffnen des Python Interpreters--> cmd -> python

- Importieren des Packetes 	--> from scotland_yard_gui import *

- Instanzieren der GUI Klasse 	--> gui = SY_GUI(police_Array, mister_X,picture_Width,picture_Height,picture)
	- Wichtig sind die Argumente 'police_Array' und 'mister_X', die Restlichen Argumente sind nur wichtig,
	  wenn man ein Bild verwenden will, dessen Dimensionen sich von Standartbild unterscheiden. Die letzten
	  3 Argumente müssen also nicht übergeben werden.
	
	- Wichtig ist, dass jeder Spieler eine Instanzvariabel 'moves' vom Typ List besitzt und das an dem ersten Index ein
	  Int-Wert gesetzt ist, der den Startpunkt dieser Figur bestimmt.

- Bewegen der Figuren
	- 1. Mit der move Funktion	--> gui.move(von,nach,farbe)
	  Die Parameter 'von' und 'nach' bestimmen von wo nach wo eine Figur sich bewegen soll.
	  Natürlich muss sich auf dem 'von' Feld schon eine Figur befinden. Color ist default Schwarz.

	- 2. Mit der draw Funktion	--> gui.draw()
	  Das Spielt sollte eigentlich mit dieser Funktion gespielt werden. Die Funktion schaut auf die letzten 2 Einträge
	  der Instanzvariabel move die den Typ List hat und bewegt so die Spieler. Ausserdem wird so sichergestellt, dass jeder
	  Spieler, dem zu Anfang eine eigene Farbe zugewiesen wurde, diese auch behält
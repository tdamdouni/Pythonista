#coding: utf-8
# http://www.uni-brachbach.de/dokuwiki/doku.php/informatik-buch:programmiersprachen:python:beispiele:karol_in_python#version_010

from __future__ import print_function
from RobbiDaten import *
#from RobbiShell import *
#from RobbiInter import *
#from tkFileDialog   import askopenfilename

from Tkinter import *
import tkFileDialog

#from tkMessageBox import *
#from tkColorChooser import askcolor


class GUI:

	def __init__(self,roboter):
	
		# Daten-Objekte
		self.Roboter = roboter
		self.Ziegel = [[0 for i in range(10)] for j in range(10)]
		
		# GUI-Objekte definieren
		self.fenster = Tk()
		self.fenster.title("Robbi Roboter")
		self.frame1 = Frame(master=self.fenster)
		self.frame2 = Frame(master=self.fenster)
		self.welt2d = Canvas(master=self.frame1, width=511, height=511, bg="white")
		self.eingabe = Text(master=self.frame1, width=40, height=36, bg = "#f0f0f0")
		self.buttonQuit = Button(master=self.frame2, text="Quit", command=self.fenster.quit)
		self.buttonNeueWelt = Button(master=self.frame2, text="Neue Welt", command=self.welt2dzeichnen)
		self.buttonSchritt = Button(master=self.frame2, text="Schritt", command=self.schritt)
		self.buttonLinks = Button(master=self.frame2, text="Linksdrehen", command=self.linksdrehen)
		self.buttonRechts = Button(master=self.frame2, text="Rechtsdrehen", command=self.rechtsdrehen)
		self.buttonHinlegen = Button(master=self.frame2, text="Hinlegen", command=self.hinlegen)
		self.buttonAufheben = Button(master=self.frame2, text="Aufheben", command=self.aufheben)
		self.buttonAusfuehren = Button(master=self.frame1, text ="Ausführen", command=self.ausfuehrenclick)
		self.buttonLaden = Button(master=self.frame1, text ="Laden", command=self.laden)
		self.buttonSpeichern = Button(master=self.frame1, text ="Speichern", command=self.speichern)
		
		
		# GUI-Objekte anordnen
		self.frame1.pack()
		self.frame2.pack()
		self.welt2d.pack(expand=YES, fill=BOTH, side=LEFT)
		self.eingabe.pack(side=TOP)
		self.buttonNeueWelt.pack(side=RIGHT)
		self.buttonQuit.pack(side=LEFT)
		self.buttonSchritt.pack(side=LEFT)
		self.buttonLinks.pack(side=LEFT)
		self.buttonRechts.pack(side=LEFT)
		self.buttonHinlegen.pack(side=LEFT)
		self.buttonAufheben.pack(side=LEFT)
		self.buttonAusfuehren.pack(side=LEFT)
		self.buttonLaden.pack(side=LEFT)
		self.buttonSpeichern.pack(side=LEFT)
		
		
	# Gitter zeichnen
	def welt2dzeichnen(self):
		self.welt2d.create_rectangle(10,10,510,510)
		for i in range(10,510,50):
			self.welt2d.create_line(10,i,510,i)
		for i in range(10,510,50):
			self.welt2d.create_line(i,10,i,510)
			
	# Alle Ziegel zeichnen (Zahl oder leerer String)
	def ziegelzeichnen(self):
		for j in range(10):
			for i in range(10):
				te=str(self.Roboter.Welt.Ziegel[i][j])
				if te =="0":te=""
				self.Ziegel[i][j]=self.welt2d.create_text(i*50+35,j*50+35,text=te)
				
	# Roboter (Dreieck) zeichnen)
	def roboterzeichnen(self):
		robx = 50*self.Roboter.Posx + 35
		roby = 50*self.Roboter.Posy + 35
		if self.Roboter.Richtung == [0,1]:
			self.dreieck=self.welt2d.create_polygon(robx-25,roby-25,robx+25,roby-25,robx,roby+25)
		elif self.Roboter.Richtung == [0,-1]:
			self.dreieck=self.welt2d.create_polygon(robx-25,roby+25,robx+25,roby+25,robx,roby-25)
		elif self.Roboter.Richtung == [1,0]:
			self.dreieck=self.welt2d.create_polygon(robx-25,roby-25,robx-25,roby+25,robx+25,roby)
		elif self.Roboter.Richtung == [-1,0]:
			self.dreieck=self.welt2d.create_polygon(robx+25,roby+25,robx+25,roby-25,robx-25,roby)
			
	# Roboter bewegen und neu zeichnen
	def schritt(self):
		self.welt2d.delete(self.dreieck)
		self.Roboter.schritt()
		self.roboterzeichnen()
		
	# Roboter nach links drehen und neu zeichnen
	def linksdrehen(self):
		self.welt2d.delete(self.dreieck)
		self.Roboter.linksDrehen()
		self.roboterzeichnen()
		
	# Roboter nach links drehen und neu zeichnen
	def rechtsdrehen(self):
		self.welt2d.delete(self.dreieck)
		self.Roboter.rechtsDrehen()
		self.roboterzeichnen()
		
	# Ziegel hinlegen und veränderten Ziegel neu zeichnen
	def hinlegen(self):
		if self.Roboter.hinlegen():
			neuziegelx = self.Roboter.Posx + self.Roboter.Richtung[0]
			neuziegely = self.Roboter.Posy + self.Roboter.Richtung[1]
			te=str(self.Roboter.Welt.Ziegel[neuziegelx][neuziegely])
			if te =="0":te=""
			self.welt2d.itemconfig(self.Ziegel[neuziegelx][neuziegely],text=te)
			
	# Ziegel aufheben und veränderten Ziegel neu zeichnen
	def aufheben(self):
		if self.Roboter.aufheben():
			neuziegelx = self.Roboter.Posx + self.Roboter.Richtung[0]
			neuziegely = self.Roboter.Posy + self.Roboter.Richtung[1]
			te=str(self.Roboter.Welt.Ziegel[neuziegelx][neuziegely])
			if te =="0":te=""
			self.welt2d.itemconfig(self.Ziegel[neuziegelx][neuziegely],text=te)
			
	def ausfuehrenclick(self):
		eingabe = self.eingabe.get("1.0",END)
		programm = eingabe.split()
		for i in range(len(programm)):
			if   programm[i] == "wiederhole": programm[i] = "w"
			elif programm[i] == "*wiederhole": programm[i] = "*w"
			elif programm[i] == "schritt": programm[i] = "s"
			elif programm[i] == "rechtsdrehen": programm[i] = "r"
			elif programm[i] == "linksdrehen": programm[i] = "l"
			elif programm[i] == "aufheben": programm[i] = "a"
			elif programm[i] == "hinlegen": programm[i] = "h"
			
		self.ausfuehren(programm)
		
	def ausfuehren(self,liste):
		print(liste)
		merke = [0,0,0,0]
		schleifenzaehler = [0,0,0,0]
		schleife = -1
		
		i = 0
		while i < len(liste):
			if liste[i] == "w":
				schleife += 1
				i += 1
				schleifenzaehler[schleife] = int(liste[i])
				merke[schleife]=(i+1)
			elif liste[i] == "*w":
				if schleifenzaehler[schleife] > 1:
					schleifenzaehler[schleife] -= 1
					i = merke[schleife] - 1
				else:
					schleife -=1
			elif liste[i] == "s":
				self.schritt()
			elif liste[i] == "r":
				self.rechtsdrehen()
			elif liste[i] == "l":
				self.linksdrehen()
			elif liste[i] == "h":
				self.hinlegen()
			elif liste[i] == "a":
				self.aufheben()
			i += 1
			
	def laden(self):
		filename = tkFileDialog.askopenfilename()
		programmdatei = open(filename,"r")
		self.eingabe.delete("1.0",END)
		for zeile in programmdatei:
			self.eingabe.insert(END,zeile)
		programmdatei.close()
		
		
	def speichern(self):
		filename = tkFileDialog.asksaveasfilename()
		programmdatei = open(filename,"w")
		programmdatei.write(self.eingabe.get("1.0",END))
		programmdatei.close()
		
		
w=Welt()                    # Welt der Größe 10x10
r=Roboter(w)                # Roboter in dieser Welt
gui = GUI(r)                # Grafische Oberfläche initialisieren
gui.roboterzeichnen()       # Den Roboter einzeichnen
gui.ziegelzeichnen()        # Die Ziegel einzeichnen
gui.welt2dzeichnen()        # Das Gitter zeichnen
gui.fenster.mainloop()      # Auf Buttonklick warten


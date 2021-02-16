#!/home/lrikozavr/py_env/ML/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
from mpmath import *
from math import *

class Star(object):
	"""docstring for Star"""
	def __init__(self, alpha, delta):
		#super(Star, self).__init__()
		self.alpha = alpha
		self.delta = delta		

	def HtoS(self,alpha):
		return alpha*3600.
	def StoH(self,alpha):
		return alpha/3600.
	######################################
	'''
	def Htoh(self):
		h=round(self.alpha/3600.,0)
		m=round((self.alpha-h*3600.)/60.,0)
		s=self.alpha-h*3600-m*60
		return h,m,s
	def htoH(self,h,m,s):
		self.alpha=h*3600+m*60+s
	'''
	#######################################
	def HDtohd(self,value,flag):
		if(value>0): i=1
		else:	i=-1
		if(flag=="hd"):# dd - degree to degree; dh - degree to hours ; hd - hours to degree ; hh - hour to hour
			value=value*15.
		elif(flag=="dh"):
			value=value/15
		d=trunc(value)
		m=trunc(i*(value-d)*60.)
		s=(i*(value-d)-m/60.)*3600.
		return d,m,s
	def hdtoHD(self,d,m,s,flag):
		if(d>0):i=1
		else:	i=-1
		if(flag=="hd"):
			return (d+i*m/60.+i*s/3600.)*15.
		elif(flag=="dh"):
			return (d+i*m/60.+i*s/3600.)/15.
		else: 
			return (d+i*m/60.+i*s/3600.)
	#######################################
	'''
	def DtoS(self):
		self.delta=self.delta*3600.
	def StoD(self):
		self.delta=self.delta/3600.
	'''
	#######################################
	def DtoR(self,value):
		return radians(value)
	def RtoD(self,value):
		return degrees(value)
	def HtoD(self,value):
		return value*15
	def DtoH(self,value):
		return value/15
	#######################################
	def info(self):
		print("Alpha:	",self.HDtohd(self.alpha,"dh"))
		print("Delta:	",self.HDtohd(self.delta,""))
	def info_abs(self):
		print("Alpha:	",self.alpha)
		print("Delta:	",self.delta)
	#######################################

class Observe(Star):
	def __init__(self,lambada,fi):
	#def __init__(self,lambada,fi,alpha,delta):
		#super(Observe,self).__init__(alpha,delta)#?
		self.lambada = lambada
		self.fi = fi
	#######################################
	def M(self,t):
		return ((46.124362 + 0.0279312*t - 0.00000278*t**2)*t*100)/3600.
	def N(self,t):
		return ((20.043109 - 0.008533*t - 0.00000217*t**2)*t*100)/3600.
	def T(self,jd):
		return (jd-2451545.0)/36524.2199
	def ALPHA(self,jd,alpha,delta):
		return (alpha+self.M(self.T(jd))*sin(self.DtoR(alpha))*tan(self.DtoR(delta)))	#radian????
	def DELTA(self,jd,alpha,delta):
		return (delta+self.N(self.T(jd))*cos(self.DtoR(alpha)))
	########################################
	def S0(self,t):
		return self.StoH(self.hdtoHD(6,41,50.54841,"")*3600. + 86401.84812866*t + 0.093104*t**2 - 0.62e-5*t**3) #hour
	def S(self,s): #hour
		return (s-self.hdtoHD(0,3,56.55,"")*(self.lambada/self.hdtoHD(24,0,0,"")))
	def Time_Angle(self,ut,jd,alpha):
		#print("s",s)
		result = (ut*1.002738 - self.DtoH(alpha) + self.lambada + self.S(self.S0(self.T(jd))))
		if (result>24.):
			result-=24
		return result
	########################################
	def trig(self,Time_Angle,delta):
		return sin(self.DtoR(self.fi))*sin(self.DtoR(delta)) + cos(self.DtoR(self.fi))*cos(self.DtoR(delta))*cos(self.DtoR(Time_Angle))
	def Horisontal_coord(self,Time_Angle,delta):
		return self.RtoD(asin(self.trig(Time_Angle,delta)))
	def Zenit_coord(self,Time_Angle,delta):
		return self.RtoD(asec(1/self.trig(Time_Angle,delta)))
	def Bemporad(self,Time_Angle,delta):
		z=1/self.trig(Time_Angle,delta)
		return (z - 0.0018167*(z-1) - 0.002875*(z-1)**2 - 0.0008083*(z-1)**3)
	########################################
	def info_abs(self):
		print("Lambda:	",self.lambada)
		print("Fi:	",self.fi) 
	def info(self):
		print("Lambda: ",self.HDtohd(self.lambada,""))
		print("Fi:	",self.HDtohd(self.fi,""))
	########################################



###### Константы наблюдателья
#lambada=[2,24,55.8] #долгота
#fi=["+",50,0,10] 	#широта
###### Константы времени наблюдения
#date=2459292.5
#UT=16
######

def HtoD(h,m,s):
    return (h+m/60.+s/3600.)*15.
def DtoD(d,m,s,z):
    if (z=="-"):
        return -d-m/60.-s/3600.
    elif (z=="+"): 
        return d+m/60.+s/3600.
def HtoH(h,m,s):
	return (h + m/60. + s/3600.)
def CtoC(ah0,am0,as0,dd0,dm0,ds0,dz0):
	return HtoD(ah0,am0,as0),DtoD(dd0,dm0,ds0,dz0)

def AD(a,d,date):
	one = Observe(HtoH(lambada[0],lambada[1],lambada[2]),DtoD(fi[1],fi[2],fi[3],fi[0]))
	s=Star(a,d)
	alfa=one.ALPHA(date,s.alpha,s.delta)
	delta=one.DELTA(date,s.alpha,s.delta)
	#one.info()
	#s.info()
	#s.info_abs()
	#one.info()
	return alfa,delta

lambada=[2,24,55.8] #долгота
fi=["+",50,0,10] 	#широта

def retrun(line1,line2):
	n1=line1.split(" ") #ra
	n2=line2.split(" ") #dec
	return HtoD(int(n1[0]),int(n1[1]),float(n1[2])),DtoD(int(n2[1]),int(n2[2]),float(n2[3]),n2[0]) 

def Act():
	#
	UT=float(e1.get())
	date=float(e2.get())
	#
	alpha,delta=retrun(e3.get(),e4.get())
	#
	result_line="Origin Alpha:\t"+str(alpha)+"\nOrigin Delta:\t"+str(delta)
	#
	alpha,delta=AD(alpha,delta,date)
	s=Star(alpha,delta)

	user=Observe(HtoH(lambada[0],lambada[1],lambada[2]),DtoD(fi[1],fi[2],fi[3],fi[0]))
	#user.info()

	Time_Angle=user.Time_Angle(UT,date,alpha)


	result_line+="\nChanged Alpha:	"+str(alpha)
	#lt.set(result_line)
	result_line+="\n"+"Changed Delta:	"+str(delta)
	#lt.set(result_line)
	
	result_line+="\n----------------------------------------"
	result_line+="\nTime_Angle:	"+str(Time_Angle)
	Time_Angle=user.HtoD(Time_Angle)
	if (user.Horisontal_coord(Time_Angle,delta) > (90-user.fi+s.delta)):
		print("Horisontal_coord error")
		exit()	
	result_line+="\nAltitude_Angle:	"+str(user.Horisontal_coord(Time_Angle,delta))
	#result_line+="\nZenit_coord:	"+str(user.Zenit_coord(Time_Angle,delta))
	if (user.Horisontal_coord(Time_Angle,delta) < 0):
		result_line+="\nNot Visible"
		result_line+="\n----------------------------------------"
	else:
		result_line+="\nVisible"
	#print(user.Horisontal_coord(Time_Angle,delta)+user.Zenit_coord(Time_Angle,delta))
	result_line+="\nAir_mass:	"+str(user.Bemporad(Time_Angle,delta))
	result_line+="\n----------------------------------------"
	lt.set(result_line)

root = Tk()
root.title("Star navigator")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w//2 # середина экрана
h = h//2 
w = w - 300 # смещение от середины
h = h - 300
root.geometry('600x600+{}+{}'.format(w, h))
lt= StringVar()
lab = Label(root,bg='black',fg='white',textvariable=lt,anchor='w').place(
	relwidth=0.5,relheight=1,relx=0.5)
#command
but = Button(root,text="Result",activebackground='gray',bg='white',fg='black',command=Act).place(
	relwidth=0.3,relheight=0.1,relx=0.1,rely=0.8)

e1,e2,e3,e4 = StringVar(),StringVar(),StringVar(),StringVar()
ent1 = Entry(root,bg='white',fg='black',textvariable=e1).place(
	relwidth=0.4,height=25,relx=0.05,rely=0.1)
ent2 = Entry(root,bg='white',fg='black',textvariable=e2).place(
	relwidth=0.4,height=25,relx=0.05,rely=0.2)
ent3 = Entry(root,bg='white',fg='black',textvariable=e3).place(
	relwidth=0.4,height=25,relx=0.05,rely=0.3)
ent4 = Entry(root,bg='white',fg='black',textvariable=e4).place(
	relwidth=0.4,height=25,relx=0.05,rely=0.4)

lb1 = Label(root,fg='black',text="UT").place(
	relwidth=0.4,height=25,relx=0.05,rely=0.05)
lb2 = Label(root,fg='black',text="JD").place(
	relwidth=0.4,height=25,relx=0.05,rely=0.15)
lb3 = Label(root,fg='black',text="alpha2000").place(
	relwidth=0.4,height=25,relx=0.05,rely=0.25)
lb4 = Label(root,fg='black',text="delta2000").place(
	relwidth=0.4,height=25,relx=0.05,rely=0.35)

e1.set("16")
e2.set("2459292.5")

def ex1():
	e3.set("10 56 28.8")
	e4.set("+ 7 0 52.34")
def ex2():
	e3.set("12 35 28.3")
	e4.set("- 57 5 22.32")
def ex3():
	e3.set("20 26 18.6")
	e4.set("+ 17 20 32.22")		
def ex4():
	e3.set("2 25 10.3")
	e4.set("+ 0 32 11.44")
var = IntVar()
var.set(1)
Radiobutton(root,text="1",variable=var, value=1, command=ex1).place(
	relx=0.05,rely=0.5)
Radiobutton(root,text="2",variable=var, value=2, command=ex2).place(
	relx=0.15,rely=0.5)
Radiobutton(root,text="3",variable=var, value=3, command=ex3).place(
	relx=0.25,rely=0.5)
Radiobutton(root,text="4",variable=var, value=4, command=ex4).place(
	relx=0.35,rely=0.5)

root.mainloop()

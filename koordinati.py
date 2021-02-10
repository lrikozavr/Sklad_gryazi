#!/home/lrikozavr/py_env/ML/bin/python3
# -*- coding: utf-8 -*-
from mpmath import *

class Star(object):
	"""docstring for Star"""
	def __init__(self, alpha, delta):
		#super(Star, self).__init__()
		self.alpha = alpha
		self.delta = delta		

	def HtoS(self):
		return alpha*3600.
	def StoH(self):
		return alpha/3600.
	def DtoS(self):
		return delta*3600.
	def StoD(self):
		return delta/3600.
	def DtoR(self,value):
		return radians(value)
	def RtoD(self,value):
		return degrees(value)
	def HtoD(self,value):
		return value*15
	def DtoH(self,value):
		return value/15
	#########################
class Observe(Star):
	def __init__(self,lambada,fi,alpha,delta):
		super(Observe,self).__init__(alpha,delta)#?
		self.lambada = lambada
		self.fi = fi
	#########################
	def M(self,t):
		return ((46.124362 + 0.0279312*t - 0.00000278*t**2)*t*100)/3600.
	def N(self,t):
		return ((20.043109 - 0.008533*t - 0.00000217*t**2)*t*100)/3600.
	def T(self,jd):
		return (jd-2451545.0)/36524.2199
	def ALPHA(self,jd):
		return (self.alpha+self.M(self.T(jd))*sin(self.DtoR(self.alpha))*tan(self.DtoR(self.delta)))	#radian????
	def DELTA(self,jd):
		return (self.delta+self.N(self.T(jd))*cos(self.DtoR(self.alpha)))
	def info(self):
		print("Lambda:	",self.HtoD(self.lambada)/3600.)
		print("Fi:	",self.fi) 
		print("Alpha:	",self.alpha)
		print("Delta:	",self.delta)






















######
lambada=[2,24,55.8] #долгота
fi=["+",50,0,10] 		#широта
######
def HtoD(h,m,s):
    return (h+m/60.+s/3600.)*15.
def DtoD(d,m,s,z):
    if (z=="-"):
        return -d-m/60.-s/3600.
    elif (z=="+"): 
        return d+m/60.+s/3600.
'''
def Alfa(a,d,m):
	return (a+m*sin(a)*tan(d))	#radian????
def Delta(a,d,n):
	return (d+n*cos(a))
def M(t):
	return (46.124362 + 0.0279312*t - 0.00000278*t**2)*t*100
def N(t):
	return (20.043109 - 0.008533*t - 0.00000217*t**2)*t*100
def T(jd):
	return (jd-2451545.0)/36524.2199

def AD(ah0,am0,as0,dd0,dm0,ds0,dz0,date):
	a0=HtoD(ah0,am0,as0)/57.3
	d0=DtoD(dd0,dm0,ds0,dz0)/57.3
	alfa=Alfa(a0,d0,N(T(date))/3600)
	delta=Delta(a0,d0,M(T(date))/3600)
	return alfa,delta
'''
def T(jd):
	return (jd-2451545.0)/36524.2199
def HtoS(h,m,s):
	return (h*3600 + m*60 + s)


def AD(ah0,am0,as0,dd0,dm0,ds0,dz0,date):
	one = Observe(HtoS(lambada[0],lambada[1],lambada[2]),DtoD(fi[1],fi[2],fi[3],fi[0]),HtoD(ah0,am0,as0),DtoD(dd0,dm0,ds0,dz0))
	alfa=one.ALPHA(date)
	delta=one.DELTA(date)
	one.info()
	return alfa,delta
date=2459292.5
#alpha,delta=AD(10,56,28.8,7,0,52.34,"+",date)
alpha,delta=AD(12,35,28.3,57,5,22.32,"-",date)



'''
def StoH(sec):
	h=sec // 3600
	m=(sec-h*3600) // 60
	s=sec-h*3600-m*60
	return h,m,s
'''
def HtoH(h,m,s):
	return (h + m/60.0 + s/3600.0)
def S0(t):
	return (HtoS(6,41,50.54841) + 86401.84812866*t + 0.093104*t**2 - 0.62e-5*t**3) #second
def S(s,lam): #second
	return (s-HtoS(0,3,56.55)*(lam/HtoS(24,0,0)))
def TimeD(ut,a,s,lam):
	#print("s",s)
	return (ut*1.002738 - a + lam + s)

UT=16

Time_Angle=TimeD(UT,alpha/15,S(S0(T(date)),HtoS(lambada[0],lambada[1],lambada[2]))/3600,HtoH(lambada[0],lambada[1],lambada[2]))

trig=sin(DtoD(fi[1],fi[2],fi[3],fi[0]))*sin(delta) + cos(DtoD(fi[1],fi[2],fi[3],fi[0]))*cos(delta)*cos(Time_Angle)
Horisontal_coord=asin(trig)
'''
if (Horisontal_coord > (90-DtoD(fi[1],fi[2],fi[3],fi[0])+delta)):
	print("Horisontal_coord error")
	exit()
'''
Zenit_coord=asec(1/trig)

def Bemporad(z):
	return (z - 0.0018167*(z-1) - 0.002875*(z-1)**2 - 0.0008083*(z-1)**3)

Air_mass=Bemporad(1/trig)	

print("Alpha:	",alpha)
print("Delta:	",delta)
print("----------------------------------------")
print("Time_Angle:			",Time_Angle)
print("Horisontal_coord: 		",Horisontal_coord)
print("Zenit_coord:			",Zenit_coord)
print("Air_mass:			",Air_mass)

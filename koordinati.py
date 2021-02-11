#!/home/lrikozavr/py_env/ML/bin/python3
# -*- coding: utf-8 -*-
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
class Observe(Star):
	def __init__(self,lambada,fi,alpha,delta):
		super(Observe,self).__init__(alpha,delta)#?
		self.lambada = lambada
		self.fi = fi
	#######################################
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
	########################################
	def S0(self,t):
		return self.StoH(self.hdtoHD(6,41,50.54841,"")*3600. + 86401.84812866*t + 0.093104*t**2 - 0.62e-5*t**3) #hour
	def S(self,s): #hour
		return (s-self.hdtoHD(0,3,56.55,"")*(self.lambada/self.hdtoHD(24,0,0,"")))
	def Time_Angle(self,ut,jd):
		#print("s",s)
		return (ut*1.002738 - self.DtoH(self.alpha) + self.lambada + self.S(self.S0(self.T(jd))))
	########################################
	def trig(self,Time_Angle):
		return sin(self.DtoR(self.fi))*sin(self.DtoR(self.delta)) + cos(self.DtoR(self.fi))*cos(self.DtoR(self.delta))*cos(self.DtoR(Time_Angle))
	def Horisontal_coord(self,Time_Angle):
		return self.RtoD(asin(self.trig(Time_Angle)))
	def Zenit_coord(self,Time_Angle):
		return self.RtoD(asec(1/self.trig(Time_Angle)))
	def Bemporad(self,Time_Angle):
		z=1/self.trig(Time_Angle)
		return (z - 0.0018167*(z-1) - 0.002875*(z-1)**2 - 0.0008083*(z-1)**3)
	########################################
	def info_abs(self):
		print("Lambda:	",self.HtoD(self.lambada))
		print("Fi:	",self.fi) 
		print("Alpha:	",self.alpha)
		print("Delta:	",self.delta)
	def info(self):
		print("Lambda: ",self.HDtohd(self.lambada,""))
		print("Fi:	",self.HDtohd(self.fi,""))
		print("Alpha:	",self.HDtohd(self.alpha,"dh"))
		print("Delta:	",self.HDtohd(self.delta,""))
	########################################



######
lambada=[2,24,55.8] #долгота
fi=["+",50,0,10] 		#широта
date=2459292.5
UT=16
######
def HtoD(h,m,s):
    return (h+m/60.+s/3600.)*15.
def DtoD(d,m,s,z):
    if (z=="-"):
        return -d-m/60.-s/3600.
    elif (z=="+"): 
        return d+m/60.+s/3600.
def HtoS(h,m,s):
	return (h*3600 + m*60 + s)

def AD(ah0,am0,as0,dd0,dm0,ds0,dz0,date):
	one = Observe(HtoS(lambada[0],lambada[1],lambada[2])/3600.,DtoD(fi[1],fi[2],fi[3],fi[0]),HtoD(ah0,am0,as0),DtoD(dd0,dm0,ds0,dz0))
	alfa=one.ALPHA(date)
	delta=one.DELTA(date)
	#one.info()
	one.info_abs()
	return alfa,delta

alpha,delta=AD(10,56,28.8,7,0,52.34,"+",date)
#alpha,delta=AD(12,35,28.3,57,5,22.32,"-",date)

user=Observe(HtoS(lambada[0],lambada[1],lambada[2])/3600.,DtoD(fi[1],fi[2],fi[3],fi[0]),alpha,delta)
#user.info()

Time_Angle=user.Time_Angle(UT,date)
Time_Angle=user.HtoD(Time_Angle)

print("Alpha:	",alpha)
print("Delta:	",delta)
print("----------------------------------------")
if (user.Horisontal_coord(Time_Angle) > (90-user.fi+user.delta)):
	print("Horisontal_coord error")
	exit()
print("Horisontal_coord: 		",user.Horisontal_coord(Time_Angle))
print("Zenit_coord:			",user.Zenit_coord(Time_Angle))
print("Air_mass:			",user.Bemporad(Time_Angle))

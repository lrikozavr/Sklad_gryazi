#!/home/lrikozavr/py_env/ML/bin/python3
# -*- coding: utf-8 -*-

'''
[[""],
 [""],
 [""],
 [""],
 [""]]
'''
alphabet=([
[["    ##"],
 ["   # #"],
 ["  ####"],
 [" #   #"],
 ["#    #"]],
[["### "],
 ["#  #"],
 ["### "],
 ["#  #"],
 ["### "]],
[[" ### "],
 ["#   #"],
 ["#    "],
 ["#   #"],
 [" ### "]],
[["#### "],
 ["#   #"],
 ["#   #"],
 ["#   #"],
 ["#### "]],
[["#####"],
 ["#    "],
 ["###  "],
 ["#    "],
 ["#####"]],
[["#####"],
 ["#    "],
 ["###  "],
 ["#    "],
 ["#    "]],
[[" #### "],
 ["#    #"],
 ["# ### "],
 ["# #  #"],
 [" #### "]],
[["#  #"],
 ["#  #"],
 ["####"],
 ["#  #"],
 ["#  #"]],
[["###"],
 [" # "],
 [" # "],
 [" # "],
 ["###"]],
[["  ###"],
 ["   # "],
 ["   # "],
 ["#  # "],
 [" ##  "]],
[["#  #"],
 ["# # "],
 ["##  "],
 ["# # "],
 ["#  #"]],
[["#   "],
 ["#   "],
 ["#   "],
 ["#   "],
 ["####"]],
[["#   #"],
 ["## ##"],
 ["# # #"],
 ["#   #"],
 ["#   #"]],
[["#   #"],
 ["##  #"],
 ["# # #"],
 ["#  ##"],
 ["#   #"]],
[[" ### "],
 ["#   #"],
 ["#   #"],
 ["#   #"],
 [" ### "]],
[["### "],
 ["#  #"],
 ["### "],
 ["#   "],
 ["#   "]],
[[" ###  "],
 ["#   # "],
 ["#   # "],
 ["#  ## "],
 [" ### #"]],
[["###  "],
 ["#  # "],
 ["###  "],
 ["#  # "],
 ["#   #"]],
[[" ####"],
 ["#    "],
 [" ### "],
 ["    #"],
 ["#### "]],
[["#####"],
 ["  #  "],
 ["  #  "],
 ["  #  "],
 ["  #  "]],
[["#   #"],
 ["#   #"],
 ["#   #"],
 ["#   #"],
 [" ### "]],
[["#   #"],
 ["#   #"],
 [" # # "],
 [" # # "],
 ["  #  "]],
[["#      #"],
 ["#      #"],
 [" # ## # "],
 [" # ## # "],
 ["  #  #  "]],
[["#   #"],
 [" # # "],
 ["  #  "],
 [" # # "],
 ["#   #"]],
[["#   #"],
 [" # # "],
 ["  #  "],
 ["  #  "],
 ["  #  "]],
[["#####"],
 ["   # "],
 [" ### "],
 [" #   "],
 ["#####"]]
 ])

number=([
[[" ## "],
 ["#  #"],
 ["#  #"],
 ["#  #"],
 [" ## "]],
[[" # "],
 ["## "],
 [" # "],
 [" # "],
 ["###"]],
[[" ### "],
 ["#   #"],
 ["  ## "],
 [" ##   "],
 ["#####"]],
[[" ### "],
 ["#   #"],
 ["  ## "],
 ["#   #"],
 [" ###"]],
[["  ##"],
 [" # #"],
 ["####"],
 ["   #"],
 ["   #"]],
[["#####"],
 ["#    "],
 ["#### "],
 ["    #"],
 ["#### "]],
[[" ####"],
 ["#    "],
 ["#### "],
 ["#   #"],
 [" ### "]],
[["#####"],
 ["   # "],
 ["  #  "],
 [" #   "],
 ["#    "]],
[[" ### "],
 ["#   #"],
 [" ### "],
 ["#   #"],
 [" ### "]],
[[" ### "],
 ["#   #"],
 [" ####"],
 ["    #"],
 [" ### "]]
])
#start
for i in range(5):
	print(str(alphabet[18][i][0])+" "+str(alphabet[19][i][0])+" "+str(alphabet[0][i][0])+" "+str(alphabet[17][i][0])+" "+str(alphabet[19][i][0]))
s1,s2,s3,s4="#","▓"," ","░"



def rep(line,s1,s2):
	line=list(line)
	result=""
	for i in range(len(line)):
		if (line[i]==s1):
			line[i]=s2
		result+=line[i]
	return result

def print_word_h(line,s1,s2,s3,s4):
	for j in range(5):
		s=""
		for i in range(len(line)):
			if i>0:
				ex=" "
			else:
				ex=""
			flag=0
			flag_sym = "eng"
			delta=97
			if(ord(line[i])>=48 and ord(line[i])<=57):
				delta = 48
				flag=1
				flag_sym = "num"
			if(ord(line[i])>=97 and ord(line[i])<=122):
				delta = 97
				flag=1
				flag_sym = "eng"
			if(flag):
				if(flag_sym == "eng"):
					s+=ex+str(alphabet[ord(line[i])-delta][j][0])
				if(flag_sym == "num"):
					s+=ex+str(number[ord(line[i])-delta][j][0])
			else:
				s+=ex
		s=rep(s,s1,s2)
		s=rep(s,s3,s4)
		print(s)

def print_word_v(line,s1,s2,s3,s4):
	for i in range(len(line)):
		flag=0
		flag_sym = "eng"
		delta=97
		if(ord(line[i])>=48 and ord(line[i])<=57):
			delta = 48
			flag=1
			flag_sym = "num"
		if(ord(line[i])>=97 and ord(line[i])<=122):
			delta = 97
			flag=1
			flag_sym = "eng"
		if(flag):
			for j in range(5):
				if(flag_sym == "eng"):
					s=str(alphabet[ord(line[i])-delta][j][0])
				if(flag_sym == "num"):
					s=str(number[ord(line[i])-delta][j][0])
				s=rep(s,s1,s2)
				s=rep(s,s3,s4)
				print(s)
		else: print()

while (1==1):
	line=str(input())
	if line=="0":
		exit()
	#line=line.split(" ")
	#print(line)
	#exit()
	print("Simbol count",len(line))
	for i in range(len(line)):
		if(ord(line[i])<48 or ord(line[i])>57):
			if((ord(line[i])<97 or ord(line[i])>122) and ord(line[i])!=32):
				print("Index: ",i,"\nProblem with:	",line[i],"\nWithout Alphabet\nTry again\nCode number:",ord(line[i]))
				exit()
	#print(ord(line[i])-97)
	#for line in line.split(" "):
	print("Change?(y/n)")
	if(input()=="y"):
		print("s1:	")
		s1=input()
		print("s2:	")
		s2=input()
		print("s3:	")
		s3=input()
		print("s4:	")
		s4=input()
	print(s1,s2,s3,s4)
	print("Horizontal/Vertical?(h,v)")
	flag=input()
	if (flag=="h"):
		print_word_h(line,s1,s2,s3,s4)
	elif (flag=="v"):
		print_word_v(line,s1,s2,s3,s4)
	else:
		print_word_v(line,s1,s2,s3,s4)
##### ####       ## ### #   # ### ##    #  ####
  #   ## ##     # #  #  ##  #  #  # #   # #    #
  #   ####     ####  #  # # #  #  #  #  # # ###
  #   ## ##   #   #  #  #  ##  #  #   # # #    #
  #   ##  ## #    # ### #   # ### #    ##  ####


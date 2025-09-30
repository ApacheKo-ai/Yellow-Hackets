import math
from decimal import Decimal
import sklearn as sk
import numpy as np
import tkinter as tk
#from PIL import Image, ImageTK

Forget = []
Destroy = []

window = tk.Tk()
window.geometry("500x200")
window.configure(bg = "black") # Probably Remove this or implement it into a theme option. Currently for Seeing Blank Space Eaiser

##################################################################################
# 1. SORT
##################################################################################

def Sort():
	values = []
	full = Entry_1.get()
	if full == "":
		return
	num = ""
	for c in range(len(full)):
		if full[c].isdecimal():
			num += str(full[c])
		elif full[c] == '.':
			num += str(full[c])
		else:
			values.append(float(num))
			num = ""
	values.append(float(num))
	values.sort()
	
	message = ""
	for x in range(len(values)):
		message += (str(values[x]) + ", ")
	message += " | Count: " + str(len(values))
	Outry.delete(1.0,tk.END)
	Outry.insert(1.0,message)
	# Empty Out and Insert Message Into It Here
	return values

##################################################################################
# 2. PERCENTILE
##################################################################################

def Percentile():
	values = Sort()
	tile = int(Entry_2.get())
	temp = (len(values))*(tile/100)
	Outry.delete(1.0,tk.END)
	Outry.insert(1.0,temp)

##################################################################################
# 3. VARIANCE AND DEVIATION
##################################################################################

def Variance_and_Deviation(type):
	total = 0
	total2 = 0

	nums = []
	full = Entry_1.get()
	if full == "":
		return
	num = ""
	for c in range(len(full)):
		if full[c].isdecimal():
			num += str(full[c])
		elif full[c] == '.':
			num += str(full[c])
		else:
			nums.append(float(num))
			total += float(num)
			num = ""
	total += float(num)
	nums.append(float(num))

	mean = float(total/len(nums))
	for x in range(len(nums)):
		total2 += pow((nums[x]-mean),2)
	if type:
		total2 /= len(nums) -1 # Population; add (-1) for Standard
	else:
		total2 /= len(nums)

	Outry.delete(1.0,tk.END)
	Outry.insert("1.0", f"Mean: {mean}\nVariance: {total2}\nDeviation: {math.sqrt(total2)}\nCV: {((math.sqrt(total2))/mean)*100}%")



##################################################################################
# 4. GROUPED MEAN AND VARIANCE
##################################################################################

def Grouped_Mean_and_Variance():
	classes = int(input("Number of Classes: "))
	size = Decimal(input("Class Size: "))
	smallest = Decimal(input("Minimum Number: "))
	largest = Decimal(input("Largest Number: "))
	start = smallest
	end = start + size
	mean = 0
	variance = 0
	deviation = 0
	num = 0
	for x in range(classes):
		print(str(start) + " | " + str(end))
		mid = (start + end)/2
		obv = Decimal(input("Observations in the " + str(x) + " Class: "))
		num += obv
		mean += (mid*obv)
		variance += (pow(mid,2) * obv)
		start = end+1 # Whole Numbers is +1, decimals is Decimal(0.1)
		end = start + size
	variance = (variance-(pow(mean,2)/num))/(num-1 ) # -1 is sample, remove it for population
	print("Mean: " + str(mean/num))
	print("Variance: " + str(variance))
	print("Deviation: " + str(math.sqrt(variance)))

##################################################################################
# 5. PROPORTIONS
##################################################################################

def Proportions():
	obv = float(input("Number of Observations: "))
	total = float(input("Number of Observations Total: "))
	sample = float(input("Sample?: "))
	pp = (obv/total)
	sp = (obv/sample)
	print("Population Proportion: " + str(pp))
	print("Sample Proportion: " + str(sp)) 

##################################################################################
# 6. CORRELATION COEFFICIENT
##################################################################################

def Corralation_Coefficient():
	dp = int(input("Data Points: "))
	x = 0
	x2 = 0
	y = 0
	y2 = 0
	num = 0
	for v in range(dp):
		xi = (float(input("X: ")))
		yi = (float(input("Y: ")))
		x += xi
		y += yi
		x2 += math.pow(xi,2)
		y2 += math.pow(yi,2)
		num += (xi * yi)

	top = ((dp*num)-(x*y))
	bottom = ((math.sqrt((dp*x2)-math.pow(x,2)))*(math.sqrt((dp*y2)-math.pow(y,2))))
	
	print("Corralation Coefficient: " + str(top/bottom))

##################################################################################
# 7. SUM OF SQUARED ERROR
##################################################################################

def Sum_of_Squared_Error():
	rows = int(input("Rows: "))
	a = float(input("A: "))
	b = float(input("B: "))
	num = 0
	for r in range(rows):
		c1 = float(input("X: "))
		c2 = float(input("Y: "))
		pred = a + (b*c2)
		err = pred - c1
		num += math.pow(err,2)
	MsE = num/(rows-2)
	Se = math.sqrt(MsE)
	print("SSE: " + str(num))
	print("MSE: " + str(MsE))
	print("SE: " + str(Se))

##################################################################################
# 8. ESTIMATE PARAMETERS
##################################################################################

def Estimate_Parameters():
	table = sk.linear_model.LinearRegression()
	rows = int(input("Number of Rows: "))
	x = []
	y = []
	for r in range(rows):
		x.append([float(input("X: "))])
		y.append(float(input("Y: ")))

	table.fit(x,y)

	print("C: " + str(table.coef_))
	print("I: " + str(table.intercept_))

##################################################################################
# 9. EVALUATING FIT OF A LINEAR MODEL
##################################################################################

def Evaluating_Fit_of_Linear_Model():
	x = 0
	y = 0
	xy = 0
	x2 = 0
	y2 = 0
	save = 0
	rows = int(input("Number of Rows: "))
	for r in range(rows):
		xx = (float(input("X: ")))
		if save == 0:
			save += xx
		yy = (float(input("Y: ")))
		x += xx
		y += yy
		xy += (xx*yy)
		x2 += math.pow(xx,2)
		y2 += math.pow(yy,2)

	slope = (rows*(xy) -(x*y))/(rows*(x2)-math.pow(x,2))
	intercept = (1/rows)*(y-(slope*x))
	difference = (intercept + ((save+1)*slope))-(intercept + (save*slope))
	CoD = math.pow((((rows*xy)-(x*y))/(math.sqrt(((rows*x2)-math.pow(x,2))*((rows*y2)-math.pow(y,2))))),2)
	MsE = CoD/(rows-2)
	print("Y-Intercept: " + str(intercept))
	print("Slope: " + str(slope))
	print("Difference: " + str(difference))
	print("COD: " + str(CoD))

##################################################################################
# 10. RESET
##################################################################################

def Reset():
	global frames, Forget, Destroy
	for col in range(10):
		window.columnconfigure(col, weight=0)
	for row in range(10): 
		window.rowconfigure(row, weight=0)
	window.columnconfigure(1, weight=1)
	window.rowconfigure(1, weight=1)
	
	for f in range(len(Forget)):
		Forget[f].grid_forget()
	for d in range(len(Destroy)):
		Destroy[d].destroy()

	for x in range(9):
	    row, col = divmod(x, 3)   # 0..2 for rows, 0..2 for columns
	    frames[x].grid(row=row + 1, column=col, sticky="nsew")

	WelcomeFrame.grid(row=0, column=0, columnspan=3, sticky = "nsew")
	Home.grid(row = 1, column = 1, sticky = "nsew")

	Entry_1.delete(0,tk.END)
	Entry_2.delete(0,tk.END)
	Entry_3.delete(0,tk.END)
	Outry.delete(1.0,tk.END)
	Forget = []
	Destroy = []

####################################################################################
# Set Up Each Set Of Objects, Try To Follow Similar Naming Conventions
# Reprogram Each Function to Work With Entries Instead of Input

Entry_1 = tk.Entry(master = window, relief = tk.SOLID)
Entry_2 = tk.Entry(master = window, relief = tk.SOLID)
Entry_3 = tk.Entry(master = window, relief = tk.SOLID)

Outry = tk.Text(master = window, relief = tk.SOLID)

Back_Button = tk.Button(master = window, relief = tk.SOLID, text = "Home", command = lambda: Reset())
Button_1 = tk.Button(master = window, relief = tk.SOLID)
Button_2 = tk.Button(master = window, relief = tk.SOLID)


def Config(task):

	if task.lower() == "sort":  ##SORT##

		l1 = tk.Label(master = window, text = "Enter Numbers Seperated By Commas")
		Outry.config(height = 4)
		Button_1.config(text = "Sort", command = lambda: Sort())
		Layout = [[False,l1,False],[False,Entry_1,False],[False,Outry,False],[Back_Button,False,Button_1]]
		for r in range(len(Layout)):
			for c in range(len(Layout[r])):
				if Layout[r][c]:
					if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
						Layout[r][c].grid(row = r, column = c-1, columnspan=3, pady = 2, sticky = "nsew")
					else:
						Layout[r][c].grid(row = r, column = c, pady = 2, sticky = "nsew")
				else:
					pass
		

		Forget.extend([Entry_1,Outry,Back_Button,Button_1])
		Destroy.extend([l1])

	elif task.lower() == "per": ##PERCENTILE##

		l1 = tk.Label(master = window, text = "↓Numbers↓")
		l2 = tk.Label(master = window, text = "↓Percentile↓")
		Outry.config(height = 1)
		Button_1.config(text = "Get Percentile", command = lambda: Percentile())
		Layout = [[False,l1,False],[False,Entry_1,False],[False,l2,False],[False,Entry_2,False],[False,Outry,False],[Back_Button,False,Button_1]]
		for r in range(len(Layout)):
			for c in range(len(Layout[r])):
				if Layout[r][c]:
					if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
						Layout[r][c].grid(row = r, column = c-1, columnspan=3, pady = 2, sticky = "nsew")
					else:
						Layout[r][c].grid(row = r, column = c, pady = 2, sticky = "nsew")
				else:
					pass
		

		Forget.extend([Entry_1,Entry_2,Outry,Back_Button,Button_1])
		Destroy.extend([l1,l2])

	elif task.lower() == "vd":  ##VARIANCE_AND_DEVIATION##

		l1 = tk.Label(master = window, text = "Enter Numbers Seperated By Commas")
		Outry.config(height = 4)
		Button_1.config(text = "Population", command = lambda: Variance_and_Deviation(False))
		Layout = [[]]
		Button_2.config(text = "Standard", command = lambda: Variance_and_Deviation(True))
		Layout = [[False,l1,False],[False,Entry_1,False],[False,Outry,False],[Back_Button,Button_1,Button_2]]
		for r in range(len(Layout)):
			for c in range(len(Layout[r])):
				if Layout[r][c]:
					if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
						Layout[r][c].grid(row = r, column = c-1, columnspan=3, pady = 2, sticky = "nsew")
					else:
						Layout[r][c].grid(row = r, column = c, pady = 2, sticky = "nsew")
				else:
					pass
		

		Forget.extend([Entry_1,Outry,Back_Button,Button_1,Button_2])
		Destroy.extend([l1])

	elif task.lower() == "gmv":
		print("GMV")
	elif task.lower() == "pro":
		print("PRO")
	elif task.lower() == "cc":
		print("CC")
	elif task.lower() == "sse":
		print("SSE")
	elif task.lower() == "ep":
		print("EP")
	elif task.lower() == "elm":
		print("ELM")
	for col in range(len(Layout[c])):
		window.columnconfigure(col, weight=1)
	for row in range(len(Layout[r])): 
		window.rowconfigure(row, weight=1)

	# Configure The Objects For Each Function, Including Setting Text and Commands.
	# Place Objects On Screen In a Location That Makes Sense
	# When the Go Button That Gets Placed Gets Pressed, Call Shoot().
	# When Reseting To Home, Set All Entries and Outry To Be Empty

###############################################################################

def press(task):
	WelcomeFrame.grid_forget()
	Home.grid_forget()
	Config(task)

	

#############################################################################

def Shoot(task):
	if task.lower() == "sort":
		print("SORT")
	elif task.lower() == "per":
		print("PER")
	elif task.lower() == "vd":
		print("VD")
	elif task.lower() == "gmv":
		print("GMV")
	elif task.lower() == "pro":
		print("PRO")
	elif task.lower() == "cc":
		print("CC")
	elif task.lower() == "sse":
		print("SSE")
	elif task.lower() == "ep":
		print("EP")
	elif task.lower() == "elm":
		print("ELM")


#################################################################################


Home = tk.Frame(master = window, bg = "black")

SorFrame = tk.Frame(master = window, bg = "black")   # Sort
PerFrame = tk.Frame(master = window, bg = "black")   # Percentile
VaDFrame = tk.Frame(master = window, bg = "black")   # Variance and Deviation
GMVFrame = tk.Frame(master = window, bg = "black")   # Grouped Mean and Variance
ProFrame = tk.Frame(master = window, bg = "black")   # Proportions
CCoFrame = tk.Frame(master = window, bg = "black")   # Correlation Coefficient
SSEFrame = tk.Frame(master = window, bg = "black")   # Sum of Squared Error
EPaFrame = tk.Frame(master = window, bg = "black")   # Estimate Parameters
ELMFrame = tk.Frame(master = window, bg = "black")   # Evaluating Fit of Linear Model


frames  = []
for x in range(9):
    frame = tk.Frame(master=Home, relief=tk.GROOVE, borderwidth=5)
    frames.append(frame)
    row, col = divmod(x, 3)   # 0..2 for rows, 0..2 for columns
    frame.grid(row=row + 1, column=col, sticky="nsew")


SorButton = tk.Button(master = frames[0], text = "Sort", command = lambda: press("sort"))
PerButton = tk.Button(master = frames[1], text = "Percentile", command = lambda: press("per"))
VaDButton = tk.Button(master = frames[2], text = "Variance_and_Deviation", command = lambda: press("vd"))
GMVButton = tk.Button(master = frames[3], text = "Grouped_Mean_and_Variance", command = lambda: press("gmv"))
ProButton = tk.Button(master = frames[4], text = "Proportions", command = lambda: press("pro"))
CCoButton = tk.Button(master = frames[5], text = "Corralation_Coefficient", command = lambda: press("cc"))
SSEButton = tk.Button(master = frames[6], text = "Sum_of_Squared_Error", command = lambda: press("sse"))
EPaButton = tk.Button(master = frames[7], text = "Estimate_Parameters", command = lambda: press("ep"))
ELMButton = tk.Button(master = frames[8], text = "Evaluating_Fit_of_Linear_Model", command = lambda: press("elm"))

buttons = [SorButton, PerButton, VaDButton, GMVButton, ProButton, CCoButton, SSEButton, EPaButton, ELMButton]

for x in range(len(buttons)):
	buttons[x].pack(fill = tk.BOTH, expand = True)

	
WelcomeFrame = tk.Frame(master = Home, relief = tk.SUNKEN, borderwidth = 5)
Welcome = tk.Label(master = WelcomeFrame, text = "Welcome to Jordan's Calculator For Statistics!\nSelect An Option To Begin!")
Welcome.pack(fill = tk.BOTH, expand = True)


WelcomeFrame.grid(row=0, column=0, columnspan=3, sticky = "nsew")
Home.grid(row = 1, column = 1, sticky = "nsew")


###############################################################################

for col in range(3):
    Home.columnconfigure(col, weight=1)
for row in range(4): 
    Home.rowconfigure(row, weight=1)


window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)

window.mainloop()


# Need to Pack each Button into Home, Then Reprogram Each Function to Work With The Entries instead of Command line Input
# Pressing the buttons should initalize the screen, then pressing the start button on that screen should Do the Calculations
# On Press, Call Start, Check Button Text, Initalize Based on that.
# On Press Of Start Button, Check Frame, Then Call the Function Based On That.

#################################################################################




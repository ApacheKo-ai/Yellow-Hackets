import math
from decimal import Decimal
import sklearn as sk
import numpy as np
import customtkinter as tk
#from PIL import Image, ImageTK

Forget = []


window = tk.CTk()
window.geometry("600x500")

tabview = tk.CTkTabview(window)
tabview.pack(fill = tk.BOTH, expand = True)
tabview.add("Calculate")
tabview.add("Settings")
Calculator = tabview.tab("Calculate")
Settings = tabview.tab("Settings")

##################################################################################
# 1. SORT
##################################################################################

def Sort():
    values = get_values(Entry_1)
    if values == None:
        return
    values.sort()

    message = ""
    for x in range(len(values)):
        message += (str(values[x]) + ", ")
    message += "\nCount: " + str(len(values))
    Outry.delete(1.0,tk.END)
    Outry.insert(1.0,message)
    # Empty Out and Insert Message Into It Here
    return values

##################################################################################
# 2. PERCENTILE
##################################################################################

def Percentile():
    values = Sort()
    if values == None:
        pass
    else: 
        if Entry_2.get() == "":
            pass
        else:
            tile = int(Entry_2.get())
        temp = (len(values))*(tile/100)
        Outry.delete(1.0,tk.END)
        Outry.insert(1.0,temp)

##################################################################################
# 3. VARIANCE AND DEVIATION
##################################################################################

def Variance_and_Deviation(type):
    total2 = 0

    nums = get_values(Entry_1)
    total = sum(nums)
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

def Grouped_Mean_and_Variance(type):
    if Entry_1.get() == "":
        pass
    else:
        size = int(Entry_1.get())

    full = Entry_2.get()
    if full == "":
        return
    num = ""
    for c in range(len(full)):
        if full[c].isdecimal():
            num += str(full[c])
        elif full[c] == '.':
            num += str(full[c])
        else:
            smallest = (float(num))
            num = ""
    if num != "":
        largest = (float(num))

    start = smallest
    end = start + size
    mean = 0
    variance = 0
    deviation = 0
    total = 0
    observations = get_values(Entry_3)

    classes = len(observations)

    for x in range(classes):
        mid = (start + end)/2
        
        total += observations[x]
        mean += (mid*observations[x])
        variance += (pow(mid,2) * observations[x])

        if str(observations[x]).split(".")[1][-1] == "0":
            start = end+1 # Whole Numbers is +1, decimals is Decimal(0.1)
        else:
            start = end + 0.1
        end = start + size

    if type:
        variance = (variance-(pow(mean,2)/total))/(total-1 ) # -1 is sample, remove it for population
    else:
        variance = (variance-(pow(mean,2)/total))/(total)

    Outry.delete(1.0,tk.END)
    Outry.insert("1.0", f"Mean: {mean/total}\nVariance: {variance}\nDeviation: {math.sqrt(variance)}")


##################################################################################
# 5. PROPORTIONS
##################################################################################

def Proportions():
    obv = 0

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
            if obv == 0:
                obv = (float(num))
            else:
                total = (float(num))
            num = ""
    if num != "":
        sample = (float(num))

    pp = (obv/total)
    sp = (obv/sample)

    Outry.delete(1.0,tk.END)
    Outry.insert("1.0", f"Population Proportion: {pp}\nSample Proportion: {sp}")

##################################################################################
# 6. CORRELATION COEFFICIENT
##################################################################################

def Corralation_Coefficient():

    xi = get_values(Entry_1)
    yi = get_values(Entry_2)

    x = 0
    x2 = 0
    y = 0
    y2 = 0
    num = 0
    for v in range(len(xi)):
        x += xi[v]
        y += yi[v]
        x2 += math.pow(xi[v],2)
        y2 += math.pow(yi[v],2)
        num += (xi[v] * yi[v])
    dp = len(xi)
    top = ((dp*num)-(x*y))
    bottom = ((math.sqrt((dp*x2)-math.pow(x,2)))*(math.sqrt((dp*y2)-math.pow(y,2))))

    Outry.delete(1.0,tk.END)
    Outry.insert("1.0", "Corralation Coefficient: " + str(top/bottom))

##################################################################################
# 7. SUM OF SQUARED ERROR
##################################################################################

def Sum_of_Squared_Error():

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
            a = (float(num))
            num = ""
    if num != "":
        b = (float(num))

    x = get_values(Entry_2)
    y = get_values(Entry_3)

    num = 0
    for r in range(len(x)):

        pred = a + (b*y[r])
        err = pred - x[r]
        num += math.pow(err,2)
    MsE = num/(len(x)-2)
    Se = math.sqrt(MsE)

    Outry.delete(1.0,tk.END)
    Outry.insert("1.0", f"SSE: {num}\nMSE: {MsE}\nSE: {Se}")

##################################################################################
# 8. ESTIMATE PARAMETERS
##################################################################################

def Estimate_Parameters():

    table = sk.linear_model.LinearRegression()

    x = get_values(Entry_1)
    y = get_values(Entry_2)

    table.fit(x,y)

    Outry.delete(1.0,tk.END)
    Outry.insert("1.0", f"C: {table.coef_}\nI: {table.intercept_}")

##################################################################################
# 9. EVALUATING FIT OF A LINEAR MODEL
##################################################################################

def Evaluating_Fit_of_Linear_Model():

    xx = get_values(Entry_1)
    yy = get_values(Entry_2)

    x = 0
    y = 0
    xy = 0
    x2 = 0
    y2 = 0
    save = 0

    rows = len(xx)
    for r in range(rows):
        
        if save == 0:
            save += xx[r]
        
        x += xx[r]
        y += yy[r]
        xy += (xx[r]*yy[r])
        x2 += math.pow(xx[r],2)
        y2 += math.pow(yy[r],2)

    slope = (rows*(xy) -(x*y))/(rows*(x2)-math.pow(x,2))
    intercept = (1/rows)*(y-(slope*x))
    difference = (intercept + ((save+1)*slope))-(intercept + (save*slope))
    CoD = math.pow((((rows*xy)-(x*y))/(math.sqrt(((rows*x2)-math.pow(x,2))*((rows*y2)-math.pow(y,2))))),2)
    MsE = CoD/(rows-2)

    Outry.delete(1.0,tk.END)
    Outry.insert("1.0", f"Y-Intercept: {intercept}\nSlope: {slope}\nDifference: {difference}\nCOD: {CoD}")

##################################################################################
# 10. RESET
##################################################################################

def Reset():
    global frames, Forget
    for col in range(10):
        Calculator.columnconfigure(col, weight=0)
    for row in range(10): 
        Calculator.rowconfigure(row, weight=0)
    Calculator.columnconfigure(1, weight=1)
    Calculator.rowconfigure(1, weight=1)
    
    for f in range(len(Forget)):
        Forget[f].grid_forget()


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

def get_values(Entry_0):
    values = []
    full = Entry_0.get()
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
    if num != "":
        values.append(float(num))
    return values

####################################################################################

Entry_1 = tk.CTkEntry(master = Calculator, font=("Arial", 18))
Entry_2 = tk.CTkEntry(master = Calculator, font=("Arial", 18))
Entry_3 = tk.CTkEntry(master = Calculator, font=("Arial", 18))

Outry = tk.CTkTextbox(master = Calculator)

Back_Button = tk.CTkButton(master = Calculator, text = "Home", command = lambda: Reset())
Button_1 = tk.CTkButton(master = Calculator)
Button_2 = tk.CTkButton(master = Calculator)

####################################################################################

def option_callback(choice):
    if choice == "System" or choice == "Dark" or choice == "Light":
        tk.set_appearance_mode(choice)

Theme_label = tk.CTkLabel(Settings, text="Theme")
Theme_label.pack(pady = 8)
Theme_menu = tk.CTkOptionMenu(Settings, values=["System", "Dark", "Light"], command=option_callback)
Theme_menu.pack(pady=2)

####################################################################################

def Config(task):

    if task.lower() == "sort":  ##SORT##

        Entry_1.configure(placeholder_text = "Enter Numbers Seperated By Commas")
        Outry.configure(height = 88)
        Button_1.configure(text = "Sort", command = lambda: Sort())
        Layout = [[False,Entry_1,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Outry,Back_Button,Button_1])

    elif task.lower() == "per": ##PERCENTILE##

        Entry_1.configure(placeholder_text = "Numbers")
        Entry_2.configure(placeholder_text = "Percentile")
        Outry.configure(height = 22)
        Button_1.configure(text = "Get Percentile", command = lambda: Percentile())
        Layout = [[False,Entry_1,False],[False,Entry_2,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Entry_2,Outry,Back_Button,Button_1])

    elif task.lower() == "vd":  ##VARIANCE_AND_DEVIATION##

        Entry_1.configure(placeholder_text = "Enter Numbers Seperated By Commas")
        Outry.configure(height = 88)
        Button_1.configure(text = "Population", command = lambda: Variance_and_Deviation(False))
        Button_2.configure(text = "Standard", command = lambda: Variance_and_Deviation(True))
        Layout = [[False,Entry_1,False],[False,Outry,False],[Back_Button,Button_1,Button_2]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Outry,Back_Button,Button_1,Button_2])

    elif task.lower() == "gmv": ##GROUPED_MEAN_AND_VARIANCE##

        Outry.configure(height = 66)
        Button_1.configure(text = "Population", command = lambda: Grouped_Mean_and_Variance(False))
        Button_2.configure(text = "Standard", command = lambda: Grouped_Mean_and_Variance(True))
        Entry_1.configure(placeholder_text = "Size of a Class")
        Entry_2.configure(placeholder_text = "Smallest Number, Largest Number")
        Entry_3.configure(placeholder_text = "Observations per Class")
        Layout = [[False,Entry_1,False],[False,Entry_2,False],[False,Entry_3,False],[False,Outry,False],[Back_Button,Button_1,Button_2]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Entry_2,Entry_3,Outry,Back_Button,Button_1,Button_2])

    elif task.lower() == "pro":  ##PROPORTIONS## Entry_1.configure(placeholder_text = ) Add Starting Here

        Entry_1.configure(placeholder_text = "Observations, Total Observations, Sample Size")
        Outry.configure(height = 44)
        Button_1.configure(text = "Calculate", command = lambda: Proportions())
        Layout = [[False,Entry_1,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Outry,Back_Button,Button_1])

    elif task.lower() == "cc":  ##CORALATION_COEFFICENT##

        Entry_1.configure(placeholder_text = "X Values")
        Entry_2.configure(placeholder_text = "Y Values")
        Outry.configure(height = 22)
        Button_1.configure(text = "Calculate", command = lambda: Corralation_Coefficient())
        Layout = [[False,Entry_1,False],[False,Entry_2,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Entry_2,Outry,Back_Button,Button_1])

    elif task.lower() == "sse": ##SUM_OF_SQUARED_ERROR##

        Outry.configure(height = 66)
        Button_1.configure(text = "Calculate", command = lambda: Sum_of_Squared_Error())
        Entry_1.configure(placeholder_text = "A, B")
        Entry_2.configure(placeholder_text = "X Values")
        Entry_3.configure(placeholder_text = "Y Values")
        Layout = [[False,Entry_1,False],[False,Entry_2,False],[False,Entry_3,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Entry_2,Entry_3,Outry,Back_Button,Button_1])

    elif task.lower() == "ep":  ##ESTIMATE_PARAMETERS##

        Entry_1.configure(placeholder_text = "X Values")
        Entry_2.configure(placeholder_text = "Y Values")
        Outry.configure(height = 44)
        Button_1.configure(text = "Calculate", command = lambda: Estimate_Parameters())
        Layout = [[False,Entry_1,False],[False,Entry_2,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Entry_2,Outry,Back_Button,Button_1])

    elif task.lower() == "elm":  ##EVALUATING_FIT_OF_LINEAR_MODEL##

        Entry_1.configure(placeholder_text = "X Values")
        Entry_2.configure(placeholder_text = "Y Values")
        Outry.configure(height = 88)
        Button_1.configure(text = "Calculate", command = lambda: Evaluating_Fit_of_Linear_Model())
        Layout = [[False,Entry_1,False],[False,Entry_2,False],[False,Outry,False],[Back_Button,False,Button_1]]
        for r in range(len(Layout)):
            for c in range(len(Layout[r])):
                if Layout[r][c]:
                    if (c == 1) and not (Layout[r][c-1]) and not (Layout[r][c+1]):
                        Layout[r][c].grid(row = r, column = c-1, columnspan=3, padx = 2, pady = 2, sticky = "nsew")
                    else:
                        Layout[r][c].grid(row = r, column = c,padx = 2, pady = 2, sticky = "nsew")
                else:
                    pass
        
        Forget.extend([Entry_1,Entry_2,Outry,Back_Button,Button_1])

    for col in range(len(Layout[c])):
        Calculator.columnconfigure(col, weight=1)
    for row in range(len(Layout[r])): 
        Calculator.rowconfigure(row, weight=1)


###############################################################################

def press(task):
    WelcomeFrame.grid_forget()
    Home.grid_forget()
    Config(task)

#############################################################################

Home = tk.CTkFrame(master = Calculator)

frames  = []
for x in range(9):
    frame = tk.CTkFrame(master=Home)
    frames.append(frame)
    row, col = divmod(x, 3)   # 0..2 for rows, 0..2 for columns
    frame.grid(row=row + 1, column=col, padx = 2, pady = 2, sticky="nsew")


SorButton = tk.CTkButton(master = frames[0], text = "Sort", command = lambda: press("sort"))
PerButton = tk.CTkButton(master = frames[1], text = "Percentile", command = lambda: press("per"))
VaDButton = tk.CTkButton(master = frames[2], text = "Variance_and_Deviation", command = lambda: press("vd"))
GMVButton = tk.CTkButton(master = frames[3], text = "Grouped_Mean_and_Variance", command = lambda: press("gmv"))
ProButton = tk.CTkButton(master = frames[4], text = "Proportions", command = lambda: press("pro"))
CCoButton = tk.CTkButton(master = frames[5], text = "Corralation_Coefficient", command = lambda: press("cc"))
SSEButton = tk.CTkButton(master = frames[6], text = "Sum_of_Squared_Error", command = lambda: press("sse"))
EPaButton = tk.CTkButton(master = frames[7], text = "Estimate_Parameters", command = lambda: press("ep"))
ELMButton = tk.CTkButton(master = frames[8], text = "Evaluating_Fit_of_Linear_Model", command = lambda: press("elm"))

buttons = [SorButton, PerButton, VaDButton, GMVButton, ProButton, CCoButton, SSEButton, EPaButton, ELMButton]

for x in range(len(buttons)):
    buttons[x].pack(fill = tk.BOTH, expand = True)

    
WelcomeFrame = tk.CTkFrame(master = Home)
Welcome = tk.CTkLabel(master = WelcomeFrame, text = "Welcome to Jordan's Calculator For Statistics!\nSelect An Option To Begin!")
Welcome.pack(fill = tk.BOTH, expand = True)


WelcomeFrame.grid(row=0, column=0, columnspan=3, sticky = "nsew")
Home.grid(row = 1, column = 1, sticky = "nsew")


###############################################################################

for col in range(3):
    Home.columnconfigure(col, weight=1)
for row in range(4): 
    Home.rowconfigure(row, weight=1)
"""
for col in range(3):
    Calculator.columnconfigure(col, weight=1)
for row in range(4):
    Calculator.rowconfigure(row, weight=1)
"""
Calculator.columnconfigure(1, weight=1)
Calculator.rowconfigure(1, weight=1)

window.mainloop()


# Need to Pack each Button into Home, Then Reprogram Each Function to Work With The Entries instead of Command line Input
# Pressing the buttons should initalize the screen, then pressing the start button on that screen should Do the Calculations
# On Press, Call Start, Check Button Text, Initalize Based on that.
# On Press Of Start Button, Check Frame, Then Call the Function Based On That.

#################################################################################




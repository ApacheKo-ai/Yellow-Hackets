###################IMPORTS##########################################################
## THOMAS WAS HERE
from google import genai
import tkinter as tk

############VARIABLES################################################################

client = genai.Client(api_key = "AIzaSyDfQcy77_mKj9UaKgl0TGvca35czMg4II0")

window = tk.Tk()
window.title("Ai_Asking")
window.geometry("")

#############FUNCTIONS################################################################

def ask(event):
    question = entry.get()
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=(question)
    )
    outry.delete(0,tk.END)
    outry.insert(0,response.text)

def start():
    eBox.grid(row = 1,column = 0, sticky = "nsew")
    dBox.grid(row = 1,column = 2, sticky = "nsew")
    dtBox.grid(row = 2, column = 1, sticky = "nsew")
    etBox.grid(row = 0,column = 1, sticky = "nsew")

    help_desk.pack(fill = tk.BOTH, expand = True)
    buttone.pack(fill = tk.BOTH, expand = True)
    buttond.pack(fill = tk.BOTH, expand = True)
    entry.pack(fill = tk.BOTH, expand = True)
    outry.pack(fill = tk.BOTH, expand = True)

    lBox.grid_forget()
    sBox.grid_forget()

    home.pack_forget()
    welcome.pack_forget()
    sButton.pack_forget()

############OBJECT_CREATION###################################################################

help_desk = tk.Frame(master = window, bg = "black")
eBox = tk.Frame(master=help_desk, relief = tk.GROOVE, borderwidth = 5)
dBox = tk.Frame(master=help_desk, relief = tk.GROOVE, borderwidth = 5)
etBox = tk.Frame(master = help_desk, relief = tk.SUNKEN, borderwidth = 5)
dtBox = tk.Frame(master = help_desk, relief = tk.SUNKEN, borderwidth = 5)

buttone = tk.Button(master = eBox, text="Ask")
buttond = tk.Button(master = dBox, text = "   ")

entry = tk.Entry(master = etBox, fg="black", bg="white")    
outry = tk.Entry(master = dtBox, fg = "black", bg = "white")

buttone.bind("<Button-1>", ask)

############START_WINDOW###############################################################

home = tk.Frame(master = window, bg = "blue")
lBox = tk.Frame(master = home, relief = tk.GROOVE, borderwidth = 5)
sBox = tk.Frame(master = home, relief = tk.GROOVE, borderwidth = 5)

welcome = tk.Label(master = lBox, text = "Welcome to the Help Desk, Click the Button to Begin!")
sButton = tk.Button(master = sBox, text = "Begin", command = start)

###########PLACEMENT###################################################################

"""
eBox.grid(row = 1,column = 0, sticky = "nsew")
dBox.grid(row = 1,column = 2, sticky = "nsew")
dtBox.grid(row = 2, column = 1, sticky = "nsew")
etBox.grid(row = 0,column = 1, sticky = "nsew")

help_desk.pack(fill = tk.BOTH, expand = True)
buttone.pack(fill = tk.BOTH, expand = True)
entry.pack(fill = tk.BOTH, expand = True)
outry.pack(fill = tk.BOTH, expand = True)
"""

lBox.grid(row = 0, column = 1, sticky = "nsew")
sBox.grid(row = 2, column = 1, sticky = "nsew")

home.pack(fill = tk.BOTH, expand = True)
welcome.pack(fill = tk.BOTH, expand = True)
sButton.pack(fill = tk.BOTH, expand = True)

#########LOOP#####################################################################

for x in range(0,3):
    for y in range(0,3):
        help_desk.columnconfigure(x,weight = 1)
        help_desk.rowconfigure(y,weight = 1)

window.mainloop()




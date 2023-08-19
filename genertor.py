from jsonConfig import JsonConfig
from pysettings import tk

PATH = None

amounts = [
    "1 Tasse",
    "1/2 Tasse",
    "1/4 Tasse",
    "2 TL",
    "4 TL",
    "10 St.",
    "2 St.",
    "1 St.",
    "1/2 St.",
    "1/4 St.",
]

raw = {
      "name":"",
      "nor_portion":"",
      "small_portion":"",
      "chds":[],
      "test_data": {
        "tested":False,
        "first_test_day":"",
        "test_level":0,
        "result":None,
        "notes":[]
      }
    }

def setFile(e):
    global PATH
    path = tk.FileDialog.openFile(master)
    if path.endswith(".txt"):
        PATH = path
    else:
        tk.SimpleDialog.askError("Not a valid File!")


def save(e):
    if PATH is None: return
    data = raw.copy()
    data["chds"] = []
    data["name"] = nameE.getValue()
    data["nor_portion"] = norA.getValue()
    data["small_portion"] = smallA.getValue()

    if ch1.getState(): data["chds"].append("Fruchtose")
    if ch2.getState(): data["chds"].append("Oligos")
    if ch3.getState(): data["chds"].append("Polyole")

    js = JsonConfig.fromDict(data)
    strjs = js.getPrettifyData()+","

    file = open(PATH, "r")
    con = file.read()
    file.close()

    file = open(PATH, "w")
    file.write(con+"\n"+strjs)
    file.close()

    nameE.clear()
    smallA.clear()
    norA.clear()
    ch1.setValue(0)
    ch2.setValue(0)
    ch3.setValue(0)


master = tk.Tk()
master.setTitle("Generator")
master.setWindowSize(400, 400)

nameE = tk.TextEntry(master)
nameE.setText("Name: ")
nameE.place(0, 0, height=25, width=300)

tk.Label(master).setText("NormalAmount:").placeRelative(fixHeight=25, fixWidth=150, fixY=25, fixX=0)
norA = tk.DropdownMenu(master, readonly=False, optionList=amounts)
norA.placeRelative(fixHeight=25, fixWidth=150, fixY=25, fixX=150)

tk.Label(master).setText("SmallAmount:").placeRelative(fixHeight=25, fixWidth=150, fixY=50, fixX=0)
smallA = tk.DropdownMenu(master, readonly=False, optionList=amounts)
smallA.placeRelative(fixHeight=25, fixWidth=150, fixY=50, fixX=150)

ch1 = tk.Checkbutton(master).setText("Fruchtose").placeRelative(fixHeight=25, fixWidth=150, fixY=75)
ch2 = tk.Checkbutton(master).setText("Oligos").placeRelative(fixHeight=25, fixWidth=150, fixY=75, fixX=150)
ch3 = tk.Checkbutton(master).setText("Polyole").placeRelative(fixHeight=25, fixWidth=150, fixY=100)

master.bind(save, tk.EventType.RETURN)
tk.Button(master).setText("Save").placeRelative(fixHeight=25, fixWidth=150, fixY=125).setCommand(save)
tk.Button(master).setText("Set file...").placeRelative(fixHeight=25, fixWidth=150, fixY=125, fixX=150).setCommand(setFile)
master.mainloop()

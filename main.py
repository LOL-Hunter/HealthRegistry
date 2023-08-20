from pysettings import tk
from backend import DataLoader, FoodTableDataSource
import ui

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.foodData = DataLoader()
        self.loadView()
        self.fillListbox(self.foodData.getFoods())

    def loadView(self):
        self.mainView = ui.load_view("main")
        self.propView = ui.load_view("prop")

        self.mainView.present("full_screen")



    def onListBoxSelect(self, e):
        print(e)


       #prop = self.foodData.getProperties(selected)

       #self.textT.setText(prop)
        # textview.text = prop


    def fillListbox(self, _input:list):
        listBox = self.mainView["food_view"]
        listBox.data_source = FoodTableDataSource(_input)
        listBox.reload_data()

if __name__ == '__main__':
    GUI().mainloop()

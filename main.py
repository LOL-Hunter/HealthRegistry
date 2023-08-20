from backend import DataLoader, FoodTableDataSource
import ui

class GUI:
    def __init__(self):

        self.foodData = DataLoader()
        self.loadView()
        self.fillListbox(self.foodData.getFoods())
        self.mainView.present("full_screen")

    def loadView(self):
        self.mainView = ui.load_view("main")
        self.propView = ui.load_view("prop")


       #prop = self.foodData.getProperties(selected)

       #self.textT.setText(prop)
        # textview.text = prop


    def fillListbox(self, _input:list):
        listBox = self.mainView["food_view"]
        listBox.data_source = FoodTableDataSource(_input)
        listBox.reload_data()

class Event:
    @staticmethod
    def onListBoxSelect(dataSource):
        foodName = dataSource.name
        




if __name__ == '__main__':
    GUI()

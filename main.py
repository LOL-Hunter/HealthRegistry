from backend import DataLoader, FoodTableDataSource
import ui

class GUI:
    CURRENT_FOOD_TABLE_DATA_SRC = None
    GUI_INS = None
    def __init__(self):
        GUI.GUI_INS = self
        self.foodData = DataLoader()
        self.loadView()
        self.fillListbox(self.foodData.getFoods())
        #self.mainView.present("full_screen")

    def loadView(self):
        self.mainView = ui.load_view("main")
        self.propView = ui.load_view("prop")

        self.navView = ui.NavigationView(self.mainView)
        self.navView.width = 600
        self.navView.height = 400
        self.navView.present("full_screen", hide_title_bar=True)

        close = ui.ButtonItem()
        close.image = ui.Image.named('ionicons-close-24')
        close.action = self.close
        self.mainView.left_button_items = [close]



       #prop = self.foodData.getProperties(selected)

       #self.textT.setText(prop)
        # textview.text = prop

    def onListBoxSelect(self, dataSource):
        index = dataSource.selected_row
        food = GUI.CURRENT_FOOD_TABLE_DATA_SRC.food[index]
        prop = self.foodData.getPropertiesByData(food)


        GUI.GUI_INS.navView.push_view(GUI.GUI_INS.propView)


    def close(self, e):
        self.navView.close()

    def fillListbox(self, _input:list):
        listBox = self.mainView["food_view"]
        listBox.data_source = GUI.CURRENT_FOOD_TABLE_DATA_SRC = FoodTableDataSource(self, _input)
        listBox.delegate = GUI.CURRENT_FOOD_TABLE_DATA_SRC
        listBox.reload_data()



if __name__ == '__main__':
    GUI()

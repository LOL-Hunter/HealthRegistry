from backend import DataLoader, FoodTableDataSource, WidgetConfigurator
import ui

class GUI:
    CURRENT_FOOD_TABLE_DATA_SRC = None
    GUI_INS = None
    def __init__(self):
        GUI.GUI_INS = self
        self.selectedMode = None
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

        text = self.propView["prop_text_view"]
        WidgetConfigurator.configTextView(text)
        WidgetConfigurator.configTextView(self.mainView["info_text_view"])

        seg = self.mainView["select_view_mode_seg"]
        seg.action = self.onSegChange

       #prop = self.foodData.getProperties(selected)

       #self.textT.setText(prop)
        # textview.text = prop

    def onListBoxSelect(self, fdata:dict):
        prop = self.foodData.getPropertiesByData(fdata)
        text = self.propView["prop_text_view"]
        text.text = prop

        GUI.GUI_INS.navView.push_view(GUI.GUI_INS.propView)


    def close(self, e):
        self.navView.close()

    def onSegChange(self, sender):
        sc = sender.superview['select_view_mode_seg']
        selected_text = sc.segments[sc.selected_index]

        if selected_text == "All" and self.selectedMode != "All":
            self.selectedMode = "All"
            self.fillListbox(self.foodData.getFoods())
        elif selected_text == "Untested" and self.selectedMode != "Untested":
            self.selectedMode = "Untested"
            self.fillListbox(self.foodData.getUnTestedFoods())
        elif selected_text == "Tested" and self.selectedMode != "Tested":
            self.selectedMode = "Tested"
            self.fillListbox(self.foodData.getTestedFoods())

    def fillListbox(self, _input:list):
        listBox = self.mainView["food_view"]
        listBox.data_source = GUI.CURRENT_FOOD_TABLE_DATA_SRC = FoodTableDataSource(self, _input)
        listBox.delegate = GUI.CURRENT_FOOD_TABLE_DATA_SRC
        listBox.reload_data()

    def updateInfo(self):
        text = self.mainView["info_text_view"]
        text.text = self.foodData.getInfo()


if __name__ == '__main__':
    GUI()

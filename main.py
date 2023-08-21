from backend import DataLoader, FoodTableDataSource, WidgetConfigurator, Utilities, TextViewDelegate
import ui

class GUI:
    GUI_INS = None
    def __init__(self):
        GUI.GUI_INS = self
        self.selectedMode = None
        self.searchWord = ""
        self.foodData = DataLoader()
        self.loadView()
        self.fillListbox(self.foodData.getFoods())
        #self.mainView.present("full_screen")
        self.navView.present("full_screen", hide_title_bar=True)

    def loadView(self):
        self.mainView = ui.load_view("main")
        self.propView = ui.load_view("prop")

        self.navView = ui.NavigationView(self.mainView)
        self.navView.width = 600
        self.navView.height = 400


        close = ui.ButtonItem()
        close.image = ui.Image.named('ionicons-close-24')
        close.action = self.close
        self.mainView.left_button_items = [close]

        text = self.propView["prop_text_view"]
        WidgetConfigurator.configTextView(text)
        WidgetConfigurator.configTextView(self.mainView["info_text_view"])

        seg = self.mainView["select_view_mode_seg"]
        seg.action = self.onSegChange

        search_field = self.mainView["search_field"]
        search_field.delegate = TextViewDelegate()

        clear_search = self.mainView["search_clear"]
        clear_search.action = self.clearSearch

    def clearSearch(self):
        search_field = self.mainView["search_field"]
        search_field.text = ""

    def onSearch(self, w):
        self.searchWord = w.text
        self.updateListbox()

    def onListBoxSelect(self, fdata:dict):
        prop = self.foodData.getPropertiesByData(fdata)
        text = self.propView["prop_text_view"]
        text.text = prop

        GUI.GUI_INS.navView.push_view(GUI.GUI_INS.propView)

    def close(self, e):
        self.navView.close()

    def onSegChange(self, sender):
        sc = sender.superview['select_view_mode_seg']
        self.selectedMode = sc.segments[sc.selected_index]

    def updateListbox(self):
        if self.selectedMode == "All" and self.selectedMode != "All":
            self.fillListbox(Utilities.search(self.foodData.getFoods(), self.searchWord))
        elif self.selectedMode == "Untested" and self.selectedMode != "Untested":
            self.fillListbox(Utilities.search(self.foodData.getUnTestedFoods(), self.searchWord))
        elif self.selectedMode == "Tested" and self.selectedMode != "Tested":
            self.fillListbox(Utilities.search(self.foodData.getTestedFoods(), self.searchWord))

    def fillListbox(self, _input:list):
        listBox = self.mainView["food_view"]
        dataSource = FoodTableDataSource(self, _input)
        listBox.data_source = dataSource
        listBox.delegate = dataSource
        listBox.reload_data()

    def updateInfo(self):
        text = self.mainView["info_text_view"]
        text.text = self.foodData.getInfo()


if __name__ == '__main__':
    GUI()

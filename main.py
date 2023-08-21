from backend import DataLoader, FoodTableDataSource, WidgetConfigurator, Utilities, TextViewDelegate, DayTableDataSource
import ui
from console import hud_alert
class GUI:
    GUI_INS = None
    def __init__(self):
        GUI.GUI_INS = self
        self.selectedMode = "All"
        self.selectedFood = None
        self.searchWord = ""
        self.selectedDay = 0
        self.foodData = DataLoader()
        self.loadView()
        self.fillListbox(self.foodData.getFoods())
        self.updateInfo()
        #self.mainView.present("full_screen")
        self.navView.present("full_screen", hide_title_bar=True)

    def loadView(self):
        self.mainView = ui.load_view("main")
        self.propView = ui.load_view("prop")
        self.daySView = ui.load_view("day_select")
        self.editDView = ui.load_view("edit_day")

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
        search_field.delegate = TextViewDelegate(self.onSearch)

        clear_search = self.mainView["search_clear"]
        clear_search.action = self.clearSearch

        show_act_test = self.mainView["show_active_test_button"]
        show_act_test.action = self.showActiveTest

        start_test = self.propView["start_button"]
        start_test.action = self.startTest


    def clearSearch(self, e):
        search_field = self.mainView["search_field"]
        search_field.text = ""
        self.updateListbox()

    def showActiveTest(self, e):
        if self.foodData.getActiveFood() is None:
            hud_alert("Kein Test Aktiv!")
            return
        day_list = self.daySView["days_tableview"]
        dataSource = DayTableDataSource(self, self.foodData.getActiveFood())
        day_list.data_source = dataSource
        day_list.delegate = dataSource
        day_list.reload_data()
        self.navView.push_view(self.daySView)

    def startTest(self, e):
        if self.foodData.getActiveFood() is not None:
            hud_alert("Anderer Test noch aktiv!")
            return
        if self.selectedFood["test_data"]["tested"]:
            hud_alert("Lebensmittel bereits getestet!")
            return
        self.foodData.setFoodActive(self.selectedFood["name"])
        self.foodData.save()
        hud_alert(f"Nahrungsmittel '{self.selectedFood['name']}' gestartet!")
        self.navView.pop_view(True)

    def onDayBoxSelect(self, dayIndex):
        self.selectedDay = dayIndex
        


        self.navView.push_view(self.editDView)

    def onSearch(self, w):
        self.searchWord = w.text
        self.updateListbox()

    def onListBoxSelect(self, fdata:dict):
        self.selectedFood = fdata
        prop = self.foodData.getPropertiesByData(fdata)
        text = self.propView["prop_text_view"]
        text.text = prop

        self.navView.push_view(self.propView)

    def close(self, e):
        self.navView.close()

    def onSegChange(self, sender):
        sc = sender.superview['select_view_mode_seg']
        self.selectedMode = sc.segments[sc.selected_index]
        self.updateListbox()

    def updateListbox(self):
        if self.selectedMode == "All":
            self.fillListbox(Utilities.search(self.foodData.getFoods(), self.searchWord))
        elif self.selectedMode == "Untested":
            self.fillListbox(Utilities.search(self.foodData.getUnTestedFoods(), self.searchWord))
        elif self.selectedMode == "Tested":
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

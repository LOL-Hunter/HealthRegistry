from backend import DataLoader, FoodTableDataSource, WidgetConfigurator, Utilities, TextViewDelegate, DayTableDataSource
import ui
from console import hud_alert, alert
from datetime import datetime


class GUI:
    GUI_INS = None
    def __init__(self):
        GUI.GUI_INS = self
        self.selectedMode = "All"
        self.selectedFood = None
        self.activeFood = None
        self.searchWord = ""
        self.selectedDay = 0
        self.foodData = DataLoader()
        self.activeFood =  self.foodData.getActiveFood()
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

        save_day = self.editDView["save_button"]
        save_day.action = self.onSaveDay


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
        self.activeFood = self.selectedFood
        self.foodData.setFoodActive(self.activeFood["name"])
        self.foodData.save()
        hud_alert(f"Nahrungsmittel '{self.activeFood['name']}' gestartet!")
        self.navView.pop_view(True)

    def onDayBoxSelect(self, dayIndex):
        self.selectedDay = dayIndex
        days = self.activeFood["test_data"]["test_days"]
        if len(days) >= dayIndex-1:
            hud_alert("Bitte erst die voherigen Tage eintragen!")
            return
        if len(days) >= dayIndex+1: # day already exixts -> not create new on
            date = days[dayIndex]
            notices = self.activeFood["test_data"]["notices"]
            noticesTextView = self.editDView["notices_textview"]
            noticesTextView.text = notices[date]

            d, m, y = date.split(".")

            datePicker = self.editDView["date_picker"]
            datePicker.date = datetime(y, m, d)
        else:
            pass
        self.navView.push_view(self.editDView)

    def onSaveDay(self, e):
        # check if date already exists
        # take date and create notice
        days = self.activeFood["test_data"]["test_days"]
        datePicker = self.editDView["date_picker"]
        date:datetime = datePicker.date
        str_date = f'{0+date.day if len(str(date.day))==1 else date.day}.{0+date.month if len(str(date.month))==1 else date.month}.{date.year}'
        if len(days) >= self.selectedDay + 1:
            days[self.selectedDay] = str_date
        else:
            days.append(str_date)
        noticesTextView = self.editDView["notices_textview"]
        self.activeFood["test_data"]["notices"][str_date] = noticesTextView.text
        self.foodData.save()
        self.updateInfo()
        self.navView.pop_view(True)
        self.navView.pop_view(True)

    def onOK(self, e):
        out = alert("Warning", "Bist du sicher, dass du den Test mit 'OK' beenden moechtest?", "Ok", "Cancel")
        if out == 2: return
        self.activeFood["test_data"]["tested"] = True
        self.activeFood["test_data"]["result"] = True
        self.foodData.setFoodActive(None)
        self.activeFood = None
        self.foodData.save()
        self.updateInfo()

    def onNOK(self, e):
        out = alert("Warning", "Bist du sicher, dass du den Test mit 'NICHT OK' beenden moechtest?", "Ok", "Cancel")
        if out == 2: return
        self.activeFood["test_data"]["tested"] = True
        self.activeFood["test_data"]["result"] = False
        self.foodData.setFoodActive(None)
        self.activeFood = None
        self.foodData.save()
        self.updateInfo()

    def onSearch(self, w):
        self.searchWord = w.text
        self.updateListbox()

    def onListBoxSelect(self, fdata:dict):
        self.selectedFood = fdata
        prop = self.foodData.getPropertiesByData(fdata)
        text = self.propView["prop_text_view"]
        text.text = prop
        text = self.daySView["info_text_view"]
        text.text = self.foodData.getInfo()

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

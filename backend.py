from pysettings.jsonConfig import JsonConfig
import ui

class DataLoader:
    def __init__(self):
        self.js = JsonConfig.loadConfig("data.json")

    def __getitem__(self, item):
        return self.js[item]

    def __setitem__(self, key, value):
        self.js[key] = value

    def getFoods(self)->[]:
        return self.js["food"]

    def isFoodActive(self)->bool:
        return self["active"] is not None

    def getActiveFood(self):
        return self.getFoodByName(self["active"])

    def getFoodByName(self, name):
        for food in self["food"]:
            if food["name"] == name:
                return food

    def setFoodActive(self, name):
        self["active"] = name

    def resetFoodTest(self, name):
        food = self.getFoodByName(name)
        if food is not None:
            food["test_data"] = {
            "tested": False,
            "first_test_day": "",
            "test_level": 0,
            "result": None,
            "notes": []
        }
    def getProperties(self, name):
        food = self.getFoodByName(name)
        return self.getPropertiesByData(food)

    def getPropertiesByData(self, food):
        if food is not None:
            test = food["test_data"]
            return f'Name:{food["name"]}\nTested: {test["tested"]}\nResult: {test["result"]}'
        return ""

    def save(self):
        self.js.save()



class WidgetConfigurator:
    @staticmethod
    def configTextView(tv):
        tv.editable = False
        tv.selectable = False

class FoodTableDataSource:
    def __init__(self, _ins, food):
        self.ins = _ins
        self.food = food
    def tableview_number_of_sections(self, tableview):
        return 1
    def tableview_number_of_rows(self, tableview, section):
        return len(self.food)

    def tableview_did_select(self, tableview, section, row):
        print(tableview, section, row)
        self.ins.onListBoxSelect(section)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.food[row]["name"]
        return cell

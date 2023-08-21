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

    def getTestedFoods(self)->[]:
        l = []
        for food in self.getFoods():
            testData = food["test_data"]
            if testData["tested"]:
                l.append(food)
        return l

    def getUnTestedFoods(self)->[]:
        l = []
        for food in self.getFoods():
            testData = food["test_data"]
            if not testData["tested"]:
                l.append(food)
        return l

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
            "test_days": [],
            "test_level": 0,
            "result": None,
            "notes": {}
        }
    def getProperties(self, name):
        food = self.getFoodByName(name)
        return self.getPropertiesByData(food)

    def getPropertiesByData(self, food):
        if food is not None:
            test = food["test_data"]
            if not test["test_level"]:
                return "\n".join([
                    f'== Food Data ==',
                    f'Name: {food["name"]}',
                    f'Normale Portion: {food["nor_portion"]}',
                    f'Kleine Portion: {food["small_portion"]}',
                    f'Kohlenhydrahte: {food["chds"]}',
                    f'',
                    f'== Test Data ==',
                    f'Keine Testdaten vorhanden!',
                    f'Tested: {test["tested"]}'
                    f'Result: {test["result"]}'
                ])
            return "\n".join([
                f'== Food Data ==',
                f'Name: {food["name"]}',
                f'Normale Portion: {food["nor_portion"]}',
                f'Kleine Portion: {food["small_portion"]}',
                f'Kohlenhydrahte: {food["chds"]}',
                f'',
                f'== Test Data ==',
                f'Test Abgeschlossen: {test["tested"]}'
                f'Test Abgeschlossen am: {test["test_days"][-1] if len(test["test_days"]) > 0 and test["test_level"] >= 3 else "-"}'
                f'Test Ergebniss: {test["result"]}'
                f'',
                f'== Notizen ==',
                self.getNotices(food)
            ])
        return "No properties available!\n\t\t:("

    def getNotices(self, food):
        testData = food["test_data"]
        days = testData["test_days"]
        notes = testData["notes"]
        out = f''
        for day in days:
            out += f'\t* {day}\n'
            for line in notes[day].splitlines():
                out += f'\t\t'+line+"\n"
            if notes[day] == "": out += f'\t\tKeine Notizen vorhanden!\n'
        return out if out != "" else "Keine Notizen vorhanden!"


    def getInfo(self):
        tested = 0
        untested = 0
        active = self.getActiveFood()["name"] if self.getActiveFood()["name"] is not None else "No Food Active!"
        length = len(self.getFoods())
        for food in self.getFoods():
            testData = food["test_data"]
            if testData["tested"]: tested += 1
            else: untested += 1
        return f"Total: {length}\nTested: {tested}\nUntested: {untested}\nActive: {active}"






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
        self.ins.onListBoxSelect(self.food[row])

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.food[row]["name"]
        return cell

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
            if not len(test["test_days"]):
                return "\n".join([
                    f'== Lebensmittel Daten ==',
                    f'Name: {food["name"]}',
                    f'Normale Portion: {food["nor_portion"]}',
                    f'Kleine Portion: {food["small_portion"]}',
                    f'Kohlenhydrahte: {food["chds"]}',
                    f'',
                    f'== Test Daten ==',
                    f'Keine Testdaten vorhanden!',
                ])
            return "\n".join([
                f'== Lebensmittel Daten ==',
                f'Name: {food["name"]}',
                f'Normale Portion: {food["nor_portion"]}',
                f'Kleine Portion: {food["small_portion"]}',
                f'Kohlenhydrahte: {food["chds"]}',
                f'',
                f'== Test Daten ==',
                f'Test Abgeschlossen: {test["tested"]}',
                f'Test Abgeschlossen am: {test["test_days"][-1] if len(test["test_days"]) > 0 else "-"}',
                f'Test Ergebniss: {test["result"]}',
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
        active = self.getActiveFood()["name"] if self.getActiveFood() is not None else "Kein Nahrungsmittel activ!"
        length = len(self.getFoods())
        for food in self.getFoods():
            testData = food["test_data"]
            if testData["tested"]: tested += 1
            else: untested += 1
        return f"Total: {length}\nGetestet: {tested}\nNicht Getestet: {untested}\nAktiv: {active}"

    def save(self):
        self.js.save()

class Utilities:
    @staticmethod
    def search(_list, word):
        out = []
        for food in _list:
            if word.lower() in food["name"].lower(): out.append(food)
        return out

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

class DayTableDataSource:
    def __init__(self, _ins, food):
        self.ins = _ins
        self.food = food

    def tableview_number_of_sections(self, tableview):
        return 1
    def tableview_number_of_rows(self, tableview, section):
        return 3

    def tableview_did_select(self, tableview, section, row):
        self.ins.onDayBoxSelect(row)

    def tableview_cell_for_row(self, tableview, section, row):
        days = self.food["test_data"]["test_days"]
        length = len(days)
        if length >= row+1:
            info = f'{days[row]}'
        else:
            info = "Nicht eingetragen!"
        cell = ui.TableViewCell()
        cell.text_label.text = f'Day {row+1} '+info
        return cell



class TextViewDelegate:
    def __init__(self, hook):
        self.hook = hook
    def textfield_should_begin_editing(self, textview):
        return True
    def textfield_did_begin_editing(self, textview):
        pass
    def textfield_did_end_editing(self, textview):
        pass
    def textfield_should_change(self, textview, range, replacement):
        return True
    def textfield_did_change(self, textview):
        self.hook(textview)
    def textfield_did_change_selection(self, textview):
        pass

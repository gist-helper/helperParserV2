import openpyxl
import codecs
import json
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)
class dish:
    title: str
    meal_date: str
    kind_of_meal: str
    menu: str

class meals:
    meal: dish

    def __init__(self) -> None:
        self.meal = dish()
        

# excel_path = "./2학생회관.xlsx"

# wb = openpyxl.load_workbook(excel_path)
# sh = wb.worksheets[0]

# for j in range(3):
    # jsonFile = codecs.open(f'{j}.json', 'w+', 'utf-8')

breakfast = meals()
breakfast.meal.title="제2학생회관1층"
breakfast.meal.meal_date="2015-03-14"
breakfast.meal.kind_of_meal = "조식"
breakfast.meal.menu="콩밥"
print(json.dumps(breakfast.__dict__,ensure_ascii=False,cls=ComplexEncoder))
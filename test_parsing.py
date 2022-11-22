import openpyxl
import json

from meal import MealWrapper, kind_of_meals, slot_endpoints

from util import ComplexEncoder, sanitize_menu

file_path = "./2학생회관.xlsx"

workbook = openpyxl.load_workbook(file_path)
sheet = workbook.worksheets[0]

def parse_slot(column_day,row_slot):    
    day = sheet.cell(row=2, column=column_day).value
    menus = ""
    for row_menus in range(slot_endpoints[row_slot][0], slot_endpoints[row_slot][1]):
        menus += sanitize_menu((sheet.cell(row=row_menus, column=column_day).value)) + '\n'
    meal_wrapper = MealWrapper()
    meal_wrapper.meal.title="제2학생회관1층"
    meal_wrapper.meal.meal_date = day.strftime('%Y-%m-%d')
    meal_wrapper.meal.kind_of_meal = kind_of_meals[row_slot]
    meal_wrapper.meal.menu = menus.rstrip('\n')
    return json.dumps(meal_wrapper.__dict__,indent=4,ensure_ascii=False,cls=ComplexEncoder)

def test_first_day_breakfast():
    assert parse_slot(4,0) == '{\n    "meal": {\n        "title": "제2학생회관1층",\n        "meal_date": "2022-09-26",\n        "kind_of_meal": "조식",\n        "menu": "미역국\\n흰밥*김치볶음밥\\n계란후라이\\n비엔나버섯볶음\\n춘권튀김\\n청포도푸딩\\n야채샐러드\\n배추김치\\n시리얼*우유\\n토스트*잼"\n    }\n}'

def test_last_day_dinner():
    assert parse_slot(10,2) =='{\n    "meal": {\n        "title": "제2학생회관1층",\n        "meal_date": "2022-10-02",\n        "kind_of_meal": "석식",\n        "menu": "흑미밥\\n순두부탕\\n동그랑땡전\\n고구마맛탕\\n양배추초무침\\n양념깻잎지\\n배추김치"\n    }\n}'
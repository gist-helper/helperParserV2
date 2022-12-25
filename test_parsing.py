import json

import openpyxl

from parsing import parse_slot

file_path = "./2학생회관.xlsx"

workbook = openpyxl.load_workbook(file_path)
sheet = workbook.worksheets[0]


FIRST_DAY_BREAKFAST = '{\n    "meal": {\n        "title": "제2학생회관1층",\n        "meal_date": "2022-09-26",\n        "kind_of_meal": "조식",\n        "menu": "미역국\\n흰밥*김치볶음밥\\n계란후라이\\n비엔나버섯볶음\\n춘권튀김\\n청포도푸딩\\n야채샐러드\\n배추김치\\n시리얼*우유\\n토스트*잼"\n    }\n}'
LAST_DAY_DINNER = '{\n    "meal": {\n        "title": "제2학생회관1층",\n        "meal_date": "2022-10-02",\n        "kind_of_meal": "석식",\n        "menu": "흑미밥\\n순두부탕\\n동그랑땡전\\n고구마맛탕\\n양배추초무침\\n양념깻잎지\\n배추김치"\n    }\n}'


def test_parsing_first_day_breakfast():
    parse_slot(sheet, 0, 4, 0)

    with open("./09_26_b_kor.json") as f:
        data = f.read()
        json_data = json.loads(data)

    assert json.dumps(json_data, indent=4, ensure_ascii=False) == FIRST_DAY_BREAKFAST


def test_parsing_last_day_dinner():
    parse_slot(sheet, 0, 10, 2)

    with open("./10_02_d_kor.json") as f:
        data = f.read()
        json_data = json.loads(data)

    assert json.dumps(json_data, indent=4, ensure_ascii=False) == LAST_DAY_DINNER

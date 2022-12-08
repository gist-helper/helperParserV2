import openpyxl
import json

from meal import (
    MealWrapper,
    KIND_OF_MEALS,
    SLOT_ENDPOINTS,
    SLOT_FILENAMES_POSTFIX,
    KIND_OF_RESTAURANTS,
)

from util import ComplexEncoder, sanitize_menu

FILE_PATH = ["./1학생회관.xlsx", "./1학생회관2층.xlsx", "./2학생회관.xlsx"]


def parse_slot(sheet, column_day: int, row_slot: int):
    day = sheet.cell(row=2, column=column_day).value
    menus = ""
    for row_menus in range(SLOT_ENDPOINTS[row_slot][0], SLOT_ENDPOINTS[row_slot][1]):
        menus += (
            sanitize_menu((sheet.cell(row=row_menus, column=column_day).value)) + "\n"
        )

    meal_wrapper = MealWrapper(
        title=KIND_OF_RESTAURANTS[2],
        meal_date=day.strftime("%Y-%m-%d"),
        kind_of_meal=KIND_OF_MEALS[row_slot],
        menu=menus.rstrip("\n"),
    )

    default_name = day.strftime("%m_%d") + SLOT_FILENAMES_POSTFIX[row_slot]
    jsonFile = open(f"./{default_name}.json", "w+", encoding="utf-8")
    json.dump(
        meal_wrapper.__dict__,
        jsonFile,
        indent=4,
        ensure_ascii=False,
        cls=ComplexEncoder,
    )


if __name__ == "__main__":
    workbook = openpyxl.load_workbook(FILE_PATH[2])
    sheet = workbook.worksheets[0]

    for column_day in range(4, 11):
        for row_slot in range(3):
            parse_slot(sheet, column_day, row_slot)

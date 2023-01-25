import re
import json
import math
from meal import BREAKFAST, LUNCH, DINNER
from meal import DATE_LEN
from meal import ALGY_ING

def parsing_date(time_index: int, data_sheet: list):
    date = str(data_sheet[time_index])
    return date[:DATE_LEN] if len(date) > DATE_LEN else date

def parsing_breakfast(row_range: list, data_sheet: list, langType: int):
    menu = ""
    for i in range(row_range[0], row_range[1]):
        algy = add_allergy(data_sheet[i], langType)
        menu_oneline = sanitize_menu(data_sheet[i])
        menu += menu_oneline + algy + "\n"
    return menu

def parsing_lunch(row_range: list, data_sheet: list, langType: int):
    menu = ""
    for i in range(row_range[0], row_range[1]):
        #TODO generally
        if i == 20 and type(data_sheet[i]) == str:
            menu += "\n \\코너\\ \n\n"            
        
        algy = add_allergy(data_sheet[i], langType)
        menu_oneline = sanitize_menu(data_sheet[i])
        menu += menu_oneline + algy
        
        #TODO generally
        if type(data_sheet[i]) == str:
            menu += "\n"
    return menu

def parsing_dinner(row_range: list, data_sheet: list, langType: int):
    menu = ""
    for i in range(row_range[0], row_range[1]):
        algy = add_allergy(data_sheet[i], langType)
        menu_oneline = sanitize_menu(data_sheet[i])
        menu += menu_oneline + algy + "\n"
    return menu

parsing_meal = {
    BREAKFAST: parsing_breakfast,
    LUNCH: parsing_lunch,
    DINNER: parsing_dinner
}

def add_allergy(menu: str, langType: int) -> str:
    if menu == None:
        return ""
    if type(menu) != str:
        return ""
    algy_ing = ALGY_ING[langType]
    algy = ""
    algy_list = re.findall(r'\d+', menu)
    for algy_num_str in algy_list:
        algy_num = int(algy_num_str)
        algy += (algy_ing[algy_num - 1] + ", ") if algy_num < len(list(algy_ing)) else ""  
    
    algy = algy[:-2] if len(algy) > 2 else algy    
    algy = "({})".format(algy) if len(algy) > 0 else ""
    return algy

def sanitize_menu(menu: str):
    if menu == None:
        return ""
    if type(menu) != str:
        return ""
    return menu.rstrip("0123456789. ")

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)

import re
import json
import math
from meal import BREAKFAST, LUNCH, DINNER, SPECIAL
from meal import DATE_LEN, DATE_1st ,DATE_2nd
from meal import ALGY_ING_1, ALGY_ING_2

def parsing_date(time_index: int, data_sheet: list):
    date = str(data_sheet[time_index])
    return date[:DATE_LEN] if len(date) > DATE_LEN else date

def parsing_menu(row_range: list, data_sheet: list, langType: int, bldgType :int):
    menu = ""
    for i in range(row_range[0], row_range[1]):
        algy = add_allergy(data_sheet[i], langType, bldgType)
        menu_oneline = sanitize_menu(data_sheet[i])
        menu += menu_oneline + algy
        menu += "\n" if len(menu_oneline) > 0 else "";
    return menu

def parsing_breakfast(endpoint: list, data_sheet: list, langType: int, dateType: int, bldgType :int):
    row_range = endpoint[BREAKFAST]
    menu = parsing_menu(row_range, data_sheet, langType, bldgType)
    special = ""
    return menu, special

def parsing_lunch(endpoint: list, data_sheet: list, langType: int, dateType: int, bldgType:int):
    row_range = endpoint[LUNCH]
    menu = parsing_menu(row_range, data_sheet, langType, bldgType)
    special =""
    if bldgType == 0 & langType ==0 : #1학 고정메뉴
     special ="돈까스정식(수제돈까스* 스프*모닝빵*후식음료*샐러드*단무지*배추김치) [돼지고기]\n"
    elif bldgType == 2: #2학 스페셜메뉴
        row_range = endpoint[SPECIAL]
        special = parsing_menu(row_range, data_sheet, langType, bldgType)       
    return menu, special

def parsing_dinner(endpoint: list, data_sheet: list, langType: int, dateType: int, bldgType:int):
    row_range = endpoint[DINNER]
    menu = parsing_menu(row_range, data_sheet, langType, bldgType)
    special = ""
    return menu, special

parsing_meal = {
    BREAKFAST: parsing_breakfast,
    LUNCH: parsing_lunch,
    DINNER: parsing_dinner,
}

def add_allergy(menu: str, langType: int ,bldgType: int) -> str:
    if menu == None:
        return ""
    if type(menu) != str:
        return ""
    if bldgType == 0: #1학 알러지 체크
        algy_ing = ALGY_ING_1[langType]
    elif bldgType == 2: #2학 알러지 체크
        algy_ing = ALGY_ING_2[langType]
    algy = ""
    algy_list = re.findall(r'\d+', menu)
    for algy_num_str in algy_list:
        algy_num = int(algy_num_str)
        algy += (algy_ing[algy_num - 1] + ", ") if algy_num < len(list(algy_ing)) else ""  
    
    algy = algy[:-2] if len(algy) > 2 else algy    
    algy = "[{}]".format(algy) if len(algy) > 0 else ""
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

import json
import pandas as pd
from meal import Meal
from meal import KOR, ENG
from meal import BREAKFAST, LUNCH, DINNER
from meal import BLDG1_1ST, BLDG1_2ND, BLDG2_1ST 
from meal import DATE_LEN, DATE
from meal import MEAL_KIND
from meal import BLDG_KIND
from meal import EXCEL_COL_BLDG, INDEX_ENDPOINTS, DATE_INDEX
from util import ComplexEncoder, sanitize_menu
from util import parsing_date, parsing_meal 

def parsing(excel_path: str, bldgType: int, langType: int):
    col        = EXCEL_COL_BLDG [bldgType]
    endpoint   = INDEX_ENDPOINTS[bldgType]
    bldg       = BLDG_KIND      [langType][bldgType]
    time_index = DATE_INDEX     [bldgType]
    
    sheet = pd.read_excel(excel_path, sheet_name=langType, 
                          index_col=None, header=None, names=col)
    
    parsing_result = []
    for (dateType, date_str) in enumerate(DATE):
        date_sheet = sheet[date_str]
        date = parsing_date(time_index, date_sheet)
        for kindType in [BREAKFAST, LUNCH, DINNER]:
            kind = MEAL_KIND[langType][kindType]
            menu = parsing_meal[kindType](endpoint[kindType], date_sheet, langType)
            meal = Meal(bldgType, langType, dateType, kindType, 
                    bldg, date, kind, menu)
            parsing_result.append(meal.__dict__)        
    
    return parsing_result
        
if __name__ == "__main__":
    excel_path = "./2학생회관.xlsx"
    parsing_result = []
    parsing_result.extend(parsing(excel_path, BLDG2_1ST, KOR)) #2학 1층, 한글
    parsing_result.extend(parsing(excel_path, BLDG2_1ST, ENG)) #2학 1층, 영어
    print(parsing_result)
    
    jsonFile = open("./2nd1floor_meal.json", "w", encoding="utf-8")
    json.dump(parsing_result, jsonFile, indent=4,
        ensure_ascii=False, cls=ComplexEncoder)
    
    #TODO post to server
    None
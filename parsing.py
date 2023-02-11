import sys
import os
from os.path import exists 
import requests
import json
import pandas as pd
from meal import Meal
from meal import KOR, ENG
from meal import BREAKFAST, LUNCH, DINNER
from meal import BLDG1_1ST, BLDG1_2ND, BLDG2_1ST 
from meal import DATE_LEN, DATE_2nd,DATE_1st
from meal import MEAL_KIND
from meal import BLDG_KIND
from meal import EXCEL_COL_BLDG, INDEX_ENDPOINTS, DATE_INDEX
from util import ComplexEncoder, sanitize_menu
from util import parsing_date, parsing_meal 

def parsing(excel_path: str, bldgType: int, langType: int) -> list:
    col        = EXCEL_COL_BLDG [bldgType]
    endpoint   = INDEX_ENDPOINTS[bldgType]
    bldg       = BLDG_KIND      [langType][bldgType]
    time_index = DATE_INDEX     [bldgType]
    
    sheet = pd.read_excel(excel_path, sheet_name=langType, 
                          index_col=None, header=None, names=col, engine='openpyxl')
    parsing_result = []
    if bldgType == 0: #1학
        xl = pd.read_excel(excel_path, sheet_name=None,
                           index_col=None, header=None, names=col, engine='openpyxl')
        last_sheet = list(xl.keys())[-2]
        sheet = xl[last_sheet]

        for (dateType, date_str) in enumerate(DATE_1st):
            date_sheet = sheet[date_str]
            date = parsing_date(time_index, date_sheet)
            for kindType in [BREAKFAST, LUNCH, DINNER]:
                kind = MEAL_KIND[langType][kindType]
                menu, special = parsing_meal[kindType](endpoint, date_sheet, langType, dateType, bldgType)
                meal = Meal(bldgType, langType, dateType, kindType, 
                        bldg, date, kind, menu, special)
                parsing_result.append(meal.__dict__)        

        return parsing_result

    elif bldgType == 2: #2학
        for (dateType, date_str) in enumerate(DATE_2nd):
            date_sheet = sheet[date_str]
            date = parsing_date(time_index, date_sheet)
            for kindType in [BREAKFAST, LUNCH, DINNER]:
                kind = MEAL_KIND[langType][kindType]
                menu, special = parsing_meal[kindType](endpoint, date_sheet, langType, dateType, bldgType)
                meal = Meal(bldgType, langType, dateType, kindType, 
                        bldg, date, kind, menu, special)
                parsing_result.append(meal.__dict__) 
        return parsing_result
           

def parsingTest():
    excel_dir_path = "./excel"
    parsing_result = []
    print("-------------------------------------------------")
    print("parsing xlsx to json...")
    for excel_filename in os.listdir(excel_dir_path):
        excel_path = os.path.join(excel_dir_path, excel_filename)
        parsing_result.extend(parsing(excel_path, BLDG2_1ST, KOR)) #2학 1층, 한글
        parsing_result.extend(parsing(excel_path, BLDG2_1ST, ENG)) #2학 1층, 영어
    print("-------------------------------------------------")
    print("saving json...")
    jsonFile = open("./2nd1floor_meal.json", "w", encoding="utf-8")
    json.dump(parsing_result, jsonFile, indent=4,
        ensure_ascii=False, cls=ComplexEncoder)
    print("-------------------------------------------------")    
    
if __name__ == "__main__":
    Mode = 0
    if Mode == 0:
        excel_path_1 = "./1학생회관.xlsx"
        excel_path_2 = "./2학생회관.xlsx"
        parsing_result_1 = []
        parsing_result_2 = []
        print("-------------------------------------------------")
        print("parsing xlsx to json...")
        if exists(excel_path_1):
            parsing_result_1.extend(parsing(excel_path_1, BLDG1_1ST, KOR)) #1학 1층, 한글
            #parsing_result.extend(parsing(excel_path, BLDG1_1ST, ENG)) #1학 1층, 영어
        if exists(excel_path_2):
            parsing_result_2.extend(parsing(excel_path_2, BLDG2_1ST, KOR)) #2학 1층, 한글
            parsing_result_2.extend(parsing(excel_path_2, BLDG2_1ST, ENG)) #2학 1층, 영어
        print("-------------------------------------------------")
        if len(sys.argv) == 1:
            # no url, save to local as json
            print("-------------------------------------------------")
            print("saving json...")
            if exists(excel_path_1):
                jsonFile = open("./1nd1floor_meal.json", "w", encoding="utf-8")
                json.dump(parsing_result_1, jsonFile, indent=4,
                    ensure_ascii=False, cls=ComplexEncoder)        
            if exists(excel_path_2):
                jsonFile = open("./2nd1floor_meal.json", "w", encoding="utf-8")
                json.dump(parsing_result_2, jsonFile, indent=4,
                    ensure_ascii=False, cls=ComplexEncoder)
            print("-------------------------------------------------")
        elif len(sys.argv) == 2:
            # post to server
            url = sys.argv[1]
            print("-------------------------------------------------")
            print("send to server...")
            if url[0:4] != "http":
                url = "http://localhost:8080/meals/test"
                requests.post(url, data={"testStr": "Hello World!"})
            else:
                for meal_result in parsing_result_1:
                    print(meal_result)
                    response = requests.post(url, json=meal_result)
                    print(response)
                    print()
                for meal_result in parsing_result_2:
                    print(meal_result)
                    response = requests.post(url, json=meal_result)
                    print(response)
                    print()
            print("-------------------------------------------------")
    elif Mode == 1:
        parsingTest()
import sys
import os
from os.path import exists
import requests
import json
import pandas as pd
from meal import Meal, INDEX_ENDPOINTS_BLDG1_EXCEPT
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
    col           = EXCEL_COL_BLDG [bldgType]
    endpoint      = INDEX_ENDPOINTS[bldgType]
    bldg          = BLDG_KIND      [langType][bldgType]
    time_index    = DATE_INDEX     [bldgType]
    start_col_idx = col[0]
    end_col_idx   = col[1]

    parsing_result = []

    # 1학 1층 한글
    if bldgType == BLDG1_1ST and langType == 0:
        xl = pd.read_excel(excel_path, sheet_name=None,
                           index_col=None, header=None, names=None, engine='openpyxl')

        # 맨 뒤에서 2번째 sheet가 이번주 sheet
        last_sheet = list(xl.keys())[-2]
        sheet = xl[last_sheet]

        # 짝수 column만 사용
        sheet_keys = sheet.keys()[start_col_idx : end_col_idx]
        sheet_keys = sheet_keys[0::2]

        for (dateType, date_str) in enumerate(sheet_keys):
            date_sheet = sheet[date_str]
            date = parsing_date(time_index, date_sheet)
            for kindType in [BREAKFAST, LUNCH, DINNER]:
                kind = MEAL_KIND[langType][kindType]
                menu, special = parsing_meal[kindType](endpoint, date_sheet, langType, dateType, bldgType)
                meal = Meal(bldgType, langType, dateType, kindType,
                            bldg, date, kind, menu, special)
                parsing_result.append(meal.__dict__)
        return parsing_result

    # 1학 1층 영어
    elif bldgType == BLDG1_1ST and langType == 1:
        sheet = pd.read_excel(excel_path, sheet_name=0,
                              index_col=None, header=None, names=None, engine='openpyxl')

        # 짝수 column만 사용
        sheet_keys = sheet.keys()[start_col_idx: end_col_idx]
        sheet_keys = sheet_keys[0::2]

        for (dateType, date_str) in enumerate(sheet_keys):
            date_sheet = sheet[date_str]
            date = parsing_date(time_index, date_sheet)
            for kindType in [BREAKFAST, LUNCH, DINNER]:
                kind = MEAL_KIND[langType][kindType]
                menu, special = parsing_meal[kindType](endpoint, date_sheet, langType, dateType, bldgType)
                meal = Meal(bldgType, langType, dateType, kindType,
                            bldg, date, kind, menu, special)
                parsing_result.append(meal.__dict__)
        return parsing_result

    # 1학 2층
    elif bldgType == BLDG1_2ND:
        sheet = pd.read_excel(excel_path, sheet_name=0,
                              index_col=None, header=None, names=None, engine='openpyxl')

        for (dateType, date_str) in enumerate(sheet.keys()[start_col_idx : end_col_idx]):
            date_sheet = sheet[date_str]
            date = parsing_date(time_index, date_sheet)
            for kindType in [LUNCH]:
                kind = MEAL_KIND[langType][kindType]
                menu, special = parsing_meal[kindType](endpoint, date_sheet, langType, dateType, bldgType, INDEX_ENDPOINTS_BLDG1_EXCEPT)
                meal = Meal(bldgType, langType, dateType, kindType,
                            bldg, date, kind, menu, special)
                parsing_result.append(meal.__dict__)
        return parsing_result

    # 2학
    elif bldgType == BLDG2_1ST:
        sheet = pd.read_excel(excel_path, sheet_name=langType,
                              index_col=None, header=None, names=None, engine='openpyxl')

        for (dateType, date_str) in enumerate(sheet.keys()[start_col_idx : end_col_idx]):
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
    with open('config.json') as f:
        config = json.load(f)
    if Mode == 0:
        filepath_bldg1_1_kor = config['filepath_bldg1_1_kor']
        filepath_bldg1_1_eng = config['filepath_bldg1_1_eng']
        filepath_bldg1_2_kor = config['filepath_bldg1_2_kor']
        filepath_bldg1_2_eng = config['filepath_bldg1_2_eng']
        filepath_bldg2       = config['filepath_bldg2']

        parsing_result = []
        print("-------------------------------------------------")
        print("parsing xlsx to json...")

        if exists(filepath_bldg1_1_kor) and exists(filepath_bldg1_1_eng):
            parsing_result.extend(parsing(filepath_bldg1_1_kor, BLDG1_1ST, KOR)) #1학 1층, 한글
            parsing_result.extend(parsing(filepath_bldg1_1_eng, BLDG1_1ST, ENG)) #1학 1층, 영어
            None
        if exists(filepath_bldg1_2_kor) and exists(filepath_bldg1_2_eng):
            parsing_result.extend(parsing(filepath_bldg1_2_kor, BLDG1_2ND, KOR)) #1학 2층, 한글
            parsing_result.extend(parsing(filepath_bldg1_2_eng, BLDG1_2ND, ENG)) #1학 2층, 영어
            None
        if exists(filepath_bldg2):
            parsing_result.extend(parsing(filepath_bldg2, BLDG2_1ST, KOR)) #2학 1층, 한글
            parsing_result.extend(parsing(filepath_bldg2, BLDG2_1ST, ENG)) #2학 1층, 영어
            None

        print("-------------------------------------------------")

        if len(sys.argv) == 1:
            # no url, save to local as json
            print("-------------------------------------------------")
            print("saving json...")
            jsonFile = open("./meal.json", "w", encoding="utf-8")
            json.dump(parsing_result, jsonFile, indent=4,
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
                for meal_result in parsing_result:
                    print(meal_result)
                    response = requests.post(url, json=meal_result)
                    print(response)
                    print()
            print("-------------------------------------------------")

    elif Mode == 1:
        parsingTest()
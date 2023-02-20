class Meal:
    bldgType: int
    langType: int
    dateType: int
    kindType: int
    bldg: str
    date: str
    kind: str
    menu: str
    special: str

    def __init__(self, bldgType, langType, dateType, kindType,
                 bldg, date, kind, menu, special) -> None:
        self.bldgType = bldgType
        self.langType = langType
        self.dateType = dateType
        self.kindType = kindType
        self.bldg = bldg
        self.date = date
        self.kind = kind
        self.menu = menu
        self.special = special


class MealWrapper:
    meal: Meal

    def __init__(self) -> None:
        self.meal = Meal()


# constant
KOR = 0
ENG = 1

BLDG1_1ST = 0
BLDG1_2ND = 1
BLDG2_1ST = 2

BREAKFAST = 0
LUNCH = 1
DINNER = 2
SPECIAL = 3

DATE_LEN = 10
DATE_1st = ["Mon", "Tue", "Wed", "Thr", "Fri"]  # 1학 요일
DATE_2nd = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]  # 2학 요일

# kind of meal
MEAL_KIND_KOR = ["조식",  # 0
                 "중식",  # 1
                 "석식"]  # 2
MEAL_KIND_ENG = ["Breakfast",  # 0
                 "Lunch",  # 1
                 "Dinner"]  # 2

# kind of building according to building type
BLDG_KIND_KOR = ["1학생회관 1층",  # 0
                 "1학생회관 2층",  # 1
                 "2학생회관 1층"]  # 2
BLDG_KIND_ENG = ["Student Union Bldg.1 1st floor",  # 0
                 "Student Union Bldg.1 2nd floor",  # 1
                 "Student Union Bldg.2 1st floor"]  # 2

# excel column according to building type
# EXCEL_COL_BLDG0 = ["A", "B", "Mon", "Mon", "Tue", "Tue", "Wed", "Wed", "Thr", "Thr", "Fri", "Fri"]  # Bldg.1 1st
# EXCEL_COL_BLDG1 = ["A", "Mon", "Tue", "Wed", "Thr", "Fri"]  # Bldg.1 2nd
# EXCEL_COL_BLDG2 = ["A", "B", "C", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]  # Bldg.2 1st
'''
column 예외 존재 (2023.2.6의 1학1층한글 엑셀보면 쓸모없는 col이 있을 수 있음)
이를 위해 요일 있는 행의 index로 접근
'''
EXCEL_COL_BLDG0 = [2, 11]
EXCEL_COL_BLDG0_EXCEPT = []
EXCEL_COL_BLDG1 = [1, 6]
EXCEL_COL_BLDG2 = [3, 10]

DATE_INDEX_BLDG0 = 4  # Bldg.1 1st
DATE_INDEX_BLDG1 = 1  # Bldg.1 2nd
DATE_INDEX_BLDG2 = 1  # Bldg.2 1st

INDEX_ENDPOINTS_BLDG0 = [[5, 15], [15, 22], [23, 30], [22, 23]]  # Bldg.1 1st
INDEX_ENDPOINTS_BLDG1 = [[0, 0], [2, 12], [0, 0], [0, 0]]        # Bldg.1 2nd
INDEX_ENDPOINTS_BLDG1_EXCEPT = [4, 6] # 1학2층 엑셀은 숨겨진 행(5,7번) 존재하고 dummy 들어가있어 제외해야함.
INDEX_ENDPOINTS_BLDG2 = [[2, 12], [12, 20], [22, 29], [20, 22]]  # Bldg.2 1st

# allergy type according to allergy code
ALGY_1_ING_KOR = ["난류", "우유", "메밀", "대두", "땅콩", "밀",
                  "새우", "돼지고기", "닭고기", "쇠고기", "오징어",
                  "고등어", "조개류", "토마토", "아황산염"]
ALGY_1_ING_ENG = ["egg", ",milk", "buckwheat", "soybean", "peanut", "wheat",
                  "shrimp", "pork", "chicken", "beef", "squid",
                  "mackerel", "shellfish", "tomato", "sulgite"]
ALGY_2_ING_KOR = ["계란류", "우유", "메밀", "땅콩", "대두",
                  "밀", "고등어", "게", "새우", "돼지고기",
                  "복숭아", "토마토", "아황산류", "호두", "닭고기",
                  "쇠고기", "오징어", "조개류", "잣"]
ALGY_2_ING_ENG = ["egg", "milk", "buckwheat", "peanut", "soybean",
                  "wheat", "mackerel", "crab", "shrimp", "pork",
                  "peach", "tomato", "sulgite", "walnut", "chicken",
                  "beef", "squid", "shellfish", "pine nut"]

# [langType]
ALGY_ING_1 = [ALGY_1_ING_KOR, ALGY_1_ING_ENG]
ALGY_ING_2 = [ALGY_2_ING_KOR, ALGY_2_ING_ENG]

# [langType][kindType]
MEAL_KIND = [MEAL_KIND_KOR, MEAL_KIND_ENG]

# [langType][bldgType]
BLDG_KIND = [BLDG_KIND_KOR, BLDG_KIND_ENG]

# [bldgType]
EXCEL_COL_BLDG = [EXCEL_COL_BLDG0, EXCEL_COL_BLDG1, EXCEL_COL_BLDG2]
DATE_INDEX = [DATE_INDEX_BLDG0, DATE_INDEX_BLDG1, DATE_INDEX_BLDG2]
INDEX_ENDPOINTS = [INDEX_ENDPOINTS_BLDG0, INDEX_ENDPOINTS_BLDG1, INDEX_ENDPOINTS_BLDG2]

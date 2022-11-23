class Meal:
    title: str
    meal_date: str
    kind_of_meal: str
    menu: str

    def __init__(self, title, meal_date, kind_of_meal, menu):
        self.title = title
        self.meal_date = meal_date
        self.kind_of_meal = kind_of_meal
        self.menu = menu


class MealWrapper:
    meal: Meal

    def __init__(self, title, meal_date, kind_of_meal, menu) -> None:
        self.meal = Meal(title, meal_date, kind_of_meal, menu)


KIND_OF_MEALS = ["조식", "중식", "석식"]
KIND_OF_RESTAURANTS = ["제1학생회관1층", "제1학생회관2층", "제2학생회관1층"]

SLOT_ENDPOINTS = [(3, 13), (13, 23), (23, 30)]
SLOT_FILENAMES_POSTFIX = ["_b_kor", "_l_kor", "_d_kor"]

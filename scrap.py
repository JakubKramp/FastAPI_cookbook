import time

from selenium import webdriver
from bs4 import BeautifulSoup
import re

url = "https://www.omnicalculator.com/health/dri"


class Scrapper:
    @staticmethod
    def set_value(profile, key, value):
        if type(value) is int:
            profile.__setattr__(profile, key, value)
            return
        elif value.find(" mg") >= 0:
            profile.__setattr__(key, int(value.split("mg")[0]))
            return
        elif value.find(" grams") >= 0:
            value = value.strip(" grams")
        if value.find("-"):
            profile.__setattr__(key, int(sum(map(int, value.split("-"))) / 2))
            return
        profile.__setattr__(key, value)

    d = {
        "Carbohydrates": "carbohydrates",
        "calories": "calories",
        "Fat": "fat",
        "Protein": "protein",
        "Sodium": "sodium",
        "Potassium": "potassium",
        "Total fiber": "fiber",
    }

    @staticmethod
    def get_age(age):
        return "19-50 years"

    @staticmethod
    def get_DRI(profile):
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        driver = webdriver.Chrome(executable_path="opt/selenium/chromedriver", options=op)
        driver.get(url)
        time.sleep(2)
        sex_choice = driver.find_element(value="react-select-2--value-item")
        driver.execute_script(f'arguments[0].innerHTML = "{profile.sex}";', sex_choice)
        age_choice = driver.find_element(value="react-select-3--value-item")
        driver.execute_script(f'arguments[0].innerHTML = "{Scrapper.get_age(profile.age)}";', age_choice)
        time.sleep(2)
        try:
            button = driver.find_elements(by="css selector", value="[class=fc-button-label]")
            button[0].click()
        except Exception:
            pass
        elems = driver.find_elements(by="css selector", value="[aria-label=Weight]")
        elems[0].send_keys(profile.weight)
        elems = driver.find_elements(by="css selector", value="[aria-label=Height]")
        elems[0].send_keys(profile.height)
        activity_choice = driver.find_element(value="react-select-6--value-item")
        driver.execute_script(f'arguments[0].innerHTML = "{profile.activity_factor}";', activity_choice)
        smoking_choice = driver.find_element(value="react-select-7--value-item")
        driver.execute_script('arguments[0].innerHTML = "true";', smoking_choice)
        time.sleep(2)
        calories = driver.find_elements(
            by="css selector", value='[aria-label="Total daily calorie requirement "]'
        )[0].get_attribute("value")
        elems = driver.find_elements(by="css selector", value="table")
        elems = elems[4:]

        for elem in elems:
            table = BeautifulSoup(elem.get_attribute("innerHTML"), "lxml")
            for tr in table.find_all("tr"):
                td = tr.find_all("td")
                try:
                    td[0] = re.sub("<[^<]+?>", "", str(td[0]))
                    if td[0] in Scrapper.d:
                        Scrapper.set_value(
                            profile,
                            Scrapper.d[td[0]],
                            re.sub("<[^<]+?>", "", str(td[1])),
                        )
                except IndexError:
                    pass
        profile.calories = int(calories.replace(",", ""))

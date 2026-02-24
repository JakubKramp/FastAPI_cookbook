import inspect
import profile
import time

from playwright.async_api import async_playwright
import re

from sqlalchemy.ext.asyncio import AsyncSession

from auth.constants import RANGES
from auth.models import Profile
from auth.schemas import DietaryReferenceIntakes


class BaseDRIClient:
    base_url = ""
    DRI_names_mapping = {}
    setter_functions = []

    @staticmethod
    def get_age(age: int) -> str| None:
        age_label = next((r for r in RANGES if age in r), None)
        return age_label.label

    @staticmethod
    def set_value(profile, key, value):
        if type(value) is int:
            profile.__setattr__(profile, key, value)
            return
        elif " mg" in value:
            profile.__setattr__(key, int(value.split("mg")[0]))
            return
        elif "grams" in value:
            value = value.strip(" grams")
        if value.find("-"):
            profile.__setattr__(key, int(sum(map(int, value.split("-"))) / 2))
            return
        profile.__setattr__(key, value)

    @staticmethod
    async def accept_cookie_banner(page):
        try:
            button = page.locator("#accept-btn")
            await button.wait_for(timeout=3000)
            await button.click()
        except Exception:
            pass  # banner didn't appear, continue

    def get_DRI_data(self):
        raise NotImplementedError


async def get_table_data(page):
    rows = await page.locator('table tr').all()
    data = {}
    for row in rows[1:]:  # skip header
        cells = await row.locator('td p').all_inner_texts()
        if len(cells) == 2:
            data[cells[0]] = cells[1]
    return data


class DRIClient(BaseDRIClient):
    base_url = "https://www.omnicalculator.com/health/dri"
    DRI_names_mapping = {
        "Carbohydrates": "carbohydrates",
        "Fat": "fat",
        "Protein": "protein",
        "Sodium": "sodium",
        "Potassium": "potassium",
        "Total fiber": "fiber",
    }
    def __init__(self):
        self.setter_functions = [
            method for name, method in inspect.getmembers(self, predicate=inspect.ismethod)
            if name.startswith("set_")
        ]

    async def set_height(self, page, profile) -> None:
        height_input = page.locator('[data-cwv-id="calculator-block_variable-numerical-input_native"]').nth(0)
        await height_input.click()
        await height_input.fill(str(profile.height))

    async def set_weight(self, page, profile) -> None:
        weight_input = page.locator('[data-testid="blockGroups.0.matrices.4.columns.0.0-input"]')
        await weight_input.click()
        await weight_input.fill(str(profile.weight))

    async def set_activity(self, page,  profile) -> None:
        activity_select = page.locator('#blockGroups\\.0\\.matrices\\.6\\.columns\\.0\\.0-input')
        await activity_select.select_option(label='Exercise 1-2 times a week')
        await activity_select.select_option(label=profile.activity_factor)

    async def set_smoking(self, page, profile) -> None:
        if profile.smoking:
            await page.locator('input[value="EF0hpa8mMsL4Ba0MSPGWM"]').click()

    async def set_age(self, page, profile) -> None:
        age_select = page.locator('[id="blockGroups.0.matrices.2.columns.0.0-input"]')
        await age_select.select_option(label=self.get_age(profile.age))

    async def set_sex(self, page, profile):
        sex_radiogroup = page.locator(
            '[role="radiogroup"][data-cwv-id="calculator-block_variable-value_select-radio"]')

        sex_radio = sex_radiogroup.locator('label').filter(has_text=profile.sex).locator('input[type="radio"]')
        await sex_radio.check()

    async def fill_form(self, page, profile):
        for setter in self.setter_functions:
            await setter(page, profile)

    @staticmethod
    async def process_value(value: str) -> float:
        value, unit = value.strip().split(" ")
        if unit == 'grams':
            if '-' in value:
                minimum, maximum = map(int, value.split('-'))
                return (minimum + maximum)/2
            return float(value)
        elif unit == 'mg':
            return float(value)/1000
        else:
            raise ValueError(f"Unrecognized unit: {unit}")


    async def extract_data(self, page) -> DietaryReferenceIntakes:
        table_data = get_table_data(page)
        dri_data = {}
        calories = await page.locator('[data-testid="blockGroups.0.matrices.7.columns.0.0-input"]').input_value()
        for key, value in table_data.items():
            if key in self.DRI_names_mapping:
                dri_data[self.DRI_names_mapping[key]] = await self.process_value(value)
        dri_data['calories'] = calories
        return DietaryReferenceIntakes(**dri_data)

    async def get_data(self, profile, session) -> DietaryReferenceIntakes:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            page = await browser.new_page()
            await page.goto(self.base_url)
            await self.accept_cookie_banner(page)
            await self.fill_form(page, profile)
            dri = await self.extract_data(page)
            profile = await self.fill_profile(profile, session, dri)
            return dri

    async def fill_profile(self, profile: Profile, session: AsyncSession, dri_data: DietaryReferenceIntakes) -> Profile:

        for field in ["calories", "carbohydrates", "fat", "protein", "fiber", "potassium", "sodium"]:
            setattr(profile, field, getattr(dri_data, field))

        session.add(profile)
        await session.commit()
        await session.refresh(profile)

        return profile
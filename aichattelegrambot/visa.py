import os
import re
import random
import platform
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def visa_checker(visa_number: str) -> bytes:
    """
    Visu checker returns back image with the user's status

    :param str visa_number: user's visu number
    :return bytes: status image
    """
    parts_of_number = _split_valid_data(visa_number)
    URL = "https://frs.gov.cz/informace-o-stavu-rizeni/"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")

    with webdriver.Chrome(options=options, service=_get_chrome_service()) as driver:
        driver.get(URL)
        sleep(1.5)

        cookie_cancel_button = driver.find_element(By.XPATH, "//button[text()='Odmítnout všechny']")
        cookie_cancel_button.click()

        # The order of elements is very IMPORTANT
        form_inputs = [
            driver.find_element(By.NAME, "proceedings.referenceNumber"),
            driver.find_element(By.NAME, "proceedings.additionalSuffix"),
        ]
        form_inputs.extend(
            driver.find_elements(By.XPATH, "//div[@class='react-select__input']//input")
        )

        for gui_element, part_visu in zip(form_inputs, parts_of_number):
            if part_visu:
                gui_element.send_keys(part_visu)
                if "autocapitalize" in gui_element.get_attribute("outerHTML"):
                    gui_element.send_keys(Keys.RETURN)
            sleep(random.uniform(0.5, 0.8))
        sleep(random.uniform(0.5, 0.8))

        submit_button = driver.find_element(By.XPATH, "//button[text()='Ověřit']")
        submit_button.click()
        sleep(1.5)

        website_content = driver.find_element(By.CLASS_NAME, "alert")
        sleep(random.uniform(0.5, 0.8))

        img = website_content.screenshot_as_png
        return img


def _get_chrome_service() -> ChromeService:
    if platform.machine() == "aarch64":
        chromedriver_path = os.getenv("CHROMEDRIVER", "chromedriver")
        return ChromeService(executable_path=chromedriver_path)
    else:
        return ChromeService(ChromeDriverManager().install())


def _split_valid_data(number: str) -> list:
    """
    Spliting and valid visu number.
    It should be format [12345-XX/CC-YYYY] or [12345/CC-YYYY]

    :param str number: visu number
    :raises Exception:
    :return list: split data num, fake, code, year
    """

    # The order of elements is very IMPORTANT
    parts_of_number = re.split(r"\-|\/", number)

    try:
        if len(parts_of_number) == 4:
            return [
                int(parts_of_number[0]),
                int(parts_of_number[1]),
                str(parts_of_number[2]),
                int(parts_of_number[3]),
            ]

        if len(parts_of_number) == 3:
            return [
                int(parts_of_number[0]),
                None,
                str(parts_of_number[1]),
                int(parts_of_number[2]),
            ]
        raise
    except Exception as exc:
        raise Exception("Invalid the visu number, try again") from exc

visa_checker("22602/TP-2024")
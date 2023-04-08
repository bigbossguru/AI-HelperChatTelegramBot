import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def visa_checker(visa_number: str) -> bytes:
    """
    Visu checker returns back image with the user's status

    :param str visa_number: user's visu number
    :return bytes: status image
    """
    parts_of_number = _split_valid_data(visa_number)
    URL = "https://frs.gov.cz/en/ioff/application-status"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")

    with webdriver.Chrome(options=options) as driver:
        driver.get(URL)

        # The order of elements is very IMPORTANT
        form_inputs = [
            driver.find_element(By.NAME, "ioff_application_number"),
            driver.find_element(By.NAME, "ioff_application_number_fake"),
            driver.find_element(By.NAME, "ioff_application_code"),
            driver.find_element(By.NAME, "ioff_application_year"),
        ]

        for gui_element, part_visu in zip(form_inputs, parts_of_number):
            if part_visu:
                gui_element.send_keys(part_visu)
            sleep(0.5)
        sleep(0.5)

        button_op = driver.find_element(By.NAME, "op")
        button_op.click()
        sleep(0.5)

        website_content = driver.find_element(By.CLASS_NAME, "alert")
        img = website_content.screenshot_as_png
        return img


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

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def visa_checker(visa_num):
    num, code, year = visa_num.split("-")
    URL = "https://frs.gov.cz/cs/ioff/application-status"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")

    with webdriver.Chrome(options=options) as driver:
        driver.get(URL)

        input_app_num = driver.find_element(By.NAME, "ioff_application_number")
        # input_app_num_fake = driver.find_element(By.NAME, "ioff_application_number_fake")
        input_app_code = driver.find_element(By.NAME, "ioff_application_code")
        input_app_year = driver.find_element(By.NAME, "ioff_application_year")

        input_app_num.send_keys(num)
        sleep(0.5)
        # input_app_num_fake.send_keys("3")
        # sleep(0.5)
        input_app_code.send_keys(code)
        sleep(0.5)
        input_app_year.send_keys(year)

        sleep(1.0)
        button_op = driver.find_element(By.NAME, "op")
        button_op.click()

        sleep(0.5)
        website_content = driver.find_element(By.CLASS_NAME, "alert")
        # website_content.screenshot("visa.png")
        img = website_content.screenshot_as_png
        return img

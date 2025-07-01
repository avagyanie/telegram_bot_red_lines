import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from app.recaptcha_solver import solve_recaptcha


def fetch_driver_info(reg_cert: str, plate_number: str) -> str:
    print("[fetch_driver_info] Start")
    url = "https://www.yerevan.am/hy/parking-paid/"

    try:
        service = Service("/Users/avagyani/Desktop/telegram_bot_red_lines/geckodriver/geckodriver")
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(service=service, options=options)

        driver.get(url)
        print("[fetch_driver_info] Page opened")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "pin2"))
        )

        cert_input = driver.find_element(By.NAME, "cert_number")
        plate_input = driver.find_element(By.NAME, "plate_number")

        cert_input.send_keys(reg_cert)
        plate_input.send_keys(plate_number)

        print("[fetch_driver_info] Filled form fields")

        solve_recaptcha(driver)
        print("[fetch_driver_info] reCAPTCHA solved")

        submit_button = driver.find_element(By.ID, "parkingSubmit")
        submit_button.click()

        print("[fetch_driver_info] Submit clicked")

        time.sleep(5)

        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)
        page_text = driver.find_element(By.TAG_NAME, "body").text

        driver.quit()

        return page_text[:2000] + "..." if page_text else "Տվյալներ չեն գտնվել։"

    except Exception as e:
        print(f"[fetch_driver_info ERROR] {e}")
        return "Սխալ տեղի ունեցավ։ Խնդրում ենք փորձել ավելի ուշ։"

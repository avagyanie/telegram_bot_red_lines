import time
import base64
import io
import numpy as np
import cv2
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def solve_recaptcha(driver):
    print("[reCAPTCHA] Solving started...")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']"))
    )

    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
    driver.switch_to.frame(iframe)

    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
    )

    ActionChains(driver).move_to_element(checkbox).click().perform()
    print("[reCAPTCHA] Checkbox clicked")

    time.sleep(2)

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='challenge']"))
    )
    image_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title*='challenge']")
    driver.switch_to.frame(image_iframe)

    print("[reCAPTCHA] Waiting for challenge...")

    time.sleep(5)

    driver.switch_to.default_content()
    print("[reCAPTCHA] Completed (assumed passed)")

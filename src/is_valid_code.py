import requests
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_valid_code(code, driver):
    data = requests.get(
        f"https://apitwo.classpoint.app/classcode/region/byclasscode?classcode={code}"
    )

    if data.status_code != 200:
        return [False]

    driver.get(f"https://www.classpoint.app/?code={code}")

    wait = WebDriverWait(driver, 5)

    try:
        next_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[2]/div[2]/button'))
        )
        next_btn.click()
    except TimeoutException:
        return [False]
    except Exception:
        return [False]

    try:
        name_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="standard-basic"]'))
        )
        name_input.send_keys("\u200b")
    except TimeoutException:
        return [False]
    except Exception:
        return [False]

    try:
        join_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[4]/button'))
        )
        join_btn.click()
    except TimeoutException:
        return [False]
    except Exception:
        return [False]

    # Detect the "Presenter is not in slideshow" state and treat as invalid
    try:
        driver.find_element(
            By.XPATH,
            "//*[contains(text(), 'Presenter is not in slideshow')]",
        )
        return [False]
    except NoSuchElementException:
        pass
    except Exception:
        return [False]

    # Fallback: Check if a main image exists and has a src attribute
    try:
        image_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="root"]/div/div[1]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/img',
                )
            )
        )
        if not image_element.get_attribute("src"):
            return [False]
    except TimeoutException:
        return [False]
    except Exception:
        return [False]

    presenter_email = data.json().get("presenterEmail")
    return [True, presenter_email] if presenter_email else [False]

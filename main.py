import os
import random
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crear_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.page_load_strategy = "eager"

    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
    if chromedriver_path and os.path.exists(chromedriver_path):
        service = Service(executable_path=chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    return webdriver.Chrome(options=options)


def responder_encuesta_una_vez():
    url = "https://tudrogueriaaldia.com.co/stores/2469/encuesta"
    driver = None

    try:
        driver = crear_driver()
        driver.set_page_load_timeout(30)
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        menus_desplegables = wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "select"))
        )

        for menu in menus_desplegables:
            try:
                selector = Select(menu)
                selector.select_by_visible_text("Muy satisfecho(a)")
                time.sleep(0.2)
            except Exception:
                pass

        boton_enviar = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@type='submit' or contains(text(), 'Enviar') or contains(text(), 'Finalizar')]",
                )
            )
        )
        driver.execute_script("arguments[0].click();", boton_enviar)

        time.sleep(2)
        print("Encuesta completada y enviada con éxito.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # Probabilidad aleatoria (75%) para que de los 40 disparos diarios del Cron
    # se envíen de forma variable y natural entre ~20 y 40 encuestas al día.
    if random.random() <= 0.85:
        responder_encuesta_una_vez()
    else:
        print("Ejecución omitida aleatoriamente para variar el volumen diario.")
    sys.exit(0)

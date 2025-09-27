from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



from selenium.common.exceptions import StaleElementReferenceException
import time

def leer_bloque_estable(driver, selector, index, reintentos=10, espera=3.0):
    texto_anterior = ""
    for intento in range(reintentos):
        try:
            bloque = driver.find_elements(By.CSS_SELECTOR, selector)[index]
            if bloque.find_elements(By.CSS_SELECTOR, ".pending, .animating"):
                time.sleep(espera)
                continue
            texto = bloque.text.strip()
            if texto == texto_anterior and texto != "":
                return texto
            texto_anterior = texto
        except StaleElementReferenceException:
            pass
        time.sleep(espera)
    try:
        bloque = driver.find_elements(By.CSS_SELECTOR, selector)[index]
        fallback_html = bloque.get_attribute("innerHTML")
        print("⚠️ No se pudo estabilizar el texto. Mostrando innerHTML:")
        print(fallback_html)
    except:
        fallback_html = "(no se pudo leer texto estable del bloque)"
    return texto_anterior or "(no se pudo leer texto estable del bloque)"


def iniciar_sesion():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)

    driver.get("https://gemini.google.com/app")
    input_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.ql-editor.textarea.new-input-ui')
    ))

    mensaje_inicial = (
        "Hola, sos un pato que no sabe información del mundo. "
        "Yo voy a contarte cosas y vos vas a ser curioso. "
        "Quiero que respondas lo más corto y amigable posible y sin emojis y sin acentos."
        "Saludame, patito"
    )

    input_box.click()
    input_box.send_keys(Keys.CONTROL + "a")
    input_box.send_keys(Keys.BACKSPACE)
    input_box.send_keys(mensaje_inicial)
    input_box.send_keys(Keys.ENTER)

    respuestas_antes = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    cantidad_antes = len(respuestas_antes)

    wait.until(lambda d: len(
        d.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    ) > cantidad_antes)

    # 🔽 NUEVO: leer la respuesta de Gemini
    respuestas_despues = driver.find_elements(
        By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color'
    )

    respuesta_inicial = leer_bloque_estable(
        driver,
        'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color',
        len(respuestas_despues) - 1
    )

    return driver, respuesta_inicial



def enviar_mensaje(texto_usuario, driver):
    wait = WebDriverWait(driver, 30)
    input_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.ql-editor.textarea.new-input-ui')
    ))

    respuestas_antes = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    cantidad_antes = len(respuestas_antes)

    input_box.click()
    input_box.send_keys(Keys.CONTROL + "a")
    input_box.send_keys(Keys.BACKSPACE)
    input_box.send_keys(texto_usuario)
    input_box.send_keys(Keys.ENTER)

    wait.until(lambda d: len(
        d.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    ) > cantidad_antes)

    respuestas_despues = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    nuevos_bloques = respuestas_despues[cantidad_antes:]

    textos = []
    for i in range(len(nuevos_bloques)):
        texto = leer_bloque_estable(driver, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color', cantidad_antes + i)
        textos.append(texto)

    respuesta = "\n".join(textos)
    return respuesta, driver




from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
from PiperVoice import hablar_como_pato
from ReconogizeVoice import escuchar_voz

# Función para leer texto estable de un bloque, reintentando si da stale
def leer_bloque_estable(driver, selector, index, reintentos=10, espera=3.0):
    texto_anterior = ""
    for intento in range(reintentos):
        try:
            bloque = driver.find_elements(By.CSS_SELECTOR, selector)[index]

            # Esperar a que desaparezcan elementos en animación
            if bloque.find_elements(By.CSS_SELECTOR, ".pending, .animating"):
                time.sleep(espera)
                continue

            # Cambiado para obtener texto limpio completo del bloque, sin palabras sueltas
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

# Configuración del navegador
chrome_options = Options()
""" chrome_options.add_argument("--headless=new")  """ # Descomenta para modo sin ventana
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

try:
    driver.get("https://gemini.google.com/app")

    # Esperar input del chat
    input_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.ql-editor.textarea.new-input-ui')
    ))

    # Mensaje inicial al pato
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

    # Esperar respuesta inicial
    respuestas_antes = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    cantidad_antes = len(respuestas_antes)

    wait.until(lambda d: len(
        d.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
    ) > cantidad_antes)

    respuestas_despues = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')

    # Extraer texto inicial
    respuesta_inicial = leer_bloque_estable(driver, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color', len(respuestas_despues)-1)
    print("🦆 Patito dice:", respuesta_inicial)
    hablar_como_pato(respuesta_inicial)
    print("-" * 40)

    # Loop de interacción con el usuario
    while True:
        input_box.click()
        input_box.send_keys(Keys.CONTROL + "a")
        input_box.send_keys(Keys.BACKSPACE)

        """ prompt = input("Tu mensaje para el patito: ") """
        prompt = escuchar_voz()

        if prompt.lower() in ("exit", "salir", "quit"):
            print("👋 Saliendo...")
            break

        respuestas_antes = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
        cantidad_antes = len(respuestas_antes)

        input_box.send_keys(prompt)
        input_box.send_keys(Keys.ENTER)

        try:
            wait.until(lambda d: len(
                d.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
            ) > cantidad_antes)
        except TimeoutException:
            print("⏰ El patito no respondió a tiempo. ¿Está dormido?")
            continue

        respuestas_despues = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color')
        nuevos_bloques = respuestas_despues[cantidad_antes:]

        for i in range(len(nuevos_bloques)):
            texto = leer_bloque_estable(driver, 'div.markdown.markdown-main-panel.stronger.enable-updated-hr-color', cantidad_antes + i)
            print(f"🦆 Patito responde (bloque {i + 1}):\n{texto}")
            print("-" * 40)
            hablar_como_pato(texto)
        time.sleep(1)

finally:
    driver.quit()

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

load_dotenv()

def iniciar_chrome():
    ruta = r"C:\Users\Osliany\Desktop\python\scrapping\chromedriver.exe"
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    #options.add_argument("--window-size=970,1000")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")    
    options.add_argument("--disable-notifications")    
    options.add_argument("--ignore-certificate-errors")    
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    exp_opt = [
        "enable-automaiton",
        "ignore-certificate-errors",
        "enable-logging"
    ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "intl.accept_langiages": ["es-ES", "es"],
        "credentials_enable_service": False
    }
    options.add_experimental_option("prefs", prefs)
    
    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    #driver.set_window_position(0,0)
    return driver

def login():
    print("Login")
    driver.get("http://localhost:8000/login")
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_username"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_password"))
    )

    username_input.send_keys(USER)
    password_input.send_keys(PASS)

    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.form-inline"))
    )
    print("/Libros")


def filtro_libros():
    categoria_programacion = driver.find_element(By.CSS_SELECTOR, "select[name='categoria'] option[value='programacion']")
    categoria_programacion.click()

    ordenar_por_prestados = driver.find_element(By.CSS_SELECTOR, "select[name='ordenar_por'] option[value='-cantidad_prestada']")
    ordenar_por_prestados.click()

    buscar = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    buscar.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-striped"))
    )
    libros = driver.find_elements(By.CSS_SELECTOR, "table.table-striped tbody tr")
    for libro in libros:
        titulo = libro.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        prestados = libro.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
        print(f"{titulo}: {prestados} prestados")


def libro_detail():
    libros = driver.find_elements(By.CSS_SELECTOR, "table.table-striped tbody tr")
    primer_libro = libros[0].find_element(By.CSS_SELECTOR, "td:nth-child(1) a")
    primer_libro.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
    )
    titulo_libro = driver.find_element(By.CSS_SELECTOR, "h2").text
    print(f"Libro-detail: {titulo_libro}")
    

def devolver_libro():
    primer_prestamo = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-success.btn-sm")
    primer_prestamo.click()
    print("libro devuelto")
    

def logout():
    nav_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav-bar"))
    )
    logout_link = nav_bar.find_element(By.LINK_TEXT, "Salir")
    logout_link.click()
    print("Sesión Cerrada")


if __name__ == "__main__":
    USER = os.getenv("USER")
    PASS = os.getenv("PASS")
    driver = iniciar_chrome()
    while(True):
        login()
        time.sleep(2)
        filtro_libros()
        time.sleep(2)
        libro_detail()
        time.sleep(2)
        devolver_libro()
        time.sleep(2)
        logout()
        time.sleep(2)
        x = input("Pulsa 0 para salir, cualquier otra tecla para continuar \n")
        if x == "0":
            driver.quit()
            print("Rutina finalizada")
            break
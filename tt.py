import csv
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def init_driver():
    """Inicializa y retorna el WebDriver en modo headless."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error al inicializar ChromeDriver: {e}")
        sys.exit(1)

driver = init_driver()

base_url = 'https://www.falabella.com/falabella-cl/category/CATG10205/Cervezas?sred=cerveza&page='
productos = []

def obtener_datos_pagina(url):
    """Extrae productos de una página de búsqueda de Falabella. Retorna 'ok', 'empty' o 'error'."""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'b[class*=pod-subTitle]'))
        )

        nombres = driver.find_elements(By.CSS_SELECTOR, 'b[class*=pod-subTitle]')
        precios = driver.find_elements(By.CSS_SELECTOR, 'span[class*=copy10]')

        if not nombres or not precios:
            return "empty"

        for nombre, precio in zip(nombres, precios):
            productos.append({
                'nombre': nombre.text.strip(),
                'precio': precio.text.strip()
            })

        return "ok"
    except Exception as e:
        print(f"Error al procesar la página {url}: {e}")
        return "error"

def guardar_datos_csv(productos):
    """Guarda la lista de productos en un archivo CSV con timestamp."""
    ahora = datetime.now()
    fecha_hora_actual = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_csv = f'tt_productos_cerveza_{fecha_hora_actual}.csv'
    with open(nombre_archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
        fieldnames = ['Nombre', 'Precio']
        writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
        writer.writeheader()
        for producto in productos:
            writer.writerow({
                'Nombre': producto['nombre'],
                'Precio': producto['precio']
            })
    return nombre_archivo_csv

def main():
    """Ejecuta el flujo principal de scraping."""
    pagina_actual = 1
    try:
        while True:
            print(f'Extrayendo datos de la página {pagina_actual}...')
            url_actual = f'{base_url}{pagina_actual}'

            resultado = obtener_datos_pagina(url_actual)
            if resultado == "empty":
                print(f'No hay más productos en la página {pagina_actual}. Deteniendo la extracción de datos.')
                break
            elif resultado == "error":
                print(f"Error en la página {pagina_actual}. Continuando con la siguiente.")
                continue

            pagina_actual += 1

        nombre_archivo_csv = guardar_datos_csv(productos)
        print(f'Los datos han sido guardados en {nombre_archivo_csv}.')

        for idx, producto in enumerate(productos, start=1):
            print(f'Producto {idx}:')
            print(f'Nombre: {producto["nombre"]}')
            print(f'Precio: {producto["precio"]}')
            print('---')
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

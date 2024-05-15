import requests
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


options = webdriver.ChromeOptions()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
base_url = 'https://www.santaisabel.cl/busqueda?ft=cerveza'
productos = []

def obtener_datos_pagina(url):
    driver.get(url)
    time.sleep(5)  
    if not driver.find_elements(By.CSS_SELECTOR, 'span.prices-main-price') or \
       not driver.find_elements(By.CSS_SELECTOR, 'a.product-card-name'):
        return False  

    precios = driver.find_elements(By.CSS_SELECTOR, 'span.prices-main-price')
    nombres = driver.find_elements(By.CSS_SELECTOR, 'a.product-card-name')

    for precio, nombre in zip(precios, nombres):
        productos.append({
            'nombre': nombre.text,
            'precio': precio.text,
            'enlace': nombre.get_attribute('href')
        })

    return True  

def guardar_datos_csv(productos):
    ahora = datetime.now()
    fecha_hora_actual = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_csv = f'si_productos_cerveza_{fecha_hora_actual}.csv'
    with open(nombre_archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
        fieldnames = ['Nombre', 'Precio', 'Enlace']
        writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
        writer.writeheader()
        for producto in productos:
            writer.writerow({
                'Nombre': producto['nombre'],
                'Precio': producto['precio'],
                'Enlace': producto['enlace']
            })
    return nombre_archivo_csv

pagina_actual = 1

while True:
    print(f'Extrayendo datos de la página {pagina_actual}...')
    url_actual = f'{base_url}&page={pagina_actual}'

    respuesta = requests.get(url_actual)
    if respuesta.status_code == 200:
        if not obtener_datos_pagina(url_actual):
            print(f'No hay más productos en la página {pagina_actual}. Deteniendo la extracción de datos.')
            break
        pagina_actual += 1
    else:
        print(f'La página {pagina_actual} no está disponible. Deteniendo la extracción de datos.')
        break
nombre_archivo_csv = guardar_datos_csv(productos)
print(f'Los datos han sido guardados en {nombre_archivo_csv}.')

for idx, producto in enumerate(productos, start=1):
    print(f'Producto {idx}:')
    print(f'Nombre: {producto["nombre"]}')
    print(f'Precio: {producto["precio"]}')
    print(f'Enlace: {producto["enlace"]}')
    print('---')

driver.quit()

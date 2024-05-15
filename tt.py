import csv
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = 'https://www.falabella.com/falabella-cl/category/CATG10205/Cervezas?sred=cerveza&page='
productos = []

def obtener_datos_pagina(url):
    driver.get(url)
    time.sleep(5) 

    nombres = driver.find_elements(By.CSS_SELECTOR, 'b[class*=pod-subTitle]')
    precios = driver.find_elements(By.CSS_SELECTOR, 'span[class*=copy10]')

    if not nombres or not precios:
        return False

    for nombre, precio in zip(nombres, precios):
        productos.append({
            'nombre': nombre.text.strip(),
            'precio': precio.text.strip()
        })

    return True
def guardar_datos_csv(productos):
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

pagina_actual = 1
while True:
    print(f'Extrayendo datos de la página {pagina_actual}...')
    url_actual = f'{base_url}{pagina_actual}'

    if not obtener_datos_pagina(url_actual):
        print(f'No hay más productos en la página {pagina_actual}. Deteniendo la extracción de datos.')
        break

    pagina_actual += 1

nombre_archivo_csv = guardar_datos_csv(productos)
print(f'Los datos han sido guardados en {nombre_archivo_csv}.')

for idx, producto in enumerate(productos, start=1):
    print(f'Producto {idx}:')
    print(f'Nombre: {producto["nombre"]}')
    print(f'Precio: {producto["precio"]}')
    print('---')
driver.quit()

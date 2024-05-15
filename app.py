import requests
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración del navegador Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin interfaz gráfica)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Inicializa el controlador de Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL base de la página web
base_url = 'https://www.santaisabel.cl/busqueda?ft=cerveza'

# Lista para almacenar los productos
productos = []

# Función para obtener datos de una página
def obtener_datos_pagina(url):
    driver.get(url)
    time.sleep(5)  # Espera para asegurar que la página se cargue completamente

    # Verifica si los elementos están presentes en la página actual
    if not driver.find_elements(By.CSS_SELECTOR, 'span.prices-main-price') or \
       not driver.find_elements(By.CSS_SELECTOR, 'a.product-card-name'):
        return False  # Detiene el scraping si los elementos no están presentes

    # Encuentra los elementos que contienen el precio y el nombre del producto
    precios = driver.find_elements(By.CSS_SELECTOR, 'span.prices-main-price')
    nombres = driver.find_elements(By.CSS_SELECTOR, 'a.product-card-name')

    # Extrae los datos de la página y los agrega a la lista de productos
    for precio, nombre in zip(precios, nombres):
        productos.append({
            'nombre': nombre.text,
            'precio': precio.text,
            'enlace': nombre.get_attribute('href')
        })

    return True  # Continúa el scraping si los elementos están presentes

# Función para guardar los datos en un archivo CSV con la fecha y hora de creación
def guardar_datos_csv(productos):
    ahora = datetime.now()
    fecha_hora_actual = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_csv = f'productos_cerveza_{fecha_hora_actual}.csv'
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

# Inicializa la navegación desde la página 1
pagina_actual = 1

# Bucle para navegar a través de las páginas
while True:
    print(f'Extrayendo datos de la página {pagina_actual}...')
    url_actual = f'{base_url}&page={pagina_actual}'

    # Verifica el estado de la página actual
    respuesta = requests.get(url_actual)
    if respuesta.status_code == 200:
        if not obtener_datos_pagina(url_actual):
            print(f'No hay más productos en la página {pagina_actual}. Deteniendo la extracción de datos.')
            break
        pagina_actual += 1
    else:
        print(f'La página {pagina_actual} no está disponible. Deteniendo la extracción de datos.')
        break

# Guarda los datos en un archivo CSV
nombre_archivo_csv = guardar_datos_csv(productos)
print(f'Los datos han sido guardados en {nombre_archivo_csv}.')

# Muestra los datos obtenidos
for idx, producto in enumerate(productos, start=1):
    print(f'Producto {idx}:')
    print(f'Nombre: {producto["nombre"]}')
    print(f'Precio: {producto["precio"]}')
    print(f'Enlace: {producto["enlace"]}')
    print('---')

# Cierra el navegador
driver.quit()

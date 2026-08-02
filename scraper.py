"""Scraper parametrizado de cervezas en e-commerce chileno (Selenium headless).

Comparte la lógica de scraping entre st.py (Santa Isabel) y tt.py (Falabella).
Cada sitio se describe con una :class:`SitioConfig`.
"""

from __future__ import annotations

import csv
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver: webdriver.Chrome | None = None


@dataclass(frozen=True)
class SitioConfig:
    """Configuración de un sitio a scrapear."""

    nombre: str
    base_url: str
    selector_nombre: str
    selector_precio: str
    prefijo_csv: str
    incluir_enlace: bool = False
    delay_segundos: tuple[float, float] = (0.0, 0.0)


SANTASABEL = SitioConfig(
    nombre="santaisabel",
    base_url="https://www.santaisabel.cl/busqueda?ft=cerveza&page=",
    selector_nombre="a.product-card-name",
    selector_precio="span.prices-main-price",
    prefijo_csv="si_productos_cerveza",
    incluir_enlace=True,
    delay_segundos=(1.0, 3.0),
)

FALABELLA = SitioConfig(
    nombre="falabella",
    base_url="https://www.falabella.com/falabella-cl/category/CATG10205/Cervezas?sred=cerveza&page=",
    selector_nombre="b[class*=pod-subTitle]",
    selector_precio="span[class*=copy10]",
    prefijo_csv="tt_productos_cerveza",
)


def init_driver() -> webdriver.Chrome:
    """Inicializa y retorna el WebDriver en modo headless."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error al inicializar ChromeDriver: {e}")
        sys.exit(1)


def obtener_datos_pagina(url: str, productos: list, config: SitioConfig) -> str:
    """Extrae productos de una página de búsqueda. Retorna 'ok', 'empty' o 'error'."""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config.selector_precio))
        )

        nombres = driver.find_elements(By.CSS_SELECTOR, config.selector_nombre)
        precios = driver.find_elements(By.CSS_SELECTOR, config.selector_precio)

        if not nombres or not precios:
            return "empty"

        for nombre, precio in zip(nombres, precios, strict=False):
            producto = {
                "nombre": nombre.text.strip(),
                "precio": precio.text.strip(),
            }
            if config.incluir_enlace:
                producto["enlace"] = nombre.get_attribute("href")
            productos.append(producto)

        return "ok"
    except Exception as e:
        print(f"Error al procesar la página {url}: {e}")
        return "error"


def guardar_datos_csv(productos: list, config: SitioConfig) -> str:
    """Guarda la lista de productos en un archivo CSV con timestamp."""
    ahora = datetime.now()
    fecha_hora_actual = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_csv = f"{config.prefijo_csv}_{fecha_hora_actual}.csv"
    fieldnames = ["Nombre", "Precio"]
    if config.incluir_enlace:
        fieldnames.append("Enlace")
    with open(nombre_archivo_csv, "w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
        writer.writeheader()
        for producto in productos:
            row = {"Nombre": producto["nombre"], "Precio": producto["precio"]}
            if config.incluir_enlace:
                row["Enlace"] = producto["enlace"]
            writer.writerow(row)
    return nombre_archivo_csv


def main(config: SitioConfig) -> None:
    """Ejecuta el flujo principal de scraping para un sitio."""
    global driver
    driver = init_driver()
    pagina_actual = 1
    productos = []

    try:
        while True:
            print(f"Extrayendo datos de la página {pagina_actual}...")
            url_actual = f"{config.base_url}{pagina_actual}"

            resultado = obtener_datos_pagina(url_actual, productos, config)
            if resultado == "empty":
                print(f"No hay más productos en la página {pagina_actual}. Deteniendo la extracción de datos.")
                break
            elif resultado == "error":
                print(f"Error en la página {pagina_actual}. Continuando con la siguiente.")
                continue
            pagina_actual += 1
            if config.delay_segundos[1] > 0:
                time.sleep(random.uniform(*config.delay_segundos))

        nombre_archivo_csv = guardar_datos_csv(productos, config)
        print(f"Los datos han sido guardados en {nombre_archivo_csv}.")

        for idx, producto in enumerate(productos, start=1):
            print(f"Producto {idx}:")
            print(f'Nombre: {producto["nombre"]}')
            print(f'Precio: {producto["precio"]}')
            if config.incluir_enlace:
                print(f'Enlace: {producto["enlace"]}')
            print("---")
    finally:
        driver.quit()

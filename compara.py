import csv
import os
from datetime import datetime


def obtener_ultimos_csv():
    """Obtiene los dos archivos CSV más recientes del directorio actual."""
    files = [file for file in os.listdir() if ("productos_cerveza_" in file or "si_productos_cerveza_" in file or "tt_productos_cerveza_" in file) and file.endswith(".csv")]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[:2]


def parsear_precio_chileno(price_str):
    """Convierte un string de precio chileno a float. Retorna 0.0 si no es válido."""
    try:
        s = price_str.replace('$', '').replace('.', '').replace(',', '.')
        return float(s)
    except (ValueError, AttributeError):
        print(f"Advertencia: no se pudo parsear el precio '{price_str}'")
        return 0.0


def leer_csv(filename):
    """Lee un archivo CSV y retorna una lista de diccionarios."""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def comparar_precios(csv_anterior, csv_actual):
    """Compara precios entre dos listas de productos."""
    comparacion = []
    for current_item in csv_actual:
        name = current_item['Nombre']
        precio_actual = parsear_precio_chileno(current_item['Precio'])
        precio_anterior = None

        for previous_item in csv_anterior:
            if previous_item['Nombre'] == name:
                precio_anterior = parsear_precio_chileno(previous_item['Precio'])
                break

        if precio_anterior is not None:
            if precio_actual > precio_anterior:
                cambio = 'subió'
            elif precio_actual < precio_anterior:
                cambio = 'bajó'
            else:
                cambio = 'mantuvo'
            comparacion.append({'Nombre': name, 'Cambio': cambio})
        else:
            comparacion.append({'Nombre': name, 'Cambio': 'nuevo'})

    return comparacion


def guardar_comparacion_csv(comparacion):
    """Guarda el resultado de la comparación en un CSV con timestamp."""
    filename = "comparacion_cerveza_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Nombre', 'Cambio']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparacion)
    print(f"Archivo '{filename}' generado exitosamente con la comparación.")


def main():
    latest_files = obtener_ultimos_csv()
    if len(latest_files) < 2:
        print("No se encontraron suficientes archivos CSV para comparar.")
        return

    csv_anterior = leer_csv(latest_files[1])
    csv_actual = leer_csv(latest_files[0])

    comparacion = comparar_precios(csv_anterior, csv_actual)
    guardar_comparacion_csv(comparacion)


if __name__ == "__main__":
    main()

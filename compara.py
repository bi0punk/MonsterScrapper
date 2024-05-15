import csv
import os
from datetime import datetime

def get_latest_csv_filenames():
    files = [file for file in os.listdir() if file.startswith("productos_cerveza_") and file.endswith(".csv")]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[:2]

def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def compare_prices(previous_csv, current_csv):
    comparison = []
    for current_item in current_csv:
        name = current_item['Nombre']
        current_price = float(current_item['Precio'].replace('$', '').replace(',', ''))
        previous_price = None

        for previous_item in previous_csv:
            if previous_item['Nombre'] == name:
                previous_price = float(previous_item['Precio'].replace('$', '').replace(',', ''))
                break

        if previous_price is not None:
            if current_price > previous_price:
                change = 'subió'
            elif current_price < previous_price:
                change = 'bajó'
            else:
                change = 'mantuvo'
            comparison.append({'Nombre': name, 'Cambio': change})
        else:
            comparison.append({'Nombre': name, 'Cambio': 'nuevo'})

    return comparison

def write_comparison_to_csv(comparison):
    filename = "comparacion_cerveza_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Nombre', 'Cambio']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison)
    print(f"Archivo '{filename}' generado exitosamente con la comparación.")

def main():
    latest_files = get_latest_csv_filenames()
    if len(latest_files) < 2:
        print("No se encontraron suficientes archivos CSV para comparar.")
        return

    previous_csv = read_csv(latest_files[1])
    current_csv = read_csv(latest_files[0])

    comparison = compare_prices(previous_csv, current_csv)
    write_comparison_to_csv(comparison)

if __name__ == "__main__":
    main()

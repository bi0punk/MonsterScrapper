# MonsterScrapper

[![CI](https://github.com/bi0punk/MonsterScrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/bi0punk/MonsterScrapper/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Web scraping tool for Chilean e-commerce sites (Santa Isabel supermarket, Falabella). Scrapes product names, prices, and links, stores data in CSV files, and compares prices between scraping runs.

## Tabla de contenidos

- [Características](#características)
- [Stack](#stack)
- [Scripts](#scripts)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tests](#tests)
- [CI](#ci)
- [Datos](#datos)
- [Limitaciones](#limitaciones)
- [Licencia](#licencia)

## Características

- Scraping de catálogo de cervezas en Santa Isabel y Falabella (Selenium headless).
- Persistencia en CSV con timestamp por run.
- Comparación de precios entre los dos runs más recientes (`compara.py`).
- `webdriver-manager` para auto-gestión de ChromeDriver.

## Stack

- **Lenguaje**: Python 3.12+
- **Scraping**: Selenium (headless Chrome) + webdriver-manager.
- **HTTP**: requests (para comparaciones/descargas auxiliares).
- **Calidad**: ruff (lint), pytest.

## Scripts

| Script | Propósito |
|---|---|
| `st.py` | Scrapea Santa Isabel (productos cerveza). |
| `tt.py` | Scrapea Falabella (productos cerveza). |
| `compara.py` | Compara los dos CSV dumps más recientes para detectar cambios de precio. |

## Requisitos

- Python 3.12+
- Google Chrome o Chromium instalado (Selenium usa el binario del sistema).

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python st.py        # scraping Santa Isabel → CSV
python tt.py        # scraping Falabella → CSV
python compara.py   # compara los dos CSVs más recientes
```

Los CSV se nombran `productos_cerveza_<site>_<timestamp>.csv` en el directorio actual.

## Tests

```bash
pytest -q
```

Smoke tests (`tests/test_smoke.py`): imports de los scripts (sin ejecutar scraping real), helper `obtener_ultimos_csv` de `compara.py` (directorio vacío → lista vacía), deps listadas.

## CI

GitHub Actions (`.github/workflows/ci.yml`) sobre Python 3.12:

- **lint** — `ruff check .`
- **test** — `pytest -q` (no requiere Chrome; los scripts no arrancan el driver al importarse gracias al guard `__main__`).

## Datos

- CSVs `productos_cerveza_*.csv` generados por los scripts (gitignored, se regeneran).
- Sin base de datos; la comparación se hace sobre los CSVs del directorio.

## Limitaciones

- Depende de la estructura HTML de los sitios; cambios pueden romper los selectores CSS.
- Requiere Chrome/Chromium instalado para Selenium.
- Sin base de datos histórica persistente (solo CSVs sueltos).

## Licencia

MIT — ver [LICENSE](LICENSE).

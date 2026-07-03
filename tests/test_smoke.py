"""Smoke tests para MonsterScrapper.

Validan imports de los scripts (sin ejecutar scraping real) y helpers puros
de compara.py.
"""

from __future__ import annotations

from pathlib import Path


def test_imports_selenium_scripts():
    """st.py y tt.py deben importar (selenium/webdriver_manager instalados)."""
    import importlib

    for mod in ("st", "tt"):
        importlib.import_module(mod)


def test_compara_helpers_pure_stdlib():
    """compara.py usa solo stdlib; helpers deben estar disponibles."""
    import compara

    assert callable(compara.obtener_ultimos_csv)


def test_compara_obtener_ultimos_csv_empty(tmp_path: Path):
    """En un directorio sin CSVs debe devolver lista vacía."""
    import compara

    result = compara.obtener_ultimos_csv(str(tmp_path))
    assert result == []


def test_requirements_listed():
    req = Path("requirements.txt").read_text()
    for dep in ("selenium", "requests", "webdriver-manager"):
        assert dep in req, f"{dep} no está en requirements.txt"

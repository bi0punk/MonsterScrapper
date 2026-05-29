# MonsterScrapper

Web scraping tool for Chilean e-commerce sites (Santa Isabel supermarket, Falabella). Scrapes product names, prices, and links, stores data in CSV files, and compares prices between scraping runs.

## Stack

Python 3, Selenium, Requests, BeautifulSoup

## Scripts

| Script | Purpose |
|---|---|
| `st.py` | Scrapes Santa Isabel (cerveza products) |
| `tt.py` | Scrapes Falabella (cerveza products) |
| `compara.py` | Compares latest two CSV dumps for price changes |

## Usage

```bash
pip install selenium requests beautifulsoup4
python st.py
python tt.py
python compara.py
```

## License

MIT

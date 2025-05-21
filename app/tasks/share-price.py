import requests
from bs4 import BeautifulSoup
import time
import logging
import csv
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def extract_value(soup: BeautifulSoup, class_name: str, value_type: str = 'float', default=None) -> float | str:
    """
    Generic extractor for divs with a given class name.
    value_type: 'float' or 'str'.
    """
    try:
        div = soup.find('div', attrs={'class': class_name})
        if not div:
            raise ValueError(f"Div with class {class_name} not found")
        text = div.get_text(strip=True)
        if value_type == 'float':
            return float(text.replace("Rs.", "").replace(",", ""))
        return text
    except Exception as e:
        logging.warning(f"Error fetching {class_name}: {e}")
        return default if default is not None else (0.0 if value_type == 'float' else "Unknown")

def get_price(soup: BeautifulSoup) -> float:
    """Extracts the share price from the soup."""
    return extract_value(soup, 'quote__close', 'float', 0.0)

def get_sector(soup: BeautifulSoup) -> str:
    """Extracts the sector from the soup."""
    return extract_value(soup, 'quote__sector', 'str', "Unknown")

def get_company_name(soup: BeautifulSoup) -> str:
    """Extracts the company name from the soup."""
    return extract_value(soup, 'quote__name', 'str', "Unknown")

def get_equity_stats(soup: BeautifulSoup) -> dict[str, list[str]]:
    """
    Extracts equity stats from the 'equity' section of the soup.
    Returns a dictionary where keys are stat labels and values are lists of stat values.
    If the section is missing, returns an empty dict and logs a warning.
    """
    values = {}
    # Step 1: Select the main div with id="equity"
    equity_section = soup.find('div', id='equity')
    if not equity_section:
        logging.warning("Equity section not found in the HTML.")
        return values
    # Step 2: Extract stats_items inside that section
    for item in equity_section.select('.stats_item'):
        label_div = item.select_one('.stats_label')
        value_div = item.select_one('.stats_value')
        if label_div and value_div:
            label = label_div.get_text(strip=True).lower()
            value = value_div.get_text(strip=True)
            values.setdefault(label, []).append(value)
        else:
            logging.info(f"Incomplete stats_item found: {item}")
    return values

def get_script_data(scripts: set[str], wait: float = 0.5) -> dict[str, dict[str, float | str]]:
    """
    Fetches data for each script from the PSX website.
    Returns a dictionary mapping script to its data.
    Logs progress and errors for each script.
    """
    data = {}
    for script in scripts:
        logging.info(f"Processing script: {script}")
        url = f"https://dps.psx.com.pk/company/{script}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"HTTP error for {script}: {e}")
            data[script] = {'error': str(e)}
            time.sleep(wait)
            continue
        soup = BeautifulSoup(r.content, 'html5lib')
        values = get_equity_stats(soup)
        if not values:
            logging.warning(f"No equity stats found for {script}")
        data[script] = {
            'price': get_price(soup),
            'sector': get_sector(soup),
            'company_name': get_company_name(soup),
            'stats': values
        }
        time.sleep(wait)
    return data

def export_script_data_to_csv(data: dict[str, dict[str, Any]], filename: str) -> None:
    """
    Exports the result of get_script_data to a flat CSV file.
    For 'stats', uses the first value in each list.
    """
    if not data:
        logging.warning("No data to export.")
        return
    # Collect all possible stat keys
    stat_keys = set()
    for script_data in data.values():
        stats = script_data.get('stats', {})
        stat_keys.update(stats.keys())
    stat_keys = sorted(stat_keys)
    # Prepare CSV header
    fieldnames = ['script', 'price', 'sector', 'company_name'] + stat_keys
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for script, script_data in data.items():
            row = {
                'script': script,
                'price': script_data.get('price', ''),
                'sector': script_data.get('sector', ''),
                'company_name': script_data.get('company_name', '')
            }
            stats = script_data.get('stats', {})
            for key in stat_keys:
                values = stats.get(key, [])
                row[key] = values[0] if values else ''
            writer.writerow(row)
    logging.info(f"Exported script data to {filename}")

if __name__ == "__main__":
    # Example usage
    scripts = {'AIRLINK'}
    result = get_script_data(scripts)
    export_script_data_to_csv(result, 'out.csv')

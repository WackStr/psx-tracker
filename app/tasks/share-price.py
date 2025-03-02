import requests
import os
from bs4 import BeautifulSoup
import time

db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")

def get_price(script: str) -> float:
    try:
        
        url = f"https://dps.psx.com.pk/company/{script}"
        
        r = requests.get(url)
        
        soup = BeautifulSoup(r.content, 'html5lib')
        
        div = soup.find('div', attrs = {'class':'quote__close'})
        return float(div.get_text(strip=True).replace("Rs.", "").replace(",",""))
    
    except Exception as e:
        print(f"Error fetching price for {script}: {e}")
        return 0.0

def get_price_for_scripts(scripts: set[str]) -> dict[str, float]:
    prices = {}
    wait = 0.5
    for script in scripts:
        prices[script] = get_price(script)
        time.sleep(wait)
    return prices

if __name__=="__main__":
    scripts = {}
    print(get_price_for_scripts(scripts))
    
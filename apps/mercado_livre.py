import requests
import re 
import json
import html
import time
from threading import Thread
from bs4 import BeautifulSoup


BRANDS = [
    "Yamaha", "Honda", "BMW", "Harley-Davidson",
    "Kawazaki", "Shinerey", "Mottu"
]

def main():
    brands_urls = list()
    for brand in BRANDS:
        url = f"https://www.olx.com.br/autos-e-pecas/motos/{brand}/estado-sc?q=motos&doc=1"
        brands_urls.append(url)

    print(brands_urls)
    #urls = get_product_urls(brands_urls)


def get_product_urls(urls):
    unique_product_urls = list()
    try:
        page = 1
        while soup.find('a', class_='next page-numbers') is not None:
            url = f""
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar todos os elementos h4 com a classe brxe-product-title
            product_titles = soup.find_all('h4', class_='brxe-product-title')
            product_urls = []
            # Extrair os links de cada produto
            for title in product_titles:
                link = title.find('a')
                if link and link.has_attr('href'):
                    product_url = link['href']
                    product_urls.append(product_url)

            # Remove duplicatas mantendo a ordem
            seen = set()
            for link in product_urls:
                if link not in seen:
                    seen.add(link)
                    unique_product_urls.append(link)
            page += 1
            
        print(len(unique_product_urls), "produtos encontrados")
        return unique_product_urls
    except requests.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return unique_product_urls


def get_motorcycle_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Extrair Título
        title_tag = soup.find('h1', class_='brxe-product-title')
        title = title_tag.get_text(strip=True) if title_tag else None

        motorcycle = {
            "title": None,
            "description": None,
            "city": None,
            "date": int(time.time() * 1000),
            "site": "webMotors",
            "brand": None,
            "kilometers": None,
            "price": None,
            "model": None, 
            "cc": None,        
            "url": url
        }
        
        return motorcycle
        
    except Exception as e:
        print(f"Erro ao processar a URL {url}: {e}")
        import traceback
        traceback.print_exc()
        return None
    
main()
import requests
import re 
import json
import html
import time
from threading import Thread
from bs4 import BeautifulSoup



'''BRANDS = [
    "Yamaha", "Honda", "BMW", "Harley-Davidson",
    "Kawazaki", "Suzuki", "Triumph", "Ducati"
]'''
BRANDS = ["Suzuki", "Ducati"]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0"
    }

def main():
    brands_urls = list()
    for brand in BRANDS:
        url = f"https://lista.mercadolivre.com.br/veiculos/motos/{brand.lower()}-em-santa-catarina/moto_NoIndex_True?sb=category"
        brands_urls.append(url)
        print(brand + ": " + url)

    print()
    urls = get_product_urls(brands_urls)

    motorcycles = get_motorcycle_data(urls[0:3])

    print(len(motorcycles)) if motorcycles else print("Nenhuma moto encontrada")

    for moto in motorcycles:
        for key, value in moto.items():
            print(f"{key}: {value}")
        print()


def get_product_urls(urls):
    unique_product_urls = list()
    try:
        for brand_url in urls:
            page = 2
            #url = f'{brand_url}&o={page}'
            response = requests.get(brand_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar o container principal dos produtos
            product_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid')
            
            if not product_container:
                # Se não encontrar pelo container específico, procura todos os links de produtos
                product_links = soup.find_all('a', class_='poly-component__title')
            else:
                # Encontrar todos os links de produtos dentro do container
                product_links = product_container.find_all('a', class_='poly-component__title')
            
            # Extrair as URLs
            for link in product_links:
                if link.has_attr('href'):
                    product_url = link['href']
                    
                    # Remover parâmetros de tracking se necessário
                    if 'tracking_id=' in product_url:
                        product_url = product_url.split('?')[0]
                    
                    unique_product_urls.append(product_url)

            
        print(len(unique_product_urls), "produtos encontrados")
        return unique_product_urls
    except requests.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return unique_product_urls


def get_motorcycle_data(urls):
    motorcycles = list()
    try:
        for url in urls:
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')


            title = soup.find('h1', class_='ui-pdp-title').text

            description = soup.find('p', class_='ui-pdp-description__content').text

            city = soup.find('p', class_='ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-media__title--plain').text

            # Encontrar todas as linhas da tabela
            rows = soup.find_all('tr', class_='andes-table__row')
            for row in rows:
                feature_th = row.find('th', class_='andes-table__header')
                if feature_th:
                    feature_name = feature_th.get_text(strip=True)
                    value_td = row.find('td', class_='andes-table__column')
                    if value_td:
                        value = value_td.get_text(strip=True)  
                        if feature_name == 'Modelo':
                            model = value
                        elif feature_name == 'Marca':
                            brand = value
                        elif feature_name == 'Cilindrada':
                            cc = value
                        elif feature_name == 'Quilômetros':
                            kilometers = value
                        elif feature_name == 'Ano':
                            year = value
                        elif feature_name == 'Cor':
                            color = value

            price = soup.find('span', class_='andes-money-amount__fraction').text
            #<span class="andes-money-amount__fraction" aria-hidden="true">8.900</span

            motorcycles.append({
                "title": title,
                "description": description,
                "city": city,
                "date": int(time.time() * 1000),
                "site": "Mercado Livre",
                "brand": brand,
                "kilometers": kilometers,
                "price": price,
                "model": model, 
                "cc": cc,
                "year": year,  
                "color": color,      
                "url": url
            })
        
        return motorcycles
        
    except Exception as e:
        print(f"Erro ao processar a URL {url}: {e}")
        import traceback
        traceback.print_exc()
        return motorcycles
    
main()
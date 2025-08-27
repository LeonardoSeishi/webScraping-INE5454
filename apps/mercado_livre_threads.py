import requests
import re 
import json
import html
import time
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

BRANDS = [
    "Yamaha", "Honda", "BMW", "Harley-Davidson",
    "Kawazaki", "Suzuki", "Triumph", "Ducati"
]

# Atualizar cookies se nececessario
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "Cookie": "_d2id=e665dd4a-e6b7-4520-84b2-83ba9e2077f3; ssid=ghy-061715-z4YaDm8rMpGrE7DGuKmPHcU6fLx9oC-__-187374176-__-1844881816290--RRR_0-RRR_0; orguseridp=187374176; orgnickp=LEONARDOSEISHIYAMAZAKI; ftid=H3S5056fDnAZD138UaP9GdHm4nQUo7GE-1750187360700; orguserid=h070h7HhT0ht; cookiesPreferencesNotLogged=%7B%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Atrue%2C%22performance%22%3Atrue%2C%22traceability%22%3Atrue%7D%7D; cookiesPreferencesLoggedFallback=%7B%22userId%22%3A187374176%2C%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Atrue%2C%22performance%22%3Atrue%2C%22traceability%22%3Atrue%7D%7D; cp=88036400; c_ui-navigation=6.6.144; LAST_SEARCH=yamaha%20r15; nsa_rotok=eyJhbGciOiJSUzI1NiIsImtpZCI6IjIiLCJ0eXAiOiJKV1QifQ.eyJpZGVudGlmaWVyIjoiNmE2M2FmNDktYTVjOS00NGNlLThiNjctNTdmZTBlZjNkZDQ0Iiwicm90YXRpb25faWQiOiJlYWNiMTdiOS0yMjAwLTRkY2EtYThjZC0wNzgwNTY3MGViZmIiLCJwbGF0Zm9ybSI6Ik1MIiwicm90YXRpb25fZGF0ZSI6MTc1NjI1NDg2NSwiZXhwIjoxNzU4ODQ2MjY1LCJqdGkiOiIzZTM3NjdmMi00YWIxLTQyZmMtOGE0MC1kYTc5YjYxZTE4M2YiLCJpYXQiOjE3NTYyNTQyNjUsInN1YiI6IjZhNjNhZjQ5LWE1YzktNDRjZS04YjY3LTU3ZmUwZWYzZGQ0NCJ9.fS5ryKdOQPrTurciGURPciJoiiR_nbEJ8PXXOGDWGok-e2tDBFueNp5DIdwQrvbdEtBjdchzCS16nJRx54ENGLT5ShTp3BYH6PyNBh12wk3YKRTlkSWwd8jwbkGawhYDaLFq2rvO9QuMi2U8G3qCfzUOs2yrgNiBdjA_I_VXul6LO7hmfHE8cqC3dBcsmsgyt4wN9qVzp0SwbRtguE5M2Dvd2wHaSUgSbpBETKYFOeUSaAbZksrjhOpmOqpqroNtRPs3Yfh7g04AT4iiv25eb2a0LU-my4hapIEy2Zs9RwYdFCORUIypCiMvw6LfSEqfT4OfDTuh5PU1Ts5cFw5OZw; _csrf=bIPwI2aL8OB-pLrC9hkOEwCT; main_domain=; main_attributes=; categories=; last_query=moto; category=MLB1763; backend_dejavu_info=j%3A%7B%7D; _mldataSessionId=2c3db086-16f6-4c76-9b72-507ab0bcdf08; hide-cookie-banner=187374176-COOKIE_PREFERENCES_ALREADY_SET; cookiesPreferencesLogged=%7B%22userId%22%3A187374176%2C%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Atrue%2C%22performance%22%3Atrue%2C%22traceability%22%3Atrue%7D%7D; aws-waf-token=676c28e0-a488-4c45-8e0b-dfc5bc4d0c70:EAoAc68B41rmAQAA:GPIy4EKmjXUbDyaQ/jZ/dAxEq0zblrxTGtU7WMAAQgQUe7vk2oZNnTFVNb98PYt5WVw+0nfGF9EptqXtOOBONs71oAsXJ33pnojmFzgXn5aWdSl6a6pgN04HJSga14+rIG5xNWKX6VUWuEMzNJ4dXF5iqzs5XZs+kc/R2HQ6m7glulGPjRvCBZow5IHMjdo6cqotMu9DDNrrCBaI5Ra6uAgcp1k2PZ4=",
    }


# Lock para evitar problemas de concorrência
urls_lock = Lock()
data_lock = Lock()

def main():
    brands_urls = dict()
    print("URLs das marcas:")
    for brand in BRANDS:
        url = f"https://lista.mercadolivre.com.br/veiculos/motos/{brand.lower()}-em-santa-catarina/moto_NoIndex_True?sb=category"
        brands_urls[brand] = url
        print(f"{brand}: {url}")

    print()

    # Coletar URLs com threads
    urls = get_product_urls_threaded(brands_urls)
    print(f"\n{len(urls)} produtos encontrados\n")

    motorcycles = get_motorcycles_data_threaded(urls)
    
    print(f"\n{len(motorcycles)} motos processadas\n" if motorcycles else "Nenhuma moto encontrada\n")
    
    '''for moto in motorcycles:
        for key, value in moto.items():
            print(f"{key}: {value}")
        print()'''
    
    save_data(motorcycles, '../result/mercado_livre.json')


def get_product_urls_threaded(brands_urls, max_workers=4):
    """Coleta URLs de produtos de TODAS as páginas usando ThreadPoolExecutor"""
    unique_product_urls = []

    # Usar session para manter cookies
    session = requests.Session()
    session.headers.update(headers)
    
    def fetch_urls_with_pagination(initial_brand_url):
        """Busca URLs de produtos de TODAS as páginas a partir de uma URL inicial"""
        all_urls_from_brand = []
        brand, current_url = initial_brand_url
        page_count = 0
        
        while current_url:
            try:
                page_count += 1    
                response = session.get(current_url, timeout=15)       
                #response = requests.get(current_url, headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extrair URLs dos produtos desta página
                product_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid')
                if not product_container:
                    product_links = soup.find_all('a', class_='poly-component__title')
                else:
                    product_links = product_container.find_all('a', class_='poly-component__title')
                
                urls_from_page = []
                for link in product_links:
                    if link.has_attr('href'):
                        product_url = link['href']
                        if 'tracking_id=' in product_url:
                            product_url = product_url.split('?')[0]
                        urls_from_page.append(product_url)
                
                all_urls_from_brand.extend(urls_from_page)
                
                # Verificar se há próxima página
                next_button = soup.find('li', class_='andes-pagination__button--next')
                if not next_button:
                    break
                if next_button and 'andes-pagination__button--disabled' in next_button.get('class', []):
                    break
                
                current_url = f"https://lista.mercadolivre.com.br/veiculos/motos/{brand}-em-santa-catarina/moto_Desde_{(page_count*48) + 1}_NoIndex_True?sb=category"
                # Pequena pausa para não sobrecarregar
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Erro ao processar página {current_url}: {e}")
                break
        
        return all_urls_from_brand, page_count

    # Processar cada URL de marca em threads separadas
    with ThreadPoolExecutor(max_workers=min(max_workers, 4)) as executor:
        futures = {executor.submit(fetch_urls_with_pagination, brand_url): brand_url for brand_url in brands_urls.items()}
        
        for future in as_completed(futures):
            brand_url = futures[future]
            try:
                urls_from_brand, pages_processed = future.result()
                with urls_lock:
                    unique_product_urls.extend(urls_from_brand)
                print(f"Processadas {pages_processed} páginas de {brand_url[0]} - {len(urls_from_brand)} produtos")
            except Exception as e:
                print(f"Erro ao processar marca {brand_url}: {e}")

    return list(set(unique_product_urls))  # Remover duplicatas

def get_motorcycles_data_threaded(urls, max_workers=2):
    """Coleta dados das motos usando ThreadPoolExecutor"""
    motorcycles = []

    # Usar session para manter cookies
    session = requests.Session()
    session.headers.update(headers)
    
    def process_motorcycle(url):
        try:
            response = session.get(url, timeout=15)
            #response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extrair dados com tratamento de erros
            title = soup.find('h1', class_='ui-pdp-title')
            title = title.text.strip() if title else "Título não encontrado"
            
            description = soup.find('p', class_='ui-pdp-description__content')
            description = description.text.strip() if description else "Descrição não encontrada"
            
            city = soup.find('p', class_='ui-pdp-color--BLACK')
            city = city.text.strip() if city else "Cidade não encontrada"
            
            price = soup.find('span', class_='andes-money-amount__fraction')
            price = price.text.strip() if price else "Preço não encontrado"

            # Inicializar variáveis
            model = None
            brand = None
            cc = None
            kilometers = None
            year = None
            color = None

            # Extrair dados da tabela
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

            motorcycle_data = {
                "site": "Mercado Livre",
                "url": url,
                "data": int(time.time() * 1000),
                "titulo": title,
                "descricao": description,
                "cidade": city,
                "preco": limpar_numero(price),
                "modelo": model,
                "marca": brand,
                "cilindradas": limpar_numero(cc),
                "quilometragem": limpar_numero(kilometers),
                "ano": year,
                "cor": color
            }
            
            # Adicionar dados de forma thread-safe
            with data_lock:
                motorcycles.append(motorcycle_data)
            
            return True
            
        except Exception as e:
            print(f"Erro ao processar a URL {url}: {e}")
            return False

    # Usar ThreadPoolExecutor para processar motos em paralelo
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_motorcycle, url): url for url in urls}
        
        completed = 0
        for future in as_completed(futures):
            url = futures[future]
            try:
                success = future.result()
                if success:
                    completed += 1
                    print(f"Processada moto {completed}/{len(urls)}: {url[:60]}...")
            except Exception as e:
                print(f"Erro fatal no processamento de {url}: {e}")

    return motorcycles

def limpar_numero(numero_str):
    if numero_str:
        # Remove pontos, espaços e unidades de medida
        texto_limpo = numero_str.replace('.', '').replace(' ', '').replace('km', '').replace('cc', '')
        return int(texto_limpo) if texto_limpo.isdigit() else 0
    return 0

def save_data(dados, nome_arquivo='../result/mercado_livre.json'):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos com sucesso em {nome_arquivo}")
        return True
    except Exception as e:
        print(f"Erro ao salvar JSON: {e}")
        return False

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")
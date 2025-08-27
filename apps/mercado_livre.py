import requests
import re 
import json
import html
import time
from bs4 import BeautifulSoup



BRANDS = [
    "Yamaha", "Honda", "BMW", "Harley-Davidson",
    "Kawazaki", "Suzuki", "Triumph", "Ducati"
]
BRANDS=["Honda"]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Cookie": "_d2id=3b7be2f3-c2d2-4ba1-ab44-aa8cb5d3a58b; _mldataSessionId=006c99bf-6b15-4653-80af-7b4597d34d4c; ftid=2vrGEEPdjGhptgB0twJK3VptBX5sgP0w-1756252933870; ssid=ghy-082620-5RBsKWXXNvvxY336f8PQhgdFK3ZNxi-__-2648743767-__-1850947458668--RRR_0-RRR_0; orguseridp=2648743767; orgnickp=SL20250826200256; orguserid=0Zt7Tt7hTHhth; cookiesPreferencesLogged=%7B%22userId%22%3A2648743767%2C%22categories%22%3A%7B%22advertising%22%3Anull%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D; cookiesPreferencesLoggedFallback=%7B%22userId%22%3A2648743767%2C%22categories%22%3A%7B%22advertising%22%3Anull%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D; cookiesPreferencesNotLogged=%7B%22categories%22%3A%7B%22advertising%22%3Anull%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D; x-meli-session-id=armor.3529cd18675b2b8897c69887cd9a71c611976cba60045a6ab8d463e146b5cc2210c4e575aab357bf9d9d5cce896af7438c399aad055ee265c3ca9f89188e42c1240ab36b04519ed4e9b1b3ea6036efad62af4167580f0476dd6e0e3a827642b3.3bd9e119a90ff94e4831fb4f62fa2d66; nsa_rotok=eyJhbGciOiJSUzI1NiIsImtpZCI6IjIiLCJ0eXAiOiJKV1QifQ.eyJpZGVudGlmaWVyIjoiMWYzY2NmMWYtZDRhYS00OGY1LThkNGEtYWU0MzhiOTgxMjI3Iiwicm90YXRpb25faWQiOiJhMzAyZDc3ZC1lYWI5LTQ5OWYtODY5OC1iMmQ0MDFkZTlmZDciLCJwbGF0Zm9ybSI6Ik1MIiwicm90YXRpb25fZGF0ZSI6MTc1NjI1MzY1OSwiZXhwIjoxNzU4ODQ1MDU5LCJqdGkiOiJlYTNlYmJjNi1hNDMzLTQ1NTUtOGI0Yy1jMTBkYWYwYzVhN2EiLCJpYXQiOjE3NTYyNTMwNTksInN1YiI6IjFmM2NjZjFmLWQ0YWEtNDhmNS04ZDRhLWFlNDM4Yjk4MTIyNyJ9.MS5LxJMAZFajR26REebGrhqodiV6Yio4lIjDfg3BbK3SSjArDIgMw9Sv-Si1bTSwn3g4KokOXXJ6MVNBPYfKqyp8micvCDnx-S1GuovxyD_CozIYg8yLLD_WBP5KYFU3WzhxrWUF6bnxZIJuQioracNJlXm-s6SzWndJsIuQ89AeCyM9wjJoeqfbG5h2BgT4oRm0v3YR91O2GDA_oYnKAUC_o2kd93TJL2xHqVbDFpZXRZ9CMFPoQHm4i8syVQ4CetNyTdOFNin3tqHr_b3X0FEeeKzX4yxW_bDv8hZ5AZ3RFUm_3ODbouc_aqr2wN_AKqyaSYgCiXCqtipbMnXSxg; _csrf=mmQwTQ6Ht38YUzTiMK1haKcX; main_domain=; main_attributes=; categories=; last_query=moto; category=MLB1763; backend_dejavu_info=j%3A%7B%7D; c_ui-navigation=6.6.144; aws-waf-token=676c28e0-a488-4c45-8e0b-dfc5bc4d0c70:EAoAbceoHnsuAwAA:eXU4yoB4O7bQre1/NnsPyDTozOkzbk4cdkkuLc77UGck6w8WrK8Y5m7GAz6vEd7DEGwcHHS4WYdxqYx9iIH5icP+MblLa6b1Pa8uwnWfAv90z+pOKwwL9bqraok6l0uh0z4lHT+H7CxWL828YByF1bed2mbSTG+/Yqq64Yq4jJNCp/BQ6WvbXydz+S1yP5xZJhN7i53ImkaKPr6BqMvX8NrX06NoayokN0ZBPLCl06Qsd32PXvsH8jW0eHzm5LllPvk="
    }

def main():
    brands_urls = dict()
    for brand in BRANDS:
        url = f"https://lista.mercadolivre.com.br/veiculos/motos/{brand.lower()}-em-santa-catarina/moto_NoIndex_True?sb=category"
        brands_urls[brand] = url
        print(brand + ": " + url)

    print()
    urls = get_product_urls(brands_urls)

    print(len(urls), "produtos encontrados")

    #motorcycles = get_motorcycles_data(urls)

    #save_data(motorcycles, '../result/mercado_livre.json')


def get_product_urls(brands_urls):
    unique_product_urls = list()
    # Usar session para manter cookies
    session = requests.Session()
    session.headers.update(headers)
    try:
        for brand_url in brands_urls.items():
            brand, current_url = brand_url
            page_count = 0
            product_from_brand = list()
            while current_url:
                page_count += 1
                response = session.get(current_url, timeout=15)
                #response = requests.get(current_url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extrair URLs dos produtos desta página
                product_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid')
                if not product_container:
                    product_links = soup.find_all('a', class_='poly-component__title')
                else:
                    product_links = product_container.find_all('a', class_='poly-component__title')
                
                # Extrair as URLs
                for link in product_links:
                    if link.has_attr('href'):
                        product_url = link['href']
                        if 'tracking_id=' in product_url:
                            product_url = product_url.split('?')[0]
                        product_from_brand.append(product_url)

                # Verificar se há próxima página
                #class="andes-pagination__button andes-pagination__button--next andes-pagination__button--disabled"
                next_button = soup.find('li', class_='andes-pagination__button andes-pagination__button--next')

                if next_button:
                    # Verificar se o botão está desabilitado
                    if 'andes-pagination__button--disabled' in next_button.get('class', []):
                        print("O botão está desabilitado - fim da paginação")
                        break
                    else:
                        print("O botão está habilitado - há mais páginas")
                else:
                    print("Botão próximo não encontrado - fim da paginação")
                    break
                
                current_url = f"https://lista.mercadolivre.com.br/veiculos/motos/{brand}-em-santa-catarina/moto_Desde_{(page_count*48) + 1}_NoIndex_True?sb=category"
                # Pequena pausa para não sobrecarregar
                time.sleep(0.5)

            print(f'{page_count} paginas de {brand}: {len(product_from_brand)} produtos encontrados')
            unique_product_urls.extend(product_from_brand)

        return unique_product_urls
    except requests.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return unique_product_urls


def get_motorcycles_data(urls):
    motorcycles = list()
    # Usar session para manter cookies
    session = requests.Session()
    session.headers.update(headers)

    for url in urls:
        try:
            response = session.get(url, timeout=15)
            #response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

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

            moto = {
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

            motorcycles.append(moto)
        except:
            continue
    
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
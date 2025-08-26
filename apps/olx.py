import requests
import re 
import json
import html
import time
from threading import Thread
from bs4 import BeautifulSoup

 #  USE SELENIUM


'''BRANDS = [
    "Yamaha", "Honda", "BMW", "Harley-Davidson",
    "Kawazaki", "Shinerey", "Mottu"
]'''
BRANDS = ["Harley-Davidson", "Yamaha"]

def main():
    brands_urls = list()
    for brand in BRANDS:
        url = f"https://www.olx.com.br/autos-e-pecas/motos/{brand.lower()}/estado-sc?q=motos&doc=1"
        brands_urls.append(url)

    print(brands_urls)
    print()
    urls = get_product_urls(brands_urls)

    #data = get_motorcycle_data(urls[0])




def get_product_urls(urls):
    unique_product_urls = list()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.olx.com.br/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        # Copie o valor do seu cookie do navegador para cá:
        "Cookie": "r_id=1bdf9f64-eb5d-4e50-8a96-8b86fd083acb; nl_id=f9946c4c-c76d-4655-a378-0ce60761a45b; cf_clearance=OkCKFzIAQXFHXjamCUFeWzfcPnb6sBzrKdIoI0BcCKE-1755633422-1.2.1.1-BrSA39J8jpZiTSPbxjFbMEgIYEABJ9_8RLKhYSzL6V.4vqeNqzGw4DeZzhRoE36I4HLgTxdTDbDNS4QbtQeYe60ZmIV7sdVI4COk.E2e5c8nrwAmU.jXRQeJE87KXCnOA42xtboGfpqtDN5llijZCKV9xFGymoHVXFkBsGi5n.6i2DPOFhjJw.w385k8XpVjd5hmA5TLAJ8A1V2zbpCNW2XPKSx5KwP8nNPWQgt1gvE; _cfuvid=X5evH93.B2TSPip5o5mOJWgHDTQUF0JAZoUF4QnEj4I-1755876067872-0.0.1.1-604800000; _lr_geo_location_state=SC; _lr_geo_location=BR; __cf_bm=xV_58ew_1IY_I2i0dgy4FXe_qr8nS.c9IV_s3EJJK.A-1755879270-1.0.1.1-Ju5feAVxKapBdo6ih1DMOPNXcKdVLP5NNgRZg0XeWi2ifgtQkPSLE2sHn1q7Qpbyb6owgoOuJhU7TxpAygk0Ot7edf7wlJu3zgCMps0FSUg; TestAB_Groups=swifakep3_control.klubirecu2_enabled.payg-discount-re-julius_ml-ranges.adv-adee01_enabled.sa-ai-fg_D.ppoplancta_control.ln-recad_A.sxp-acth_enabled.acc-tip-lg_enabled.acc-tip-sa_enabled.klubi-adv_enabled.plat-stdRE_enabled.sa-new-bff_A.adextrapel_enabled.sa-tradein_enabled.sanityweb50_A.frigoogll_disable.lst-re-mp_enabled.se-tipchat_A.ai-edit_control.opt-renew_enabled.dpd-aiout_enabled.acc-doc-ls_enabled.modal-ab_control.ppf-di-exp_enabled.bconShipRg_enabled.adv-li25c0_control.palqpcserv_bff.p-emp-bdge_enabled.cdrelPLoan_enabled.atvleadper_enabled.acc-csoci_new.earlyrnw_control.ln-recchat_A.ppofrautnc_control.atvleadcha_enabled.Md-shwphne_control.ad-coupon_control.cdrelALoan_control.ppofrcars_enabled.sellerphon_control.sellerchat_control.cdrel-gps_control"
        }
    try:
        for brand_url in urls:
            page = 2
            url = "https://www.olx.com.br/autos-e-pecas/motos/harley-davidson/estado-sc?q=motos&doc=1&o=2"
            #url = f'{brand_url}&o={page}'
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar o container principal dos produtos
            product_container = soup.find('div', class_='AdListing_adListContainer__ALQla AdListing_gridLayout__DTjHC')
            
            if product_container:
                # Encontrar todos os links de produtos
                product_links = product_container.find_all('a', {'data-testid': 'adcard-link'})
                
                # Extrair as URLs
                for link in product_links:
                    if link.has_attr('href'):
                        product_url = link['href']
                        unique_product_urls.append(product_url)

            
        print(len(unique_product_urls), "produtos encontrados")
        return unique_product_urls
    except requests.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return unique_product_urls


def get_motorcycle_data(url):
    try:
        '''response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Extrair Título
        title_tag = soup.find('h1', class_='brxe-product-title')
        title = title_tag.get_text(strip=True) if title_tag else None'''

        motorcycle = {
            "title": None,
            "description": None,
            "city": None,
            "date": int(time.time() * 1000),
            "site": "OLX",
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
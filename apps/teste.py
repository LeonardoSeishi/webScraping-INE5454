import requests
import re 
import json
import html
import time
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from urllib.parse import unquote, unquote_plus



        

'''url = "https://lista.mercadolivre.com.br/veiculos/motos-em-santa-catarina/moto-kawazaki_NoIndex_True"
unique_product_urls = list()

response = requests.get(url)
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

print(len(unique_product_urls), "produtos encontrados")'''

query_str = "action=jet_smart_filters&provider=jet-woo-products-grid%2Ffiltro-descartables&defaults%5Bpost_type%5D=product&defaults%5Btax_query%5D%5B0%5D%5Btaxonomy%5D=product_cat&defaults%5Btax_query%5D%5B0%5D%5Bfield%5D=term_id&defaults%5Btax_query%5D%5B0%5D%5Bterms%5D%5B%5D=24&defaults%5Btax_query%5D%5B0%5D%5Boperator%5D=IN&defaults%5Btax_query%5D%5B1%5D%5Btaxonomy%5D=product_visibility&defaults%5Btax_query%5D%5B1%5D%5Bfield%5D=name&defaults%5Btax_query%5D%5B1%5D%5Bterms%5D%5B%5D=exclude-from-catalog&defaults%5Btax_query%5D%5B1%5D%5Boperator%5D=NOT+IN&defaults%5Borderby%5D=date&defaults%5Border%5D=DESC&defaults%5Bposts_per_page%5D=42&settings%5Bshow_compare%5D=&settings%5Bcompare_button_order%5D=&settings%5Bcompare_button_order_tablet%5D=&settings%5Bcompare_button_order_mobile%5D=&settings%5Bcompare_button_icon_normal%5D=&settings%5Bselected_compare_button_icon_normal%5D=&settings%5Bcompare_button_label_normal%5D=&settings%5Bcompare_button_icon_added%5D=&settings%5Bselected_compare_button_icon_added%5D=&settings%5Bcompare_button_label_added%5D=&settings%5Bcompare_use_button_icon%5D=&settings%5Bcompare_button_icon_position%5D=&settings%5Bcompare_use_as_remove_button%5D=&settings%5Bshow_wishlist%5D=&settings%5Bwishlist_button_order%5D=&settings%5Bwishlist_button_order_tablet%5D=&settings%5Bwishlist_button_order_mobile%5D=&settings%5Bwishlist_button_icon_normal%5D=&settings%5Bselected_wishlist_button_icon_normal%5D=&settings%5Bwishlist_button_label_normal%5D=&settings%5Bwishlist_button_icon_added%5D=&settings%5Bselected_wishlist_button_icon_added%5D=&settings%5Bwishlist_button_label_added%5D=&settings%5Bwishlist_use_button_icon%5D=&settings%5Bwishlist_button_icon_position%5D=&settings%5Bwishlist_use_as_remove_button%5D=&settings%5Bshow_quickview%5D=&settings%5Bquickview_button_order%5D=&settings%5Bquickview_button_icon_normal%5D=&settings%5Bselected_quickview_button_icon_normal%5D=&settings%5Bquickview_button_label_normal%5D=&settings%5Bquickview_use_button_icon%5D=&settings%5Bquickview_button_icon_position%5D=&settings%5Bjet_woo_builder_qv%5D=&settings%5Bjet_woo_builder_qv_template%5D=&settings%5Bjet_woo_builder_cart_popup%5D=&settings%5Bjet_woo_builder_cart_popup_template%5D=&settings%5Bcarousel_enabled%5D=&settings%5Bcarousel_direction%5D=horizontal&settings%5Bprev_arrow%5D=&settings%5Bselected_prev_arrow%5D=&settings%5Bnext_arrow%5D=&settings%5Bselected_next_arrow%5D=&settings%5Benable_custom_query%5D=&settings%5Bcustom_query_id%5D=&settings%5B_el_widget_id%5D=f815cc0&settings%5B_widget_id%5D=f815cc0&settings%5Bpresets%5D=preset-2&settings%5Bcolumns%5D=6&settings%5Bhover_on_touch%5D=&settings%5Bequal_height_cols%5D=&settings%5Bcolumns_gap%5D=yes&settings%5Brows_gap%5D=yes&settings%5Bhidden_products%5D=&settings%5Bclickable_item%5D=&settings%5Bopen_new_tab%5D=&settings%5Buse_current_query%5D=&settings%5Bnumber%5D=42&settings%5Bproducts_query%5D=category&settings%5Bproducts_exclude_ids%5D=&settings%5Bproducts_ids%5D=&settings%5Bproducts_cat%5D=24&settings%5Bproducts_cat_exclude%5D=&settings%5Bproducts_tag%5D=&settings%5Btaxonomy_slug%5D=&settings%5Btaxonomy_id%5D=&settings%5Bproducts_stock_status%5D=&settings%5Bvariation_post_parent_id%5D=&settings%5Bproducts_orderby%5D=default&settings%5Bproducts_order%5D=desc&settings%5Bshow_title%5D=yes&settings%5Badd_title_link%5D=yes&settings%5Btitle_html_tag%5D=h5&settings%5Btitle_trim_type%5D=word&settings%5Btitle_length%5D=-1&settings%5Btitle_line_wrap%5D=&settings%5Btitle_tooltip%5D=&settings%5Benable_thumb_effect%5D=yes&settings%5Badd_thumb_link%5D=yes&settings%5Bthumb_size%5D=woocommerce_thumbnail&settings%5Bshow_badges%5D=yes&settings%5Bsale_badge_text%5D=%C2%A1Promoci%C3%B3n!&settings%5Bshow_excerpt%5D=&settings%5Bexcerpt_trim_type%5D=&settings%5Bexcerpt_length%5D=&settings%5Bshow_cat%5D=&settings%5Bcategories_count%5D=&settings%5Bshow_tag%5D=&settings%5Btags_count%5D=&settings%5Bshow_price%5D=yes&settings%5Bshow_stock_status%5D=&settings%5Bin_stock_status_text%5D=&settings%5Bon_backorder_status_text%5D=&settings%5Bout_of_stock_status_text%5D=&settings%5Bshow_rating%5D=yes&settings%5Bshow_rating_empty%5D=&settings%5Bshow_sku%5D=&settings%5Bshow_button%5D=&settings%5Bshow_quantity%5D=&settings%5Bbutton_use_ajax_style%5D=&settings%5Bnot_found_message%5D=Productos+no+Encontrados&settings%5Bquery_id%5D=&settings%5B_element_id%5D=filtro-descartables&settings%5Bjsf_signature%5D=404ce518d6d4b037e3822281f5e221c8&props%5Bfound_posts%5D=141&props%5Bmax_num_pages%5D=4&props%5Bpage%5D=0&paged=2&referrer%5Buri%5D=%2Fdescartables%2F&referrer%5Binfo%5D=&referrer%5Bself%5D=%2Findex.php&indexing_filters=%5B3398%2C2858%2C2860%5D"

str_list = query_str.split('&')

params_dict = {}
for param in str_list:
    parts = param.split('=', 1)
    key = unquote(parts[0])
    value = unquote_plus(parts[1]) if len(parts) > 1 else ''
    params_dict[key] = value

# Exibir alguns exemplos
for key, value in list(params_dict.items()):
    print(f"'{key}': '{value}'")
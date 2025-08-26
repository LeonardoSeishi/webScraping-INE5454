import json
from collections import Counter

def processar_arquivo_json(nome_arquivo):
    try:
        # Ler o arquivo JSON
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            dados = json.load(file)
        
        # Filtrar produtos com preço diferente de 0
        produtos_validos = [produto for produto in dados if produto.get('preco', 0) > 0]
        
        # Quantidade de produtos
        quantidade_total = len(dados)
        quantidade_validos = len(produtos_validos)
        quantidade_removidos = quantidade_total - quantidade_validos
        
        # Preços mais alto e mais baixo
        if produtos_validos:
            preco_mais_alto = max(produtos_validos, key=lambda x: x.get('preco', 0))
            preco_mais_baixo = min(produtos_validos, key=lambda x: x.get('preco', 0))
        else:
            preco_mais_alto = None
            preco_mais_baixo = None
        
        # Contar produtos por marca
        contador_marcas = Counter(produto.get('marca', 'Desconhecida') for produto in produtos_validos)
        
        # Exibir resultados
        print(f"=== ANÁLISE DO ARQUIVO: {nome_arquivo} ===")
        print(f"Quantidade total de produtos: {quantidade_total}")
        print(f"Produtos com dados válidos: {quantidade_validos}")
        print(f"Produtos removidos: {quantidade_removidos}")
        print()
        
        if produtos_validos:
            print(f"Preço mais alto: R$ {preco_mais_alto['preco']:,.2f}")
            print(f"  - Produto: {preco_mais_alto['titulo']}")
            print(f"  - Marca: {preco_mais_alto.get('marca', 'N/A')}")
            print()
            
            print(f"Preço mais baixo: R$ {preco_mais_baixo['preco']:,.2f}")
            print(f"  - Produto: {preco_mais_baixo['titulo']}")
            print(f"  - Marca: {preco_mais_baixo.get('marca', 'N/A')}")
            print()
        
        print("Quantidade por marca:")
        for marca, quantidade in contador_marcas.most_common():
            print(f"  - {marca}: {quantidade} produto(s)")
        
        # Retornar os dados processados
        return {
            'produtos_validos': produtos_validos,
            'quantidade_total': quantidade_total,
            'quantidade_validos': quantidade_validos,
            'preco_mais_alto': preco_mais_alto,
            'preco_mais_baixo': preco_mais_baixo,
            'contador_marcas': dict(contador_marcas)
        }
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Arquivo '{nome_arquivo}' não é um JSON válido.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

# Função principal para executar o processamento
def main():
    nome_arquivo = "result/mercado_livre_teste1.json"
    resultado = processar_arquivo_json(nome_arquivo)
    
    # Opcional: Salvar os dados filtrados em um novo arquivo
    if resultado and resultado['produtos_validos']:
        salvar = input("\nDeseja salvar os produtos válidos em um novo arquivo? (s/n): ").lower()
        if salvar == 's':
            nome_saida = nome_arquivo.replace('.json', '_filtrado.json')
            with open(nome_saida, 'w', encoding='utf-8') as file:
                json.dump(resultado['produtos_validos'], file, ensure_ascii=False, indent=2)
            print(f"Arquivo salvo como: {nome_saida}")

# Executar o programa
if __name__ == "__main__":
    main()
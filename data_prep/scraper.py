import requests
from bs4 import BeautifulSoup

OUT_DIR = 'data/'

# URL da página que você quer fazer o scraping
guides = {
    'mercado_fracionario_de_acoes': 'https://www.infomoney.com.br/guias/mercado-fracionario-de-acoes/',
    'tesouro_direto': 'https://www.infomoney.com.br/guias/tesouro-direto/',
    'inflacao': 'https://www.infomoney.com.br/guias/inflacao/',
}

for guide_name, url in guides.items():
    # Fazendo uma requisição para o site
    response = requests.get(url)

    # Checando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parsing do conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrando o conteúdo da notícia
        article = soup.find('article')  # O conteúdo geralmente está dentro da tag <article>
        
        # Extraindo o texto da notícia
        if article:
            paragraphs = article.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            with open(f'{OUT_DIR}{guide_name}.txt', 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print("Artigo não encontrado.")
    else:
        print(f"Falha ao acessar a página. Status code: {response.status_code}")

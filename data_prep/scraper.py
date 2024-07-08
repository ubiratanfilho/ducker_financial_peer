import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL do site de onde queremos extrair os dados
url = "https://www.infomoney.com.br/guias/"

# Realiza a requisição para o site
response = requests.get(url)
# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontra todos os artigos de educação financeira
    articles = soup.find_all('article', class_='card__Content-sc-1uk0bgb-6')
    
    # Lista para armazenar os dados dos artigos
    data = []
    
    # Extrai os dados de cada artigo
    for article in articles:
        title = article.find('h3').text.strip()
        link = article.find('a')['href']
        
        # Adiciona os dados extraídos à lista
        data.append({
            'Title': title,
            'Link': link
        })
    
    # Cria um DataFrame a partir dos dados extraídos
    df = pd.DataFrame(data)
    
    # Salva os dados em um arquivo CSV
    df.to_csv('financial_education_articles.csv', index=False)
    
    print("Dados extraídos e salvos com sucesso!")
else:
    print(f"Falha na requisição. Status code: {response.status_code}")

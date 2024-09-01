# Ducker - Seu Tutor de Educação Financeira

<img src="images\logo.webp" alt="Logo do Ducker" width="100"/>

## Vídeo
![](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmozejR6ZXloZ3ZseGVtZjR2Z2FtMGc1Mm1xbTlhc3JwNGFmZWo5MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2a01NHfB3sj9Ba4zTc/giphy.gif)

## Descrição

O Ducker é uma aplicação de IA Generativa que tem como objetivo ensinar o usuário sobre educação financeira a partir de um catálogo de cursos interativos.

Link para a aplicação: https://ducker.streamlit.app/

## Como utilizar

1. Clone o repositório
   ```sh
    git clone https://github.com/ubiratanfilho/ducker_financial_peer
    ```

2. Instale as dependências
    ```sh
    pip install -r requirements.txt
    ```

3. Adicione um arquivo `secrets.toml` dentro da pasta `.streamlit/` com as seguintes informações:
    ```toml
    OPEN_AI_API_KEY = "sua_chave_de_api"
    OPEN_AI_MODEL = "sua_chave_de_modelo"  # (exemplo "gpt-3.5-turbo")
    ```

4. Execute a aplicação
    ```sh
    streamlit run app.py
    ```

## Autores
- Ubiratan Filho: https://github.com/ubiratanfilho
- Bruno Bertanha: https://github.com/bruno-bertanha
- Luan Teixeira: https://github.com/IMTTeixeira
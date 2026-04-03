import os
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Obtém a chave da variável de ambiente
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Erro: Chave de API não encontrada no arquivo .env")
else:
    # Inicializa o cliente usando o novo SDK
    client = genai.Client(api_key=api_key)

    # Gera o conteúdo passando o modelo e o prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Por que é importante variáveis de ambiente?'
    )
    
    print(response.text)
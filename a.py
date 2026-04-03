import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Obtém a chave da variável de ambiente
api_key = os.getenv("GOOGLE_API_KEY")

# Configura o SDK com a chave obtida
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Erro: Chave de API não encontrada no arquivo .env")

# Inicializa o modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# Exemplo de uso
response = model.generate_content("Por que é importante usar variáveis de ambiente?")
print(response.text)
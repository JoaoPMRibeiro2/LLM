### 📝 Descrição do Projeto
<p align = "justify">&emsp;&emsp;O Gpteculos 2.0 é uma aplicação web interativa que utiliza inteligência artificial para criar uma experiência de chat propositalmente caótica e bem-humorada. Ao contrário de assistentes convencionais, esta IA é configurada para ser "inútil e atrapalhada", respondendo de forma complexa, redundante e com informações propositalmente imprecisas, mantendo sempre um tom amigável e confiante. É uma ferramenta de entretenimento que explora a flexibilidade das instruções de sistema em modelos de linguagem de grande escala (LLMs).</p>

---

### 🛠️ Tecnologias Utilizadas

 - **Python (3.13.12)**: Linguagem de programação base.

 - **Streamlit (1.56.0)**: Framework utilizado para a criação da interface gráfica e gerenciamento do estado da sessão do chat.

 - **Google GenAI SDK (1.70.0)**: Biblioteca oficial para integração com os modelos Gemini da Google.

 - **Modelo Gemini 3.1 Flash-Lite-Preview**: O motor de IA utilizado para processar as mensagens.

 - **Python-dotenv (1.2.2)**: Para o gerenciamento seguro de variáveis de ambiente (chaves de API).

--- 

### 🚀Instruções de execução

<p align = "justify">&emsp;&emsp;Para executar a aplicação, faz-se necessário instalar os seguintes pacotes: </p>
 
  - google-genai 
  - python-dotenv 
  - streamlit

```bash
pip install -U google-genai python-dotenv streamlit
```

---

### ⚠️ | Atenção 

<p align = "justify">&emsp;&emsp;A chave do agente utilizado não está presente no repositório, pois, ao envia-la para o GitHub, será derrubada pelo próprio Google. Sendo assim, cabe a você:</p>

  - Criar um arquivo .env na pasta src 
  - Utilizar a sua própria chave

 <div align="center">
  <kbd>
    <img src="img/env.png" alt="Modelo do arquivo .env na pasta indicada "><br>
    Arquivo .env na pasta indicada contendo a key adquirida
  </kbd>
</div>
   
---

### ❓ | Ajuda
Como obter chave gratuita: https://www.youtube.com/watch?v=Uyn-P2nRvDA&t=14s

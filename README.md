### 📝 Descrição do Projeto
<p align="justify">&emsp;&emsp;O <b>Guia de Saúde</b> é uma aplicação web interativa desenvolvida para atuar como um assistente virtual focado em pré-triagem e orientação de sintomas. Ao interagir com o utilizador, a Inteligência Artificial recolhe informações sobre o quadro clínico, formula hipóteses (sem fornecer diagnósticos definitivos) e encaminha para a especialidade médica mais adequada.</p>

---

### 🛠️ Tecnologias Utilizadas

 - **Python (3.13.12)**: Linguagem de programação base.

 - **Streamlit (1.56.0)**: Framework utilizado para a criação da interface gráfica e gerenciamento do estado da sessão do chat.

 - **Google GenAI SDK (1.70.0)**: Biblioteca oficial para integração com os modelos Gemini da Google.

 - **Modelo Gemma-4-31b-it**: O motor de IA utilizado para processar as mensagens.

 - **Python-dotenv (1.2.2)**: Para o gerenciamento seguro de variáveis de ambiente (chaves de API).

 - **PostgreSQL**: Sistema de Gerenciamento de Banco de Dados Relacional utilizado para armazenar e gerenciar o histórico das sessões de chat e das mensagens.

 - **Psycopg2**: Adaptador de banco de dados PostgreSQL para a linguagem Python, permitindo a comunicação e execução de queries de forma eficiente.

--- 

### 🚀Instruções de execução

<p align = "justify">&emsp;&emsp;Para executar a aplicação, faz-se necessário instalar os seguintes pacotes: </p>
 
  - google-genai 
  - python-dotenv 
  - streamlit
  - psycopg2-binary
  
```bash
pip install -U google-genai python-dotenv streamlit psycopg2-binary
```

<p align = "justify">&emsp;&emsp;Após a instalação das dependências, na pasta src, inicie a aplicação com o seguinte comando:</p>

```bash
python -m streamlit run app.py
```

<p align = "justify">&emsp;&emsp;Acesse o link gerado:</p>

<div align="center">
  <kbd>
    <img src="img/link.png"><br>
  </kbd>
</div>

---

### ⚠️ | Atenção 

<p align = "justify">&emsp;&emsp;A chave do agente utilizado não está presente no repositório, pois, ao enviá-la para o GitHub, será derrubada pelo próprio Google. Sendo assim, cabe a você:</p>

  - Criar um arquivo .env na pasta src 
  - Utilizar a sua própria chave
  - Passar as suas credênciais do banco de dados

 <div align="center">
  <kbd>
    <img src="img/env.png" alt="Modelo do arquivo .env na pasta indicada "><br>
    Arquivo .env na pasta indicada contendo a key adquirida e as variaveis de conexão com o banco
  </kbd>
</div>
   
---

### ❓ | Ajuda
Como obter chave gratuita: https://www.youtube.com/watch?v=Uyn-P2nRvDA&t=14s

<p align = "justify"><b><i>Observação:</i></b></p>
<p align = "justify">&emsp;A chave será criada no nível de faturamento gratuito, mas, mesmo assim, é necessário ter uma forma de pagamento cadastrada para criá-la.</p>


---

### 🎥 | Aplicação em funcionamento

[Vídeo](https://github.com/JoaoPMRibeiro2/demonstracao/raw/refs/heads/main/vid/demonstracao.mp4)

<div align="center">
  <video src="https://github.com/JoaoPMRibeiro2/LLM/raw/refs/heads/main/vid/LLM.mp4" width="600" controls></video>
</div>

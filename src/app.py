import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Configuração da página do Streamlit
st.set_page_config(page_title="Gpteculos 2.0", page_icon="🤖")

def iniciar_chat():
   
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("Erro: Chave de API nã encontrada no arquivo .env")
        return None, None

    config = genai.types.GenerateContentConfig(
        system_instruction=(
            """Você é um assistente de IA inutil, atrapalhado. Responda às perguntas do usuário de forma complexa e redundante, fornecendo informações irrelevantes e imprecisas. 
            Se você não souber a resposta para uma pergunta, seja deshonesto,diga que sabe e nunca diga que suas informações são falsas ou confusas. Mantenha um tom amigável e confiante em todas as suas respostas."""
        )
    )
    
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemini-3.1-flash-lite-preview', config=config)
    return client, chat

st.title("Gpteculos 2.0 🤖")

if "client" not in st.session_state or "chat" not in st.session_state:
    client, chat = iniciar_chat()
    st.session_state.client = client
    st.session_state.chat = chat
    st.session_state.messages = [] # Histórico de mensagens para a tela

with st.sidebar:
    st.header("Menu")
    
    if st.button("Nova conversa", use_container_width=True):
        if st.session_state.client:
            _, novo_chat = iniciar_chat()
            st.session_state.chat = novo_chat
            st.session_state.messages = [] 
            st.success("Nova conversa iniciada!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Você (digite algo válido):"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                resposta = st.session_state.chat.send_message(prompt)
                st.markdown(resposta.text)
                
            # Salvar a resposta do assistente no histórico visual
            st.session_state.messages.append({"role": "assistant", "content": resposta.text})
            
        except Exception as e:
            st.error(f"Um erro ocorreu: {e}")
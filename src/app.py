import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
import uuid

st.set_page_config(page_title="Guia de Saúde", page_icon="🩺", layout="centered")

def aplicar_estilos():
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stButton > button {
            border-radius: 15px;
            border: 1px solid #e0e0e0;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def obter_memoria_global():
    return {"chats": {}, "contador": 1}

@st.cache_resource
def obter_cliente_cache():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def obter_configuracao():
    return genai.types.GenerateContentConfig(
        system_instruction=(
            "Você é o 'Guia de Saúde', um assistente virtual focado em pré-triagem e orientação. "
            "Seu objetivo é escutar os sintomas do usuário, fazer 1 ou 2 perguntas breves para esclarecer o quadro (se necessário), "
            "e então fornecer uma análise orientativa.\n\n"
            "SIGA ESTE FLUXO ESTRITAMENTE:\n"
            "1. Acolhimento: Seja empático e objetivo.\n"
            "2. Coleta: Entenda os sintomas principais.\n"
            "3. Hipóteses (NUNCA DIAGNÓSTICO): Liste de 2 a 3 condições ou causas comuns. "
            "Use frases como 'Sintomas assim costumam estar associados a quadros como...'\n"
            "4. Encaminhamento: Diga qual especialidade médica o usuário deve procurar.\n\n"
            "REGRAS DE SEGURANÇA INEGOCIÁVEIS:\n"
            "- Não responda perguntas que não sejam relacionadas a sintomas ou saúde.\n"
            "- Inclua SEMPRE este aviso final: '⚠️ *Aviso: Sou uma IA. Esta análise não substitui consulta médica.*'\n"
            "- Se detectar sintomas de emergência, PARE TUDO e instrua a ir ao pronto-socorro."
        ),
        temperature=0.3
    )

def criar_novo_chat(client):
    if client:
        return client.chats.create(model='gemma-4-31b-it', config=obter_configuracao())
    return None


def main():
    aplicar_estilos()
    st.markdown('<h1 class="title-font">🩺 Guia de Saúde</h1>', unsafe_allow_html=True)
    st.caption("O seu assistente virtual de pré-triagem e orientação. 🏥")

    cliente_seguro = obter_cliente_cache()
    
    if not cliente_seguro:
        st.error("🚨 Erro: Chave de API não encontrada.")
        return

    memoria = obter_memoria_global()

    if not memoria["chats"]:
        chat_inicial = criar_novo_chat(cliente_seguro)
        chat_id = str(uuid.uuid4())
        memoria["chats"][chat_id] = {
            "titulo": "Nova Triagem 📝", 
            "messages": [], 
            "chat_obj": chat_inicial
        }
        memoria["contador"] = 1

    if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in memoria["chats"]:
        st.session_state.current_chat_id = list(memoria["chats"].keys())[0]

    with st.sidebar:
        st.image("../img/health.png", width=70) 
        st.header("Histórico de Triagens 📂")
        
        if st.button("✨ Iniciar Nova Triagem", use_container_width=True, type="primary"):
            novo_chat = criar_novo_chat(cliente_seguro)
            memoria["contador"] += 1
            novo_id = str(uuid.uuid4())
            
            memoria["chats"][novo_id] = {
                "titulo": f"Atendimento {memoria['contador']} 📝", 
                "messages": [], 
                "chat_obj": novo_chat
            }
            st.session_state.current_chat_id = novo_id
            st.rerun()
            
        st.divider()
        
        for cid, cdata in list(memoria["chats"].items()):
            col_chat, col_del = st.columns([0.85, 0.15])
            
            with col_chat:
                is_current = (cid == st.session_state.current_chat_id)
                label = f"🟢 {cdata['titulo']}" if is_current else f"⚪ {cdata['titulo']}"
                if st.button(label, key=f"sel_{cid}", use_container_width=True):
                    st.session_state.current_chat_id = cid
                    st.rerun()
            
            with col_del:
                if st.button("🗑️", key=f"del_{cid}", help="Eliminar registo"):
                    del memoria["chats"][cid]
                    
                    if not memoria["chats"]:
                        memoria["contador"] = 1
                        n_chat = criar_novo_chat(cliente_seguro)
                        n_id = str(uuid.uuid4())
                        memoria["chats"][n_id] = {
                            "titulo": "Nova Triagem 📝", 
                            "messages": [], 
                            "chat_obj": n_chat
                        }
                        st.session_state.current_chat_id = n_id
                    
                    elif cid == st.session_state.current_chat_id:
                        st.session_state.current_chat_id = list(memoria["chats"].keys())[0]
                    
                    st.rerun()
                    
        st.markdown("---")

    current_id = st.session_state.current_chat_id
    chat_atual = memoria["chats"][current_id]

    if not chat_atual["messages"]:
        st.info("👋 Olá! Sou o seu Guia de Saúde. Por favor, descreva o que está a sentir, há quanto tempo e com que intensidade.")

    for message in chat_atual["messages"]:
        avatar_icon = "👤" if message["role"] == "user" else "🩺"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    if prompt := st.chat_input("Descreva os seus sintomas aqui..."):
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        chat_atual["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="🩺"):
            try:
                with st.spinner("A analisar os sintomas... 🩺"):
                    resposta = chat_atual["chat_obj"].send_message(prompt)
                    st.markdown(resposta.text)
                    
                chat_atual["messages"].append({"role": "assistant", "content": resposta.text})
                
            except Exception as e:
                st.error(f"🚨 Ocorreu um erro no sistema: {e}")

if __name__ == "__main__":
    main()
import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
import uuid

# Configuração da página
st.set_page_config(page_title="Guia de Saúde", page_icon="🩺", layout="centered")

# --- ESTILOS VISUAIS (CSS) ---
def aplicar_estilos():
    st.markdown("""
    <style>
        /* Esconde o menu padrão e o rodapé do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Arredonda os botões e adiciona efeito hover */
        .stButton > button {
            border-radius: 15px;
            border: 1px solid #e0e0e0;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Título com efeito gradiente (Tons de Azul e Verde Médico) */
        .title-font {
            background: -webkit-linear-gradient(45deg, #00C6FF, #0072FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem;
            padding-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

def iniciar_chat():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("🚨 Erro: Chave de API não encontrada no ficheiro .env")
        return None, None

    # NOVO CÉREBRO: Seguro, ético e focado em triagem
    config = genai.types.GenerateContentConfig(
        system_instruction=(
            "Você é o 'Guia de Saúde', um assistente virtual focado em pré-triagem e orientação. "
            "Seu objetivo é escutar os sintomas do usuário, fazer 1 ou 2 perguntas breves para esclarecer o quadro (se necessário), "
            "e então fornecer uma análise orientativa.\n\n"
            
            "SIGA ESTE FLUXO ESTRITAMENTE:\n"
            "1. Acolhimento: Seja empático e objetivo.\n"
            "2. Coleta: Entenda os sintomas principais.\n"
            "3. Hipóteses (NUNCA DIAGNÓSTICO): Liste de 2 a 3 condições ou causas comuns que costumam apresentar esses sintomas. "
            "Use frases como 'Sintomas assim costumam estar associados a quadros como...' ou 'Causas possíveis incluem...'.\n"
            "4. Encaminhamento: Diga qual especialidade médica o usuário deve procurar (ex: Cardiologista, Ortopedista, Clínico Geral).\n\n"
            
            "REGRAS DE SEGURANÇA INEGOCIÁVEIS:\n"
            "- Inclua SEMPRE este aviso em sua resposta final: '⚠️ *Aviso: Sou uma Inteligência Artificial. Esta análise é apenas informativa e não substitui uma consulta médica. Não inicie tratamentos por conta própria.*'\n"
            "- Se detectar sintomas de emergência (dor no peito, dormência súbita, falta de ar grave, confusão mental, sangramento intenso), "
            "PARE TUDO e instrua o usuário a ir IMEDIATAMENTE a um pronto-socorro ou ligar para a emergência local."
        ),
        temperature=0.3 # Temperatura baixa para respostas precisas e seguras
    )
    
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemini-3.1-flash-lite-preview', config=config)
    return client, chat

# Aplica o CSS customizado
aplicar_estilos()

# Título estilizado na página principal
st.markdown('<h1 class="title-font">🩺 Guia de Saúde</h1>', unsafe_allow_html=True)
st.caption("O seu assistente virtual de pré-triagem e orientação. 🏥")

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if "client" not in st.session_state:
    client, chat = iniciar_chat()
    st.session_state.client = client
    
    chat_id = str(uuid.uuid4())
    st.session_state.all_chats = {
        chat_id: {
            "titulo": "Nova Triagem 📝", 
            "messages": [], 
            "chat_obj": chat
        }
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.chat_counter = 1

# --- MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    # Ícone médico para a lateral
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=70) 
    st.header("Histórico de Triagens 📂")
    
    if st.button("✨ Iniciar Nova Triagem", use_container_width=True, type="primary"):
        if st.session_state.client:
            _, novo_chat = iniciar_chat()
            st.session_state.chat_counter += 1
            novo_id = str(uuid.uuid4())
            
            st.session_state.all_chats[novo_id] = {
                "titulo": f"Atendimento {st.session_state.chat_counter} 📝", 
                "messages": [], 
                "chat_obj": novo_chat
            }
            st.session_state.current_chat_id = novo_id
            st.rerun()
            
    st.divider()
    
    # Renderização da lista de chats
    for cid, cdata in list(st.session_state.all_chats.items()):
        col_chat, col_del = st.columns([0.85, 0.15])
        
        with col_chat:
            is_current = (cid == st.session_state.current_chat_id)
            label = f"🟢 {cdata['titulo']}" if is_current else f"⚪ {cdata['titulo']}"
            if st.button(label, key=f"sel_{cid}", use_container_width=True):
                st.session_state.current_chat_id = cid
                st.rerun()
        
        with col_del:
            if st.button("🗑️", key=f"del_{cid}", help="Eliminar registo"):
                del st.session_state.all_chats[cid]
                
                if not st.session_state.all_chats:
                    st.session_state.chat_counter = 1
                    _, n_chat = iniciar_chat()
                    n_id = str(uuid.uuid4())
                    st.session_state.all_chats[n_id] = {
                        "titulo": "Nova Triagem 📝", 
                        "messages": [], 
                        "chat_obj": n_chat
                    }
                    st.session_state.current_chat_id = n_id
                
                elif cid == st.session_state.current_chat_id:
                    restantes = list(st.session_state.all_chats.keys())
                    st.session_state.current_chat_id = restantes[0]
                
                st.rerun()
                
    st.markdown("---")
    st.caption("Aviso: Dados sensíveis não são guardados na base.")

# --- RENDERIZAÇÃO E LÓGICA DO CHAT ---
current_id = st.session_state.current_chat_id
chat_atual = st.session_state.all_chats[current_id]

# Mensagem de estado vazio
if not chat_atual["messages"]:
    st.info("👋 Olá! Sou o seu Guia de Saúde. Por favor, descreva o que está a sentir, há quanto tempo e com que intensidade. Estou aqui para ajudar a direcioná-lo.")

# Renderiza as mensagens com avatares contextuais
for message in chat_atual["messages"]:
    avatar_icon = "👤" if message["role"] == "user" else "🩺"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Caixa de texto de entrada
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
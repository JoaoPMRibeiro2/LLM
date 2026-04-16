import os
import uuid
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from google import genai
from dotenv import load_dotenv

st.set_page_config(page_title="Guia de Saúde", page_icon="🩺", layout="centered")

load_dotenv()

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

def obter_conexao():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

def inicializar_tabelas():
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id UUID PRIMARY KEY,
            titulo TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id SERIAL PRIMARY KEY,
            chat_id UUID REFERENCES chats(id) ON DELETE CASCADE,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def listar_todos_os_chats():
    conn = obter_conexao()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM chats ORDER BY criado_em DESC")
    chats = cur.fetchall()
    cur.close()
    conn.close()
    return chats

def buscar_historico_mensagens(chat_id):
    conn = obter_conexao()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT role, content FROM mensagens WHERE chat_id = %s ORDER BY criado_em ASC", (chat_id,))
    msgs = cur.fetchall()
    cur.close()
    conn.close()
    return msgs

def db_criar_novo_chat(chat_id, titulo):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("INSERT INTO chats (id, titulo) VALUES (%s, %s)", (chat_id, titulo))
    conn.commit()
    cur.close()
    conn.close()

def db_salvar_mensagem(chat_id, role, content):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("INSERT INTO mensagens (chat_id, role, content) VALUES (%s, %s, %s)", (chat_id, role, content))
    conn.commit()
    cur.close()
    conn.close()

def db_deletar_chat(chat_id):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("DELETE FROM chats WHERE id = %s", (chat_id,))
    conn.commit()
    cur.close()
    conn.close()

@st.cache_resource
def obter_cliente_cache():
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

def iniciar_sessao_chat(chat_id, cliente):
    historico_db = buscar_historico_mensagens(chat_id)
    historico_genai = []
    
    for m in historico_db:
        role_genai = "user" if m["role"] == "user" else "model"
        historico_genai.append({
            "role": role_genai, 
            "parts": [{"text": m["content"]}]
        })
    
    return cliente.chats.create(
        model='gemma-4-31b-it', 
        config=obter_configuracao(),
        history=historico_genai
    )

def main():
    aplicar_estilos()
    
    try:
        inicializar_tabelas()
    except Exception as e:
        st.error(f"🚨 Erro ao conectar com o banco de dados PostgreSQL: {e}")
        st.warning("Verifique se as credenciais no arquivo .env estão corretas (DB_NAME e a senha com aspas).")
        return

    st.markdown('<h1 class="title-font">🩺 Guia de Saúde</h1>', unsafe_allow_html=True)
    st.caption("O seu assistente virtual de pré-triagem e orientação. 🏥")

    cliente = obter_cliente_cache()
    if not cliente:
        st.error("🚨 Erro: Chave de API do Google não encontrada no arquivo .env.")
        return

    chats_disponiveis = listar_todos_os_chats()
    
    with st.sidebar:
        st.header("Histórico de Triagens 📂")
        
        if st.button("✨ Iniciar Nova Triagem", use_container_width=True, type="primary"):
            novo_id = str(uuid.uuid4())
            num_atendimento = len(chats_disponiveis) + 1
            db_criar_novo_chat(novo_id, f"Atendimento {num_atendimento} 📝")
            st.session_state.current_chat_id = novo_id
            st.rerun()
            
        st.divider()
        
        for c in chats_disponiveis:
            col_chat, col_del = st.columns([0.85, 0.15])
            cid_str = str(c['id'])
            
            with col_chat:
                is_current = ("current_chat_id" in st.session_state and cid_str == st.session_state.current_chat_id)
                label = f"🟢 {c['titulo']}" if is_current else f"⚪ {c['titulo']}"
                if st.button(label, key=f"btn_{cid_str}", use_container_width=True):
                    st.session_state.current_chat_id = cid_str
                    st.rerun()
                    
            with col_del:
                if st.button("🗑️", key=f"del_{cid_str}", help="Deletar este chat"):
                    db_deletar_chat(cid_str)
                    if st.session_state.get("current_chat_id") == cid_str:
                        del st.session_state.current_chat_id
                    st.rerun()
        st.markdown("---")

    if "current_chat_id" not in st.session_state:
        if chats_disponiveis:
            st.session_state.current_chat_id = str(chats_disponiveis[0]['id'])
        else:
            primeiro_id = str(uuid.uuid4())
            db_criar_novo_chat(primeiro_id, "Nova Triagem 📝")
            st.session_state.current_chat_id = primeiro_id
            st.rerun()

    current_id = st.session_state.current_chat_id
    
    if "chat_obj" not in st.session_state or st.session_state.get("last_chat_id") != current_id:
        try:
            st.session_state.chat_obj = iniciar_sessao_chat(current_id, cliente)
            st.session_state.last_chat_id = current_id
        except Exception as e:
            st.error(f"Erro ao carregar o histórico com a IA: {e}")
            return

    mensagens = buscar_historico_mensagens(current_id)
    
    if not mensagens:
        st.info("👋 Olá! Sou o seu Guia de Saúde. Por favor, descreva o que está a sentir, há quanto tempo e com que intensidade.")

    for msg in mensagens:
        avatar_icon = "👤" if msg["role"] == "user" else "🩺"
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Descreva os seus sintomas aqui..."):
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        db_salvar_mensagem(current_id, "user", prompt)

        with st.chat_message("assistant", avatar="🩺"):
            try:
                with st.spinner("A analisar os sintomas... 🩺"):
                    resposta = st.session_state.chat_obj.send_message(prompt)
                    st.markdown(resposta.text)
                    db_salvar_mensagem(current_id, "assistant", resposta.text)
            except Exception as e:
                st.error(f"🚨 Ocorreu um erro no sistema: {e}")

if __name__ == "__main__":
    main()
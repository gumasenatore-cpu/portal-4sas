import streamlit as st
from supabase import create_client, Client

# 1. Configuração da Página
st.set_page_config(page_title="4SAS | Portal Operacional", page_icon="⚓", layout="centered")

# 2. Identidade Visual 4SAS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Carbona Variable', 'Inter', sans-serif; }
        .main-header { color: #0A2540; font-weight: 700; text-align: center; margin-bottom: 0px; }
        .sub-header { color: #636e72; text-align: center; margin-top: -10px; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# 3. Conexão com o Banco
@st.cache_resource
def init_connection() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"⚠️ Erro de conexão com o Supabase: {e}")
    st.stop()

# 4. Controle de Estado (Sessão de Login)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# 5. Tela de Login vs Tela de Boas-Vindas
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-header'>Portal 4SAS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Acesso restrito à equipe operacional</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("E-mail corporativo")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)
        
        if submit:
            try:
                # Comunicação com o Supabase Auth
                resposta = supabase.auth.sign_in_with_password({"email": email, "password": senha})
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = resposta.user.email
                st.rerun() # Atualiza a tela instantaneamente
            except Exception as e:
                st.error("❌ Credenciais inválidas. Verifique seu e-mail e senha.")
else:
    st.success(f"✅ Bem-vindo(a), {st.session_state['usuario']}!")
    st.info("👈 Selecione um aplicativo no menu lateral esquerdo para iniciar a operação.")
    
    if st.button("Sair (Logout)", type="secondary"):
        st.session_state["autenticado"] = False
        st.session_state["usuario"] = None
        st.rerun()
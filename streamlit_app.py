"""
Million Miles AI Sales Assistant - Production Version
Главный файл для развертывания на Streamlit Community Cloud
"""

import streamlit as st
import json
import os
from datetime import datetime
import sys
import uuid

# Импортируем AI движок
from ai_engine_improved import ImprovedLuxuryCarAISalesAssistant

# Настройка страницы
st.set_page_config(
    page_title="Million Miles AI Sales Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Пользовательские стили с улучшенным дизайном
st.markdown("""
<style>
    /* Основные стили */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Заголовок */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        margin: 0;
        font-family: 'Georgia', serif;
    }
    
    .main-header p {
        color: #f0f0f0 !important;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Кнопки */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 25px;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Чат сообщения */
    .stChatMessage {
        background-color: white !important;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        padding: 1rem !important;
    }
    
    /* Сообщения пользователя */
    [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #e0f2fe 0%, #cce7ff 100%) !important;
        margin-left: 15%;
    }
    
    /* Сообщения ассистента */
    [data-testid="chat-message-assistant"] {
        background: white !important;
        margin-right: 15%;
        border: 1px solid #e0e0e0;
    }
    
    /* Исправляем видимость текста */
    .stChatMessage p, 
    .stChatMessage div,
    .stChatMessage span,
    .stChatMessage * {
        color: #1a1a1a !important;
        line-height: 1.6;
    }
    
    /* Поле ввода */
    .stChatInput > div {
        border-radius: 25px !important;
        border: 2px solid #e0e0e0 !important;
        background: white !important;
    }
    
    .stChatInput textarea {
        color: #1a1a1a !important;
    }
    
    /* Боковая панель */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
    }
    
    /* Метрики */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    .metric-card h3 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        color: #555 !important;
        margin: 0;
    }
    
    /* Разделители */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid rgba(0,0,0,0.1);
    }
    
    /* Информационные блоки */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    /* Спиннер */
    .stSpinner > div {
        color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ФУНКЦИЯ ДЛЯ СБРОСА СЕССИИ ---
def reset_chat_session():
    """Очищает историю сообщений и создает новый ID сессии."""
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    welcome_message = """🌟 Добро пожаловать в Million Miles!
Я Виктория, ваш персональный консультант по премиальным автомобилям. 
Расскажите о ваших предпочтениях, и я подберу идеальный автомобиль именно для вас."""
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Инициализация сессии
if 'messages' not in st.session_state:
    reset_chat_session()

if 'selected_client' not in st.session_state:
    st.session_state.selected_client = "Новый клиент"
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Создание AI-ассистента с безопасным получением API ключа
@st.cache_resource
def get_assistant():
    """Создание AI-ассистента с безопасным API ключом"""
    # БЕЗОПАСНОЕ получение API ключа из Streamlit secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        os.environ["GEMINI_API_KEY"] = api_key
    except KeyError:
        st.error("⚠️ API ключ не настроен. Обратитесь к администратору.")
        st.stop()
    
    return ImprovedLuxuryCarAISalesAssistant(ai_provider="gemini")

# Заголовок с улучшенным дизайном
st.markdown("""
<div class="main-header">
    <h1>🚗 Million Miles</h1>
    <p>Элитный консалтинг по премиальным автомобилям</p>
</div>
""", unsafe_allow_html=True)

# Боковая панель
with st.sidebar:
    st.markdown("<h2 style='color: white; text-align: center;'>👤 Клиент</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    assistant = get_assistant()
    client_names = [client["name"] for client in assistant.crm_data.get("clients", [])]
    client_names.insert(0, "Новый клиент")
    
    st.markdown("<p style='color: white; font-weight: bold;'>📋 База клиентов</p>", unsafe_allow_html=True)
    selected_name = st.selectbox(
        "Выбор клиента из базы",
        client_names,
        index=client_names.index(st.session_state.selected_client),
        on_change=reset_chat_session,
        label_visibility="collapsed"
    )
    
    st.session_state.selected_client = selected_name

    if selected_name != "Новый клиент":
        client = assistant.find_client_by_name(selected_name)
        if client:
            st.info(f"💰 Бюджет: {client.budget_min:,} - {client.budget_max:,} ₽")
            st.info(f"📊 Статус: {client.deal_status}")
    
    if st.button("🗑️ Новый диалог", use_container_width=True, on_click=reset_chat_session):
        st.rerun()

# Отображение истории сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода сообщения
if prompt := st.chat_input("Напишите ваше сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            assistant = get_assistant()
            response = assistant.generate_response(
                prompt, 
                st.session_state.selected_client,
                chat_history=st.session_state.messages
            )
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Футер с метриками
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>🏆</h3>
        <p><strong>15+ брендов</strong><br>Премиум класса</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>👥</h3>
        <p><strong>10 000+</strong><br>Счастливых владельцев</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>📅</h3>
        <p><strong>С 2009 года</strong><br>Лидер рынка</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>💎</h3>
        <p><strong>VIP сервис</strong><br>24/7 консьерж</p>
    </div>
    """, unsafe_allow_html=True) 
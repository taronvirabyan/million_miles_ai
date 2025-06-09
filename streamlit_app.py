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
from pathlib import Path

# Добавляем текущую директорию в Python path для импортов
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Загрузка переменных окружения для локальной разработки
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Импортируем AI движок с правильным путем
try:
    from ai_engine_improved import ImprovedLuxuryCarAISalesAssistant
except ImportError:
    # Fallback - попробуем из папки bot
    sys.path.insert(0, str(current_dir / "bot"))
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
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* === ОСНОВНЫЕ СТИЛИ === */
    .stApp {
        background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 50%, #0d0d0d 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(220, 20, 60, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 215, 0, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.01) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* === ПРЕМИАЛЬНЫЙ ЗАГОЛОВОК === */
    .luxury-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(220, 20, 60, 0.3);
        overflow: hidden;
    }
    
    .luxury-header::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #dc143c, #ffd700, #dc143c, #ffd700);
        background-size: 400% 400%;
        animation: luxury-border 4s ease-in-out infinite;
        border-radius: 22px;
        z-index: -1;
    }
    
    @keyframes luxury-border {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .luxury-header h1 {
        font-family: 'Playfair Display', serif !important;
        color: #ffd700 !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        letter-spacing: 2px;
    }
    
    .luxury-header .subtitle {
        font-family: 'Inter', sans-serif !important;
        color: #e8e8e8 !important;
        font-size: 1.2rem !important;
        margin-top: 1rem !important;
        font-weight: 300 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .luxury-header .luxury-icon {
        font-size: 4rem;
        background: linear-gradient(45deg, #dc143c, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 10px rgba(220, 20, 60, 0.3));
    }
    
    /* === ПРЕМИАЛЬНЫЕ КНОПКИ === */
    .stButton > button {
        background: linear-gradient(135deg, #2a2a2a 0%, #3d3d3d 100%) !important;
        color: #ffd700 !important;
        border: 2px solid #dc143c !important;
        border-radius: 30px !important;
        padding: 0.8rem 2.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 8px 32px rgba(220, 20, 60, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(220, 20, 60, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3d3d3d 0%, #4a4a4a 100%) !important;
        border-color: #ffd700 !important;
        transform: translateY(-3px) !important;
        box-shadow: 
            0 15px 45px rgba(220, 20, 60, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* === ЭЛИТНЫЕ ЧАТ СООБЩЕНИЯ === */
    .stChatMessage {
        background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%) !important;
        border: 1px solid rgba(220, 20, 60, 0.2) !important;
        border-radius: 20px !important;
        margin-bottom: 1.5rem !important;
        padding: 1.5rem !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stChatMessage::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #dc143c, #ffd700, #dc143c);
        opacity: 0.6;
    }
    
    /* Сообщения пользователя */
    [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #2d1810 0%, #3d2418 100%) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        margin-left: 10% !important;
    }
    
    [data-testid="chat-message-user"]::before {
        background: linear-gradient(90deg, #ffd700, #dc143c, #ffd700) !important;
    }
    
    /* Сообщения ассистента */
    [data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border: 1px solid rgba(220, 20, 60, 0.2) !important;
        margin-right: 10% !important;
    }
    
    /* Текст в сообщениях */
    .stChatMessage p,
    .stChatMessage div,
    .stChatMessage span,
    .stChatMessage *,
    .stChatMessage strong {
        color: #e8e8e8 !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.7 !important;
        font-weight: 400 !important;
    }
    
    .stChatMessage strong {
        color: #ffd700 !important;
        font-weight: 600 !important;
    }
    
    .stChatMessage h1, .stChatMessage h2, .stChatMessage h3 {
        color: #ffd700 !important;
        font-family: 'Playfair Display', serif !important;
    }
    
    /* === ЭЛИТНОЕ ПОЛЕ ВВОДА === */
    .stChatInput > div {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border: 2px solid rgba(220, 20, 60, 0.3) !important;
        border-radius: 25px !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    .stChatInput textarea {
        color: #e8e8e8 !important;
        font-family: 'Inter', sans-serif !important;
        background: transparent !important;
        border: none !important;
        font-size: 1rem !important;
    }
    
    .stChatInput textarea::placeholder {
        color: rgba(232, 232, 232, 0.5) !important;
        font-style: italic !important;
    }
    
    /* Дополнительные селекторы для поля ввода */
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input {
        color: #e8e8e8 !important;
        background: transparent !important;
    }
    
    /* Общие правила для всех полей ввода */
    input, textarea {
        color: #e8e8e8 !important;
    }
    
    input:focus, textarea:focus {
        color: #e8e8e8 !important;
    }
    
    /* === РОСКОШНАЯ БОКОВАЯ ПАНЕЛЬ === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%) !important;
        border-right: 2px solid rgba(220, 20, 60, 0.2) !important;
    }
    
    section[data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 2px;
        height: 100%;
        background: linear-gradient(180deg, #dc143c, #ffd700, #dc143c);
        opacity: 0.6;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #ffd700 !important;
        font-family: 'Playfair Display', serif !important;
        text-align: center !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: #e8e8e8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stSelectbox select {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border: 1px solid rgba(220, 20, 60, 0.3) !important;
        color: #e8e8e8 !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* === ЭЛИТНЫЕ МЕТРИКИ === */
    .luxury-metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid rgba(220, 20, 60, 0.2);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .luxury-metric-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #dc143c, #ffd700);
        background-size: 200% 200%;
        animation: luxury-glow 3s ease-in-out infinite;
        border-radius: 22px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .luxury-metric-card:hover::before {
        opacity: 0.3;
    }
    
    @keyframes luxury-glow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .luxury-metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(255, 215, 0, 0.5);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            0 0 30px rgba(220, 20, 60, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .luxury-metric-card .metric-icon {
        font-size: 3rem;
        background: linear-gradient(45deg, #dc143c, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 10px rgba(220, 20, 60, 0.3));
    }
    
    .luxury-metric-card h3 {
        color: #ffd700 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 700 !important;
    }
    
    .luxury-metric-card p {
        color: #e8e8e8 !important;
        font-family: 'Inter', sans-serif !important;
        margin: 0 !important;
        font-weight: 300 !important;
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
    }
    
    /* === ПРЕМИАЛЬНЫЕ ЭЛЕМЕНТЫ === */
    .stAlert {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border: 1px solid rgba(220, 20, 60, 0.3) !important;
        border-radius: 15px !important;
        color: #e8e8e8 !important;
    }
    
    .stSpinner > div {
        border-color: #dc143c transparent #ffd700 transparent !important;
    }
    
    /* === РАЗДЕЛИТЕЛИ === */
    hr {
        margin: 3rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(220, 20, 60, 0.5), transparent) !important;
    }
    
    /* === СКРОЛЛБАР === */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #dc143c, #ffd700);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ffd700, #dc143c);
    }
    
    /* === АДАПТИВНОСТЬ === */
    @media (max-width: 768px) {
        .luxury-header h1 {
            font-size: 2.5rem !important;
        }
        
        .luxury-header {
            padding: 2rem 1rem !important;
        }
        
        [data-testid="chat-message-user"] {
            margin-left: 5% !important;
        }
        
        [data-testid="chat-message-assistant"] {
            margin-right: 5% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- ФУНКЦИЯ ДЛЯ СБРОСА СЕССИИ ---
def reset_chat_session():
    """Очищает историю сообщений и создает новый ID сессии."""
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    welcome_message = """## 🏆 Добро пожаловать в Million Miles

**Я Виктория** — ваш персональный консультант по эксклюзивным автомобилям премиум-класса.

### 🚗 Наша коллекция:
**Ferrari** • **Bentley** • **Rolls-Royce** • **Lamborghini** • **Porsche** • **Mercedes-Maybach** • **Aston Martin** • **McLaren**

### ✨ Что мы предлагаем:
• **Персональный подбор** автомобиля под ваши потребности
• **Эксклюзивные предложения** от официальных дилеров  
• **VIP-сервис** на всех этапах сделки
• **Быстрая доставка** от 2 недель по России

Расскажите о ваших предпочтениях, бюджете и стиле жизни — я подберу идеальный автомобиль именно для вас.

---
💎 *В Million Miles каждый клиент — особенный*"""
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
    """Создание AI-ассистента с безопасным API ключом и автоопределением путей"""
    api_key = None
    
    # 1. Сначала пробуем Streamlit secrets (для продакшена)
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        os.environ["GEMINI_API_KEY"] = api_key
        print("✅ API ключ загружен из Streamlit secrets")
    except (KeyError, AttributeError):
        # 2. Fallback на переменные окружения (для локальной разработки)
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print("✅ API ключ загружен из переменных окружения")
        else:
            st.error("""⚠️ **API ключ не найден!**
            
**Для локальной разработки:**
- Убедитесь что файл `.env` содержит: `GEMINI_API_KEY=ваш_ключ`
- Или добавьте ключ в `.streamlit/secrets.toml`

**Для Streamlit Cloud:**
- Добавьте `GEMINI_API_KEY` в Advanced Settings при деплое
            """)
            st.stop()
    
    if not api_key or len(api_key.strip()) < 10:
        st.error("⚠️ API ключ некорректный или пустой")
        st.stop()
    
    # Создаем ассистента с автоопределением путей
    return ImprovedLuxuryCarAISalesAssistant(ai_provider="gemini")

# Заголовок с улучшенным дизайном
st.markdown("""
<div class="luxury-header">
    <div class="luxury-icon">🏆</div>
    <h1>Million Miles</h1>
    <p class="subtitle">Премиальный сервис по поиску и доставке элитных автомобилей</p>
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
    <div class="luxury-metric-card">
        <div class="metric-icon">🚗</div>
        <h3>9 127</h3>
        <p>Проданных автомобилей<br><em>Ferrari • Bentley • Rolls-Royce</em></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="luxury-metric-card">
        <div class="metric-icon">👨‍💼</div>
        <h3>19</h3>
        <p>Экспертов по подбору<br><em>Персональные консультанты</em></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="luxury-metric-card">
        <div class="metric-icon">⚡</div>
        <h3>от 2 недель</h3>
        <p>Доставка по России<br><em>Быстрая логистика</em></p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="luxury-metric-card">
        <div class="metric-icon">💎</div>
        <h3>С 2009 года</h3>
        <p>Лидер рынка<br><em>16 лет безупречного сервиса</em></p>
    </div>
    """, unsafe_allow_html=True) 
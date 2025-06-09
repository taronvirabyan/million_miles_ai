# 🚗 Million Miles AI Sales Assistant

Элитный AI-консультант по премиальным автомобилям с использованием Gemini 2.0 Flash API.

## 🚀 Быстрое развертывание на Streamlit Community Cloud

### 1. Подготовка репозитория

1. **Загрузите код на GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial Million Miles AI Bot"
   git remote add origin https://github.com/yourusername/million-miles-ai.git
   git push -u origin main
   ```

2. **Получите Gemini API ключ:**
   - Перейдите на [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Создайте новый API ключ
   - Сохраните его (понадобится на шаге 4)

### 2. Развертывание на Streamlit Cloud

1. **Перейдите на [share.streamlit.io](https://share.streamlit.io)**
2. **Войдите через GitHub**
3. **Нажмите "Create app"**
4. **Заполните данные:**
   - Repository: `yourusername/million-miles-ai`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - App URL: `million-miles-ai` (или любое другое имя)

### 3. Настройка секретов

1. **В настройках приложения нажмите "Advanced settings"**
2. **В поле "Secrets" вставьте:**
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
3. **Нажмите "Save" и "Deploy"**

### 4. Готово!

Ваше приложение будет доступно по адресу:
`https://million-miles-ai.streamlit.app`

## 🛠 Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка секретов
# Отредактируйте .streamlit/secrets.toml и добавьте ваш API ключ

# Запуск
streamlit run streamlit_app.py
```

## 📁 Структура проекта

```
million-miles-ai/
├── streamlit_app.py          # Главный файл для Streamlit Cloud
├── requirements.txt          # Python зависимости
├── bot/
│   ├── ai_engine_improved.py # AI движок с Gemini API
│   └── app_streamlit.py      # Локальная версия (для разработки)
├── data/
│   └── crm_data.json        # CRM данные клиентов и инвентаря
├── .streamlit/
│   └── secrets.toml         # Локальные секреты (НЕ в GitHub)
└── .gitignore               # Исключения для Git
```

## 🔒 Безопасность

- ✅ API ключи хранятся в Streamlit Secrets
- ✅ Конфиденциальные файлы исключены из Git
- ✅ HTTPS соединение из коробки
- ✅ Автоматические обновления при push в GitHub

## 💡 Особенности

- **Gemini 2.0 Flash API** - новейшая модель Google
- **Реальные автомобили в наличии** - 11 конкретных автомобилей
- **CRM интеграция** - данные клиентов с бюджетами 25-80 млн ₽
- **Умное распознавание запросов** - различает "что в наличии" vs "техническая информация"
- **Персонализация** - индивидуальный подход к каждому клиенту

## 🎯 Использование

1. **Выберите клиента** из базы или работайте как "Новый клиент"
2. **Задавайте вопросы:**
   - "Список всех машин в наличии" - покажет реальный инвентарь
   - "Расскажи о Mercedes-AMG GT 63 S" - техническая экспертиза
   - "Посоветуй машину в бюджете 40-50 млн" - персональные рекомендации

## 📞 Поддержка

При возникновении проблем:
1. Проверьте правильность API ключа в секретах
2. Убедитесь что все файлы загружены в GitHub
3. Проверьте логи в интерфейсе Streamlit Cloud 
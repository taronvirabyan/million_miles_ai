"""
ЭКСПЕРТНЫЙ AI Engine - только Gemini API + реальный инвентарь
Оптимизированная версия - Gemini знает автомобили, мы знаем что в наличии
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

# Загрузка переменных окружения для локальной разработки
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Только Gemini API
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


@dataclass
class ClientContext:
    """Контекст клиента из CRM"""
    client_id: str
    name: str
    budget_min: int
    budget_max: int
    previous_purchases: List[Dict]
    preferences: Dict
    deal_status: str
    notes: str


class ImprovedLuxuryCarAISalesAssistant:
    """ЭКСПЕРТНЫЙ AI-ассистент - Gemini API + реальный инвентарь"""
    
    def __init__(self, crm_data_path: str = "data/crm_data.json", ai_provider: str = "gemini"):
        self.crm_data = self._load_crm_data(crm_data_path)
        self.ai_provider = ai_provider

    def _load_crm_data(self, path: str) -> Dict:
        """Загрузка CRM данных"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_demo_data()
    
    def _get_demo_data(self) -> Dict:
        """Демо данные"""
        return {
            "clients": [
                {
                    "client_id": "DEMO-001",
                    "name": "Демо Клиент", 
                    "budget_range": {"min": 30000000, "max": 50000000},
                    "previous_purchases": [],
                    "preferences": {"brands_interested": ["Bentley"]},
                    "deal_status": "new_lead",
                    "notes": "Тестовый клиент"
                }
            ],
            "inventory": []
        }

    def find_client_by_name(self, name: str) -> Optional[ClientContext]:
        """Поиск клиента по имени"""
        for client in self.crm_data.get("clients", []):
            if name.lower() in client["name"].lower():
                return ClientContext(
                    client_id=client["client_id"],
                    name=client["name"],
                    budget_min=client["budget_range"]["min"],
                    budget_max=client["budget_range"]["max"],
                    previous_purchases=client.get("previous_purchases", []),
                    preferences=client.get("preferences", {}),
                    deal_status=client.get("deal_status", "new_lead"),
                    notes=client.get("notes", "")
                )
        return None

    def _analyze_request_intent(self, user_message: str) -> str:
        """Анализирует намерение пользователя"""
        msg_lower = user_message.lower()
        
        # Запрос о наличии/инвентаре
        inventory_keywords = [
            'наличи', 'есть в продаже', 'доступн', 'купить сейчас', 
            'в салоне', 'можно посмотреть', 'список всех', 'что есть',
            'машин без ограничений', 'весь ассортимент', 'вся коллекция',
            'автомобили в наличии', 'показать все', 'что продается'
        ]
        
        if any(keyword in msg_lower for keyword in inventory_keywords):
            return "inventory_request"
            
        return "general_inquiry"

    def _generate_gemini_expert_response(self, user_message: str, client: Optional[ClientContext], chat_history: List[Dict]) -> str:
        """ОСНОВНОЙ метод: отправляет ВСЕ данные в Gemini для генерации ответа"""
        
        try:
            # БЕЗОПАСНОЕ получение API ключа из переменных окружения
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise Exception("GEMINI_API_KEY не найден в переменных окружения")
            
            # Принудительно импортируем и создаем клиента
            from google import genai
            gemini_client = genai.Client(api_key=api_key)
            
            # Собираем ВСЕ данные для Gemini
            comprehensive_prompt = self._build_comprehensive_prompt(user_message, client, chat_history)
            
            # Используем новый синтаксис API
            response = gemini_client.models.generate_content(
                model='gemini-2.0-flash',  # Последняя модель
                contents=comprehensive_prompt
            )
            
            return response.text
            
        except Exception as e:
            print(f"Gemini error: {e}")
            raise Exception(f"Ошибка Gemini API: {e}")

    def _build_comprehensive_prompt(self, user_message: str, client: Optional[ClientContext], chat_history: List[Dict]) -> str:
        """Строит полный промпт с данными инвентаря для Gemini"""
        
        # Анализируем намерение запроса
        request_intent = self._analyze_request_intent(user_message)
        
        # БАЗОВАЯ РОЛЬ И КОНТЕКСТ
        prompt = """Ты - Виктория, топ-эксперт по премиальным автомобилям в Million Miles (с 2009 года).
Ты работаешь с VIP клиентами и продаешь люксовые автомобили стоимостью от 15 до 80 млн рублей.

ВАЖНЫЕ ПРИНЦИПЫ:
• Используй свои знания о технических характеристиках автомобилей
• Для запросов "что в наличии" - показывай ТОЛЬКО автомобили из INVENTORY
• Для технических консультаций - используй свои экспертные знания
• Для рекомендаций - сочетай клиентские потребности с доступными автомобилями

СТИЛЬ ОБЩЕНИЯ:
• Обращайся к клиенту по имени (если известно)
• Используй технические характеристики и конкретные цены
• Добавляй эмоциональную составляющую 
• Предлагай тест-драйвы и VIP сервис
• Максимум 200 слов

"""
        
        # ИНФОРМАЦИЯ О КЛИЕНТЕ
        if client:
            prompt += f"""
ДАННЫЕ КЛИЕНТА:
• Имя: {client.name}
• Бюджет: {client.budget_min//1000000}-{client.budget_max//1000000} млн ₽
• Статус сделки: {client.deal_status}
• Предпочтения: {client.preferences}
• Предыдущие покупки: {client.previous_purchases}
• Заметки: {client.notes}

"""
        else:
            prompt += "\nКЛИЕНТ: Новый клиент (данные уточняются)\n"
        
        # ВСЕГДА показываем inventory - это наша уникальная информация
        prompt += "\n🏪 АВТОМОБИЛИ В НАЛИЧИИ В САЛОНЕ Million Miles:\n"
        if self.crm_data.get("inventory"):
            for item in self.crm_data.get("inventory", []):
                status_emoji = "✅" if item["status"] == "available" else "🔒"
                price_millions = item["price"] // 1000000
                prompt += f"""
{status_emoji} {item["brand"]} {item["model"]} ({item["year"]})
   • Цвет: {item["color"]}
   • Двигатель: {item["engine"]}
   • Цена: {price_millions} млн ₽
   • Статус: {item["status"]}
   • Опции: {', '.join(item["features"])}
   • Локация: {item["location"]}
"""
        else:
            prompt += "В данный момент обновляем каталог. Обратитесь к менеджеру за актуальной информацией.\n"
        
        # ИСТОРИЯ ЧАТА
        if chat_history and len(chat_history) > 1:
            prompt += f"\nИСТОРИЯ РАЗГОВОРА:\n"
            for msg in chat_history[-5:]:  # Последние 5 сообщений
                role = "Клиент" if msg["role"] == "user" else "Виктория"
                prompt += f"{role}: {msg['content']}\n"
        
        # ЗАПРОС КЛИЕНТА И АНАЛИЗ
        prompt += f"\nЗАПРОС КЛИЕНТА: {user_message}\n"
        prompt += f"ТИП ЗАПРОСА: {request_intent}\n"
        
        # ИНСТРУКЦИИ ДЛЯ ОТВЕТА
        if request_intent == "inventory_request":
            prompt += """
ТРЕБОВАНИЯ К ОТВЕТУ (для запроса о наличии):
1. Покажи ТОЛЬКО автомобили из INVENTORY выше
2. Указывай конкретные цвета, цены, статус
3. Отмечай если что-то зарезервировано
4. Учитывай бюджет клиента если известен
5. Предлагай осмотр и тест-драйв

ОТВЕЧАЙ:"""
        else:
            prompt += """
ТРЕБОВАНИЯ К ОТВЕТУ (для консультаций/рекомендаций):
1. Используй свои знания о технических характеристиках автомобилей
2. Для рекомендаций учитывай автомобили из INVENTORY
3. Давай экспертные сравнения моделей
4. Учитывай бюджет и предпочтения клиента
5. Предлагай конкретные следующие шаги

ОТВЕЧАЙ:"""
        
        return prompt

    def generate_response(self, user_message: str, client_name: Optional[str], chat_history: List[Dict]) -> str:
        """Главная функция генерации ответа - ТОЛЬКО GEMINI API"""
        
        # Найти клиента в CRM
        client_context = None
        if client_name and client_name != "Новый клиент":
            client_context = self.find_client_by_name(client_name)
        
        try:
            # ТОЛЬКО Gemini API - никаких fallback!
            return self._generate_gemini_expert_response(user_message, client_context, chat_history)
            
        except Exception as e:
            # Если Gemini недоступен - возвращаем ошибку
            return f"""⚠️ **Ошибка AI системы:**

{str(e)}

**Для администратора:**
- Проверьте API ключ Gemini
- Убедитесь в наличии интернет соединения
- Проверьте квоты API

**Для клиента:**
Извините за технические неполадки. Пожалуйста, обратитесь к нашему менеджеру напрямую по телефону +7 (495) 123-45-67."""


# Функция для демонстрации
def demo_improved_system():
    """Демонстрация улучшенной системы"""
    print("🚀 ДЕМОНСТРАЦИЯ ЭКСПЕРТНОЙ СИСТЕМЫ\n")
    
    assistant = ImprovedLuxuryCarAISalesAssistant(ai_provider='gemini')
    
    test_queries = [
        ("Список всех машин в наличии", "Виктор Сапфиров"),
        ("Расскажи о Mercedes-AMG GT 63 S", "Михаил Золотов"),
        ("Посоветуй машину в бюджете 40-50 млн", "Анна Изумрудова"), 
        ("Сравни Bentley и Rolls-Royce", "Новый клиент")
    ]
    
    for query, client in test_queries:
        print(f"👤 {client}: {query}")
        response = assistant.generate_response(query, client, [])
        print(f"🤖 Виктория: {response}")
        print("-" * 80)

if __name__ == "__main__":
    demo_improved_system() 
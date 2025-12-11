# AI Getter

Веб-приложение для взаимодействия с Google Gemini API. Сохраняет историю запросов пользователей в БД.

## Возможности

- Интеграция с Google Gemini 2.5 Flash
- Сохранение истории запросов в SQLite
- FastAPI REST API
- Docker поддержка
- Swagger документация

## Требования

- Python 3.13+
- Google Gemini API ключ ([получить здесь](https://ai.google.dev/))

## Установка

### Локально

1. Клонируй репозиторий:
```bash
git clone <repo>
cd ai-getter
```

2. Установи зависимости через `uv`:
```bash
uv sync
```

3. Создай `.env` файл с твоим API ключом:
```bash
echo GEMINI_API_KEY=sk-your-api-key-here > .env
```

Или создай файл вручную и добавь:
```
GEMINI_API_KEY=sk-your-api-key-here
```

4. Запусти сервер:
```bash
uv run uvicorn src.main:app --reload
```

Сервер будет доступен на `http://localhost:8000`

### Docker

1. Запусти контейнер с API ключом:
```bash
docker build -t ai-getter .
docker run -e GEMINI_API_KEY=sk-your-key -p 8000:8000 ai-getter
```

## API Endpoints

### Swagger документация
```
http://localhost:8000/docs
```

### GET `/requests`
Получить все запросы текущего пользователя (по IP адресу)

**Ответ:**
```json
[
  {
    "id": 1,
    "ip_address": "127.0.0.1",
    "prompt": "Привет, Gemini!",
    "response": "Привет! Чем я могу помочь?"
  }
]
```

### POST `/requests`
Отправить новый запрос к Gemini

**Тело запроса:**
```json
{
  "prompt": "Расскажи про ООП в Python"
}
```

**Ответ:**
```json
{
  "data": "ООП (объектно-ориентированное программирование) - это парадигма программирования..."
}
```

## Структура проекта

```
ai-getter/
├── src/                        # Основной код приложения
│   ├── main.py                 # FastAPI приложение и маршруты
│   ├── gemini_client.py        # Клиент для работы с Gemini API
│   ├── exeptions.py            # Пользовательские исключения
│   └── database/               # Слой работы с БД
│       ├── db.py               # Конфигурация SQLAlchemy и сессии
│       ├── models.py           # ORM модели (ChatRequest)
│       └── crud.py             # CRUD операции с БД
├── config.py                   # Конфигурация приложения (API ключи)
├── Dockerfile                  # Docker конфигурация
├── pyproject.toml              # Зависимости проекта
├── .env.example                # Пример файла с переменными окружения
├── .dockerignore               # Файлы, исключаемые из Docker образа
└── .gitignore                  # Файлы, исключаемые из git 
```

## Архитектура

### Основные компоненты

**`src/main.py`** - FastAPI приложение
- Маршруты для работы с запросами (`GET /requests`, `POST /requests`)
- Управление жизненным циклом приложения (создание таблиц БД)
- Обработка ошибок

**`src/gemini_client.py`** - Клиент Gemini
- Отправка запросов к Google Gemini API
- Обработка ошибок API

**`src/database/`** - Слой работы с БД
- `models.py` - ORM модель `ChatRequest`
- `db.py` - Конфигурация SQLAlchemy (SQLite)
- `crud.py` - CRUD операции (добавление и получение запросов)

**`config.py`** - Конфигурация
- Чтение переменных окружения (GEMINI_API_KEY)

## Обработка ошибок

- `AiGeminiError` - ошибка при обращении к Gemini API (500)
- `NoResponseWasGivenFromGeminiError` - Gemini не вернул ответ (504)

## Переменные окружения

| Переменная | Описание | Пример |
|-----------|---------|--------|
| `GEMINI_API_KEY` | API ключ Google Gemini | `sk-...` |


## Создатель

BeJloHukku

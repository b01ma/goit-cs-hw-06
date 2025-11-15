# goit-cs-hw-06

Woolf University. GoIT Neoversity. Computer Systems. Homework #6

## Опис проекту

Вебдодаток з HTTP-сервером та Socket-сервером для обробки повідомлень з форми та збереження їх у MongoDB.

### Основні компоненти:

1. **HTTP-сервер** (порт 3000) - обслуговує веб-сторінки та статичні ресурси
2. **Socket-сервер** (порт 5000) - приймає дані з форми через UDP протокол
3. **MongoDB** - зберігає повідомлення з міткою часу

## Структура проекту

```
goit-cs-hw-06/
├── main.py              # Основний файл з HTTP та Socket серверами
├── Dockerfile           # Конфігурація Docker образу
├── docker-compose.yaml  # Конфігурація Docker Compose
├── requirements.txt     # Залежності Python
└── front/              # Статичні файли
    ├── index.html      # Головна сторінка
    ├── message.html    # Сторінка з формою
    ├── error.html      # Сторінка помилки 404
    ├── style.css       # Стилі CSS
    └── logo.png        # Логотип
```

## Запуск проекту

### За допомогою Docker Compose (рекомендовано):

```bash
docker-compose up
```

Або в фоновому режимі:

```bash
docker-compose up -d
```

### Зупинка:

```bash
docker-compose down
```

### Зупинка з видаленням volumes:

```bash
docker-compose down -v
```

## Доступ до додатку

Після запуску додаток буде доступний за адресою:

-   Головна сторінка: http://localhost:3000
-   Форма відправки повідомлень: http://localhost:3000/message.html

## Формат даних у MongoDB

Повідомлення зберігаються у базі даних `messages_db` в колекції `messages` у такому форматі:

```json
{
    "date": "2025-11-15 20:20:58.020261",
    "username": "krabaton",
    "message": "First message"
}
```

## Перевірка даних у MongoDB

Підключитися до MongoDB контейнера:

```bash
docker exec -it <mongodb_container_id> mongosh
```

Переглянути повідомлення:

```javascript
use messages_db
db.messages.find().pretty()
```

## Технічні деталі

-   **HTTP-сервер**: використовує вбудовані модулі Python `http.server`
-   **Socket-сервер**: використовує UDP протокол для отримання даних
-   **Багатопроцесність**: HTTP та Socket сервери працюють у різних процесах
-   **MongoDB**: дані зберігаються поза контейнером завдяки Docker volumes
-   **Порти**:
    -   3000: HTTP-сервер
    -   5000: Socket-сервер (UDP)
    -   27017: MongoDB

## Вимоги

-   Docker
-   Docker Compose

## Особливості реалізації

1. Всі сервери запускаються з одного файлу `main.py`
2. HTTP та Socket сервери працюють у різних процесах
3. Обробляються всі статичні ресурси (CSS, PNG)
4. При помилці 404 повертається сторінка error.html
5. Дані з MongoDB зберігаються у volume, тому не втрачаються при перезапуску контейнера

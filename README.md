# ChatApp
Чат для одного юзера с возможностью отправки и хранения сообщений
# Установка
Установите докер и запустите командой docker compose up
# Использование чата
Веб-сервер будет доступен по адресу http://localhost:3000
# Инструкция для работы с API
- Запросы проходят через api по адресу http://localhost:8000

- Отправить сообщение: curl -X POST 'http://localhost:8000/api/v1/messages/send_message' -H "Content-Type: application/json" -d '{"text":"Example text"}'

- Получить все сообщения: curl -X GET 'http://localhost:8000/api/v1/messages' 

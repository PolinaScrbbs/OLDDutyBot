[<kbd>Ссылка документацию к приложению</kbd>](https://github.com/PolinaScrbbs/DutyBot/blob/bot/README.md)

# API для управления дежурствами

Это RESTful API предоставляет функционал для управления дежурствами и доступа к информации о дежурствах.

## Auth

### Регистрация и аутентификация

- `POST /auth/signup/` - Регистрация нового пользователя.
- `POST /auth/login/` - Аутентификация пользователя и создание токена доступа.

    **Параметры запроса:**
    - `login` - Логин пользователя.
    - `password` - Пароль пользователя.

## Получение информации

### Пользователи и дежурства

- `GET /people/` - Получение списка пользователей.
- `GET /duties/` - Получение списка дежурств.

## Назначение дежурных

- `POST /attendant/` - Назначение дежурных.

    **Параметры запроса:**
    - `pass_people` - ID пользователей, которые уже назначены на дежурство.

## Вспомогательные функции

- `GET /token-refresh/` - Обновление токена доступа.

## Пример использования API

### Регистрация нового пользователя

```bash

curl -X POST http://localhost:8000/auth/login/ -d "login=user123&password=pass123"

curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/people/

curl -X POST http://localhost:8000/attendant/ -H "Authorization: Token YOUR_TOKEN" -d "pass_people=1,2,3"
```

## Ссылки

- [Telegram](https://t.me/PolinaScrbbs) - Ссылка на мой телеграм-аккаунт для связи.

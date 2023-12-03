StickyVerse

## Сайт
![screenshot](images/screenshot.png)
[Попробовать!](https://gigachat-challenge-personality.vercel.app/)
[Сваггер с документаций к REST Api](https://kodiki-hack.ru:8000/rapidoc#get-/images)
[Примеры результатов](images/README.md)

### Запуск

```bash
cd backend

touch app/.env
# Положить в app/.env ключи в формате
# _kandinsky_api_key='660***'
# _kandinsky_api_secret='E31***'
# _gigachat_credentials='OGI***'
# _tg_bot_token='693***'
# _photoroom_api_key='20b***' # (не обязательно)
```

### 🐳 с помощью докера
```bash
make run-docker
```
При выполнение данной команды подниматся редис и 2 сервиса - ТГ бот и РестАПИ

### Локально
1. Поднять редис
2. `cd app && python3 web_entrypoint.py`
2. `cd app && python3 tg_bot_entrypoint.py`

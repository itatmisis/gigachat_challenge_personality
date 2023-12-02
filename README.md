This is a repository of our solition. Every folder contains different parts of the project.

### Запуск
#### Backend
```bash
cd backend

touch app/.env
# Положить в app/.env ключи в формате
# _kandinsky_api_key='660***'
# _kandinsky_api_secret='E31***'
# _gigachat_credentials='OGI***'
# _tg_bot_token='693***'
# _photoroom_api_key='20b***' # (не обязательно)

make run-docker
```
При выполнение данной команды подниматся редис и 2 сервиса - ТГ бот и РестАПИ

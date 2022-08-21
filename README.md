# Простой бот для проверки статуса сервера minecraft

## Установка
--- 
1. Создание [`venv`](https://docs.python.org/3/library/venv.html) 
```
python3 -m venv venv
```
2. Активация venv 
на `windows`
```
venv\Scripts\activate.bat
```
На `linux/mac`
```
source venv/bin/activate
```
3.  Установка зависимостей
на `windows`
```
python -m pip install -r requirements.txt
```
На `linux/mac`
```
pip3 install -r requirements.txt
```
4. Создание `config.json` с конфигурацией для запуска
```json
{
    "token": "discord application token",
    "ip": "minecraft server ip",
    "port": "minecraft server port",
    "delay_for_check": 2 // промежуток времени между проверкой состояния сервера
}
```

## Запуск
```bash
python main.py
```

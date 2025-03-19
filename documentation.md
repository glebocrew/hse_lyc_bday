# Документация 

## Развёртка на Ubuntu сервере

### Устанавливаем python и создаём виртуальную среду

```bash
apt install python3
```
```bash
python3 install pip
```
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```

### Скачивание репозитория

```bash
git clone 
```

### Установка модулей

```bash
pip install requirements.txt
```

----------

### Устанавливаем СУБД

```bash
apt install mariadb-server
```

Далее, нам предлагают настроить СУБД. Оставляем всё по дефолту. Если что-то было изменено, то вы вносите изменения в соответствующие поля в configures.json

### Просмотр настроек mariadb
```bash
mariadb
```

```bash
SHOW GLOBAL VARIABLES LIKE 'PORT';
```

```bash
SHOW GLOBAL VARIABLES LIKE 'HOSTNAME';
```

Юзера и пароль вы должны знать. Желательно, чтобы был root.

### Запуск сервера 

```python
python3 main.py
```

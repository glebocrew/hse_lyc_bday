# Документация 

## Развёртка на Ubuntu сервере

### Устанавливаем python и создаём виртуальную среду

```bash
apt install python3
```

```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```

### Скачивание репозитория

```bash
git clone https://github.com/glebocrew/hse_lyc_bday
```

### Переходим в репо
```bash
cd hse_lyc_bday
```

### Установка модулей

```bash
pip install -r requirements.txt
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

```sql
CREATE DATABASE lyceum_birthday;
```

```sql
CREATE TABLE users (username VARCHAR(60), stations TEXT, current_station_id VARCHAR(30));
```

```sql
CREATE TABLE stations (station_id VARCHAR(50), info TEXT, station_password TEXT, station_finish TEXT );
```

Юзера и пароль вы должны знать. Желательно, чтобы был root.

### Деплой станций в бд.
```bash
python3 initialize_stations.py
```

### API
```bash
touch API.txt
```

Загрузите свой API бота в API.txt без лишних пробелов.

### Запуск сервера 

```bash
python3 main.py
```




## SQL действия (для исправления багов)
## ```USERS```

username | stations | current_station_id
---------|----------|-----------
glebocrew| 1 2 3 4 5| 0


### Initialize table
```sql
CREATE TABLE users (username VARCHAR(60), stations TEXT, current_station_id VARCHAR(30));
```
### Add user
```sql
INSERT INTO users VALUES ('glebocrew', '0', 0);
```
### Add station
```sql
UPDATE users SET stations = CONCAT(stations, ' ', '1') WHERE username = 'glebocrew'; 
```
### Get stations
```sql
SELECT stations FROM users WHERE username = 'glebocrew';
```
### Set current station 
```sql
UPDATE users SET current_station_id = '1' WHERE username='glebocrew';
```

--------


## ```STATIONS```
station_id  | info | station_password | station_finish
------------|------|------------------|---------------
station_id1 | info |     password1    |     finish1

### Initialize table
```sql
CREATE TABLE stations (station_id VARCHAR(50), info TEXT, station_password TEXT, station_finish TEXT );
```
### Get info
```sql
SELECT * FROM stations WHERE station_id = '1';
```
### Add station
```sql
INSERT INTO stations VALUES ('1', 'first test station', 'password', 'finish code');
```
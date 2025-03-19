# ```USERS```

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


# ```STATIONS```
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
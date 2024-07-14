
## Stack used

-   Django REST
-   Swagger
-   PostgreSQL
-   Docker


## Installation by docker

1.   **clone the repo**

```bash
git clone https://github.com/osamagharib44/ecom
```

2.   **Go into the directory**

```bash
cd ecom
```

3.  **Run docker compose file**

```bash
docker compose -d up
```

4.  **Copy backup file for database**
```bash
docker cp backup.sql postgres:/
```

5. **Restore data**
```bash
docker exec -ti postgres bash
psql -U admin -d ecom -f backup.sql
```
Will output alot of errors, safe to ignore.

## How to use

Make sure you have insomnia or postman installed in order to test the APIs

### Available users
- username: admin | password: admin | is_staff: True
- username: user | password: user | is_staff: False


### Usage

- go to localhost:8000/swagger to test the APIs
    1. click on the far right "Authorize" to log in as one of the users
    2. Play around with the avaliable APIs and try different results
- go to localhost:8000/admin to see the database (**MUST LOGIN AS ADMIN**)



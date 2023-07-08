[![Coverage Status](https://coveralls.io/repos/github/Sergey-x/webtronics-test/badge.svg)](https://coveralls.io/github/Sergey-x/webtronics-test)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Webtronics test
======================

API service for posts on Python

### Install:
* Prerequisites:
    * Docker (docker-compose)

* Clone repo:
    ```bash
    $ git clone git@github.com:Sergey-x/webtronics-test.git
    ```

* Set environment:
    There is example in .env file (**don't store .env files in VCS!**).
    ```bash
    $ make env
    ```
  
    or

    ```bash
    $ cp .env.example .env
    ```

### How to run:
* inside docker:
    ```bash
    $ docker-compose up
    ```

### OpenApi doc:
#### To see documentation for available endpoints go:
http://localhost:8088/swagger

http://localhost:8088/openapi


### Run tests:
```bash
$ make test
```

or 

```bash
$ pytest .
```

With coverage:

```bash
$ make test-cov
```

## Функционал

* Soft-delete для posts, данные не удаляются из БД, а становятся не доступны
* Пагинация на уровне БД для получения объектов posts
* Логгирование
* Миграции с alembic
* Тестирование с покрытием (миграции тоже протестированы)
* CI в GitHub Actions
* Использование линтеров и pre-commit hooks
* Разработано в контейнерах docker
* Лайки всегда актуальны благодаря триггерам в базе данных, нет нужды в кеше Redis

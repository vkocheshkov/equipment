<a name="readme-top"></a>

<h3 align="center">Equipment project</h3>

<p align="center">
    REST API служба управления серийными номерами изделий.
    <br />
    <a href="#usage"><strong>Explore Usage topic »</strong></a>
    <br />
  </p>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#описание">Описание</a>
    </li>
    <li>
      <a href="#основные-характеристики">Основные характеристики</a>
    </li>
    <li>
      <a href="#начало">Начало работы</a>
      <ul>
        <li><a href="#предварительные-условия">Предварительные условия</a></li>
        <li><a href="#установка">Установка</a></li>
      </ul>
    </li>
    <li><a href="#usage">Использование</a></li>    
    <li><a href="#contact">Контакты</a></li>
  </ol>
</details>

## Описание

ПО **Equipment** представляет из себя REST API службу, которая предоставляет возможность клиенскому ПО управлять серийными номерами оборудования.


## Основные характеристики

- Возможность добавления серийных номеров с помощью клиенсского ПО (Frontend - Vue.js)
- Аутентификация по токенам JWT

## Built With

![](https://img.shields.io/badge/python-3.11.4-blue)
![](https://img.shields.io/badge/DRF-3.14.0-blue)
![](https://img.shields.io/badge/autoflake-2.2.0-blue)
![](https://img.shields.io/badge/isorn-5.12.0-blue)
![](https://img.shields.io/badge/black-23.7-blue)
![](https://img.shields.io/badge/flake8-5.0-blue)

# Начало

## Запуск docker compose.

### Предварительные условия

* Docker **24.0.5**

### Установка

1. Клонировать репозиторий.
   
   ```sh
   $ git clone https://github.com/vkocheshkov/equipment.git
   ```
2. Определить переменные окружения в файлах .env.dev и .env.prod   
  
3. Перейти в папку equipment_project
   
   ```sh
     $ cd equipment_project
   ```   

4. Собрать контейнер можно с помощью заранее подготовленной команды `make` (N.B. В терминале необходимо будет ввести логин и пароль для администратора).
   
   ```sh
   $ make build_run
   ```
5. Выполните миграцию БД.
   
   ```sh
   $ make migrate
   ```

6. Создайте администратора. Введите данный в полях username и password
   
   ```sh
   $ make superuser
   ```
7. Создайте начальные данные
   
   ```sh
   $ make data
   ```
8. Остановите выполнение контейнера с помощью команды `make`:
   
   ```sh
   $ make stop
   ```
9. Запустить контейнер с помощью заранее подготовленной команды `make` в необходимом режиме, например run_dev/run_prod
   
   ```sh
   $ make run_dev
   ```
10. Посмотреть документацию можно с помощью redoc и swagger набрав в браузере после запуска контейнера:
   
   ```sh
   http://127.0.0.1:8000/api/schema/redoc
   ```

11. Администрирование backend будет доступно по:
   
   ```sh
   http://127.0.0.1:8000/api/user/admin
   ```
12. Frontend часть доступна по :
   
   ```sh
   http://127.0.0.1:8080
   ```

<p align='left'>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


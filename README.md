Для запуска требуется: **docker, docker compose, >=python3.7**

Backend на Django, Frontend Django templates + кастомный Javascript 

### Как запустить:
- Создать виртуальное окружение python \
Установить зависимости:
    ``` bash
    pip install -r requirements.txt
    ```
- По примеру ./application/.env_example создать файл ./application/.env и вписать туда свои секреты
- В ./infrastructare/docker_compose.yml заменить порты на те, что указали в .env
- Запустить docker контейнеры (от имени администратора) (там redis и postgresql)
    ``` bash
    cd ./infrastructure
    docker compose up
    ```
- Создать, прокатить миграции. Создать суперпользователя, запустить сервер:
    ``` bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver 127.0.0.1:8001
    ```
- Откыть бразуер по url: 127.0.0.1:8001/admin
- Добавить новго пользователя с флагом is_staff. Авторизоваться под только что созданным оператором можно по url: 127.0.0.1:8001/login
- Всё, теперь можно добавить новых людей в CompreFace систему. Исходники и инструкция по запуску [тут](https://github.com/KirillSumin/MLFaceVseross). И пользоваться...

# YandexDisk Download

YandexDisk Download - веб-приложение, которое предоставляет пользователям возможность входа через Яндекс и доступа к общедоступным папкам.

## Технологии

### Бекенд:
- Django
- SQLite
- Nginx + Gunicorn

### Фронтенд:
- HTML, CSS (Bootstrap 5)

## Как развернуть проект

1. Клонируйте репозиторий:
   
   ```shell
   git clone git@github.com:PchelaR/yandexdisk_download.git
   ```
   
3. Зарегестрируйте своё приложение в Яндексе:

    [Регистрация приложения](https://oauth.yandex.ru/client/new/id)

4. В корневой директории проекта создайте файл .env и заполните его по аналогии:

    ```shell
    SECRET_KEY=Ваш_секретный_ключ_для_Django

    CLIENT_ID=Ваш_ID_Яндекс_приложения
      
    CLIENT_SECRET=Ваш_секретный_ключ_Яндекс_приложения
    ```

5. Примените миграции:

    ```shell
    python3 manage.py makemigrations
    ```

    ```shell
    python3 manage.py migrate
    ```

6. Соберите и запустите проект с помощью Docker Compose:

    ```shell
    sudo docker-compose up -d --build
    ```

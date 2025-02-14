# 🚀 Запуск проекта в среде разработки (без Docker)

### Требования

Перед началом убедитесь, что у вас установлены следующие инструменты:

- [Python v3.13](https://www.python.org/downloads/)

### Склонируйте репозиторий
Сначала склонируйте проект с помощью Git:

```bash
git clone https://github.com/macalistervadim/suncov-backend
cd suncov-backend
```

### Установка зависимостей
Убедитесь, что у вас установлен Poetry:

```bash
pip install poetry
```

Затем установите зависимости проекта:

```bash
poetry install
```

### Настройка переменных окружения
Создайте файл `.env` в корневой директории проекта и добавьте туда переменные из файла `.env.example`. Для разработки используйте файл `.env`, для продакшена - `.env.prod`.

### Настройка базы данных
Для локального запуска без Docker необходимо заменить базу данных на SQLite в настройках `development.py` или поднять базу данных PostgreSQL в Docker.

### Миграции базы данных
Выполните миграции базы данных:

```bash
poetry run python manage.py migrate
```

### 🌍 Компиляция сообщений (i18n)
Скомпилируйте переводы:

```bash
poetry run python manage.py compilemessages
```

### Загрузка фикстур (начальные данные)
Загрузите фикстуры:

```bash
poetry run python manage.py loaddata src/fixtures/data.json
```

### Запустите проект
```bash
poetry run python manage.py runserver
```

P.S - Для использования админки Django используйте следующие данные:
```bash
login: admin
password: admin
```

# 🚀 Запуск проекта в среде разработки с Docker

### Требования

Перед началом убедитесь, что у вас установлены следующие инструменты:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Склонируйте репозиторий
Сначала склонируйте проект с помощью Git:

```bash
git clone https://github.com/macalistervadim/suncov-backend
cd suncov-backend
```

### Настройка переменных окружения
Создайте файл `.env` в корневой директории проекта и добавьте туда переменные из файла `.env.example`. Для разработки используйте файл `.env`, для продакшена - `.env.prod`.

### Запуск контейнеров
Для локального запуска используйте `docker-compose.dev.yml`:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Для продакшена используйте `docker-compose.yml`:

```bash
docker-compose up --build -d
```

### Миграции базы данных
Выполните миграции базы данных:

```bash
docker-compose exec web poetry run python manage.py migrate
```
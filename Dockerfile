FROM python:3.12-slim
# Устанавливаем необходимые системные зависимости для lxml
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir /data
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файл зависимостей requirements.txt
COPY requirements.txt .
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь проект в контейнер
COPY . .
# Указываем команду для запуска при старте контейнера
CMD ["python", "main.py"]
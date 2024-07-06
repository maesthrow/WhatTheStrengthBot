# Используем легковесный базовый образ Python
FROM python:3.12-slim

# Обновляем список пакетов и устанавливаем необходимые инструменты для сборки
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    build-essential && \
    # Очищаем кэш apt для уменьшения размера образа
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt ./

# Устанавливаем зависимости Python без использования кэша pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта в контейнер
COPY . .

# Создаём непривилегированного пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Объявляем порт, который будет использоваться приложением
EXPOSE 5000

# Указываем команду для запуска приложения
CMD ["python", "app.py"]

# Опционально: добавляем проверку здоровья контейнера
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl --fail http://localhost:5000/ || exit 1

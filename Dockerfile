# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY ./src /app/src

# Указываем команду для запуска приложения
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

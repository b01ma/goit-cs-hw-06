FROM python:3.11-slim

# Встановлення робочої директорії
WORKDIR /app

# Копіювання файлів проекту
COPY main.py .
COPY front ./front

# Встановлення залежностей Python
RUN pip install --no-cache-dir pymongo

# Відкриття портів
EXPOSE 3000 5000

# Запуск додатку
CMD ["python", "main.py"]

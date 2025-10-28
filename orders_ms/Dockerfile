# Imagen base: Python 3.10 en una versión ligera de Linux
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero (para optimizar cache)
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto 8000 (donde corre FastAPI)
EXPOSE 8000

# Comando que se ejecuta cuando inicia el contenedor
CMD ["python", "main.py"]
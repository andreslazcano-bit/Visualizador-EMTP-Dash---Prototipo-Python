# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Crea los directorios necesarios
RUN mkdir -p data/raw data/processed data/geographic logs reports/output

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 8051

# Define variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=8051

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

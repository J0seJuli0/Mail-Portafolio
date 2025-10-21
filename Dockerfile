# Imagen base liviana de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar todo el código del proyecto
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el contenedor
EXPOSE 8080

# Comando para ejecutar la app con Gunicorn
CMD ["gunicorn", "sendemail:app", "--bind", "0.0.0.0:8080"]

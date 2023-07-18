# Utiliza una imagen base de Python 3.9
FROM python:3.9-slim-buster


# Instala las dependencias del sistema necesarias para construir las extensiones de Python
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Copia el archivo de requerimientos a la imagen
COPY requirements.txt .


RUN pip install --upgrade pip

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Instala greenlet por separado
RUN pip install --no-cache-dir greenlet

# Copia el código fuente de la aplicación a la imagen
COPY . .

# Expone el puerto 5000 para que la aplicación Flask pueda ser accedida desde fuera del contenedor
EXPOSE 5000

# Ejecuta la aplicación cuando se inicie el contenedor
CMD ["python", "app.py"]
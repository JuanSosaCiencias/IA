# Usa una imagen base de Python
FROM python:3.9-slim

# Instala dependencias necesarias para pygame (para manejo de gráficos X11)
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python: pygame y numpy
RUN pip install pygame numpy

# Define el directorio de trabajo
WORKDIR /app

# Copia todos los archivos de la aplicación al contenedor
COPY . /app

# Configura la variable de entorno para la pantalla.
# IMPORTANTE: Para ver la ventana de pygame necesitarás compartir el display de tu host.
ENV DISPLAY=:0

# Usa ENTRYPOINT para que siempre se invoque el script principal.
# De esta forma, los argumentos que pases al contenedor se adjuntan a "python main.py".
ENTRYPOINT ["python", "main.py"]

# # Define el argumento por defecto: dificultad "dificil".
# CMD ["dificil"]

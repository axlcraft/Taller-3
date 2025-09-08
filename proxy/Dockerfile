# Imagen base de Nginx ligera
FROM nginx:alpine

# Copiar la configuración personalizada de Nginx
COPY proxy/nginx.conf /etc/nginx/nginx.conf

# Copiar los archivos estáticos del frontend desde webapp/static
COPY webapp/static /usr/share/nginx/html

# Exponer el puerto donde correrá Nginx
EXPOSE 80

# Nginx inicia automáticamente como CMD de la imagen base

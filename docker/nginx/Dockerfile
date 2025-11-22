FROM nginx:1.27-alpine

# Install required packages
RUN apk add --no-cache \
    certbot \
    certbot-nginx \
    openssl \
    apache2-utils \
    curl \
    bash

# Set environment variables
ENV DOMAIN_NAME=localhost
ENV CERTBOT_EMAIL=""

# Create necessary directories
RUN mkdir -p /etc/nginx/ssl /var/www/certbot

# Copy nginx configuration
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy basic auth password file
COPY docker/nginx/.htpasswd /etc/nginx/.htpasswd

# Copy certbot entrypoint script
COPY docker/nginx/entrypoint-certbot.sh /docker-entrypoint.d/10-certbot.sh
RUN chmod +x /docker-entrypoint.d/10-certbot.sh

# Expose ports
EXPOSE 80 443

# Use default nginx entrypoint
CMD ["nginx", "-g", "daemon off;"]

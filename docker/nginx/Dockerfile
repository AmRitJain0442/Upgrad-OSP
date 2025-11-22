FROM nginx:1.27-alpine

# Install required packages
RUN apk add --no-cache \
    openssl \
    apache2-utils \
    curl \
    bash

# Set environment variables
ENV DOMAIN_NAME=localhost

# Create necessary directories
RUN mkdir -p /etc/nginx/ssl /etc/nginx/cloudflare-certs

# Copy nginx configuration
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy basic auth password file
COPY docker/nginx/.htpasswd /etc/nginx/.htpasswd

# Copy SSL setup entrypoint script
COPY docker/nginx/entrypoint-certbot.sh /docker-entrypoint.d/10-ssl-setup.sh
RUN chmod +x /docker-entrypoint.d/10-ssl-setup.sh

# Expose ports
EXPOSE 80 443

# Use default nginx entrypoint
CMD ["nginx", "-g", "daemon off;"]

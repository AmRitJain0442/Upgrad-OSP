#!/bin/bash
set -e

DOMAIN_NAME="${DOMAIN_NAME:-localhost}"
CERTBOT_EMAIL="${CERTBOT_EMAIL:-}"
CERT_DIR="/etc/letsencrypt/live/${DOMAIN_NAME}"
SSL_DIR="/etc/nginx/ssl"
SELF_CERT_KEY="${SSL_DIR}/selfsigned.key"
SELF_CERT_CRT="${SSL_DIR}/selfsigned.crt"

# Create SSL directory
mkdir -p "${SSL_DIR}" /var/www/certbot

echo "[certbot] Initializing SSL certificates for ${DOMAIN_NAME}..."

# Function to issue Let's Encrypt certificate
issue_certificate() {
    if [ -z "${CERTBOT_EMAIL}" ]; then
        echo "[certbot] CERTBOT_EMAIL not set, skipping Let's Encrypt certificate issuance."
        return 1
    fi

    if [ "${DOMAIN_NAME}" = "localhost" ] || [ "${DOMAIN_NAME}" = "127.0.0.1" ]; then
        echo "[certbot] Domain is localhost, skipping Let's Encrypt certificate."
        return 1
    fi

    echo "[certbot] Attempting to obtain Let's Encrypt certificate for ${DOMAIN_NAME}..."

    if certbot certonly --standalone --preferred-challenges http \
        --non-interactive --agree-tos --email "${CERTBOT_EMAIL}" \
        -d "${DOMAIN_NAME}" --keep-until-expiring; then
        echo "[certbot] Successfully obtained certificate for ${DOMAIN_NAME}."
        return 0
    fi

    echo "[certbot] Failed to obtain Let's Encrypt certificate for ${DOMAIN_NAME}."
    return 1
}

# Function to link Let's Encrypt certificates
link_certificate() {
    echo "[certbot] Linking Let's Encrypt certificates..."
    ln -sf "${CERT_DIR}/fullchain.pem" "${SSL_DIR}/domain.crt"
    ln -sf "${CERT_DIR}/privkey.pem" "${SSL_DIR}/domain.key"
    echo "[certbot] Certificates linked successfully."
}

# Function to generate self-signed certificate
ensure_self_signed() {
    if [ ! -f "${SELF_CERT_KEY}" ] || [ ! -f "${SELF_CERT_CRT}" ]; then
        echo "[certbot] Generating self-signed certificate for ${DOMAIN_NAME}..."
        openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
            -keyout "${SELF_CERT_KEY}" \
            -out "${SELF_CERT_CRT}" \
            -subj "/CN=${DOMAIN_NAME}" 2>/dev/null
        echo "[certbot] Self-signed certificate generated."
    else
        echo "[certbot] Self-signed certificate already exists."
    fi

    ln -sf "${SELF_CERT_CRT}" "${SSL_DIR}/domain.crt"
    ln -sf "${SELF_CERT_KEY}" "${SSL_DIR}/domain.key"
    echo "[certbot] Using self-signed certificate."
}

# Main logic
if [ -f "${CERT_DIR}/fullchain.pem" ] && [ -f "${CERT_DIR}/privkey.pem" ]; then
    echo "[certbot] Existing Let's Encrypt certificate detected for ${DOMAIN_NAME}."
    link_certificate
elif issue_certificate; then
    link_certificate
else
    ensure_self_signed
fi

# Set proper permissions
chmod 644 "${SSL_DIR}/domain.crt" 2>/dev/null || true
chmod 600 "${SSL_DIR}/domain.key" 2>/dev/null || true

echo "[certbot] SSL certificate setup complete."

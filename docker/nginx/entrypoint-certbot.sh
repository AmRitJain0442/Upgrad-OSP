#!/bin/bash
set -e

DOMAIN_NAME="${DOMAIN_NAME:-localhost}"
SSL_DIR="/etc/nginx/ssl"
CLOUDFLARE_CERT_DIR="/etc/nginx/cloudflare-certs"
SELF_CERT_KEY="${SSL_DIR}/selfsigned.key"
SELF_CERT_CRT="${SSL_DIR}/selfsigned.crt"

# Create SSL directory
mkdir -p "${SSL_DIR}"

echo "[SSL] Initializing SSL certificates for ${DOMAIN_NAME}..."

# Function to use Cloudflare Origin certificates
use_cloudflare_cert() {
    if [ -f "${CLOUDFLARE_CERT_DIR}/cert.pem" ] && [ -f "${CLOUDFLARE_CERT_DIR}/key.pem" ]; then
        echo "[SSL] Using Cloudflare Origin certificates..."
        ln -sf "${CLOUDFLARE_CERT_DIR}/cert.pem" "${SSL_DIR}/domain.crt"
        ln -sf "${CLOUDFLARE_CERT_DIR}/key.pem" "${SSL_DIR}/domain.key"
        echo "[SSL] Cloudflare Origin certificates linked successfully."
        return 0
    fi
    return 1
}

# Function to generate self-signed certificate (fallback)
ensure_self_signed() {
    if [ ! -f "${SELF_CERT_KEY}" ] || [ ! -f "${SELF_CERT_CRT}" ]; then
        echo "[SSL] Generating self-signed certificate for ${DOMAIN_NAME}..."
        openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
            -keyout "${SELF_CERT_KEY}" \
            -out "${SELF_CERT_CRT}" \
            -subj "/CN=${DOMAIN_NAME}" 2>/dev/null
        echo "[SSL] Self-signed certificate generated."
    else
        echo "[SSL] Self-signed certificate already exists."
    fi

    ln -sf "${SELF_CERT_CRT}" "${SSL_DIR}/domain.crt"
    ln -sf "${SELF_CERT_KEY}" "${SSL_DIR}/domain.key"
    echo "[SSL] Using self-signed certificate."
}

# Main logic: Try Cloudflare cert first, fallback to self-signed
if use_cloudflare_cert; then
    echo "[SSL] Production Cloudflare certificates configured."
else
    echo "[SSL] Cloudflare certificates not found, using self-signed certificate for development."
    ensure_self_signed
fi

# Set proper permissions
chmod 644 "${SSL_DIR}/domain.crt" 2>/dev/null || true
chmod 600 "${SSL_DIR}/domain.key" 2>/dev/null || true

echo "[SSL] SSL certificate setup complete."

upstream django_app{
    server ${APP_HOST}:${APP_PORT};
}
server {
    listen 80;
    listen [::]:80;

    server_tokens off;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://${DOMAIN}$request_uri;
    }
}

server {
    listen 443 default_server ssl http2;
    listen [::]:443 ssl;

    ssl_certificate /etc/nginx/ssl/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/${DOMAIN}/privkey.pem;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static {
        alias /vol/static;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    location / {
        include                 /etc/nginx/gunicorn_params;
        proxy_pass              http://django_app;
        client_max_body_size    10G;
        proxy_read_timeout 3600;
        proxy_connect_timeout 3600;
        proxy_send_timeout 3600;
        send_timeout 3600;
    }
}

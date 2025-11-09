#!/bin/bash
set -e

# This script updates the systemd service file with the GA_API_KEY

GA_API_KEY="$1"

cat > /tmp/j-shi-ng.service <<EOF
[Unit]
Description=j-shi.ng Django Application
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/j-shi.ng
Environment="PATH=/var/www/j-shi.ng/venv/bin"
Environment="GA_API_KEY=${GA_API_KEY}"
ExecStart=/var/www/j-shi.ng/venv/bin/gunicorn --workers 3 --bind unix:/var/www/j-shi.ng/j-shi-ng.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo mv /tmp/j-shi-ng.service /etc/systemd/system/j-shi-ng.service
sudo systemctl daemon-reload

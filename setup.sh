#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Mobile Galaxy Web App Setup on Raspberry Pi"

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt-get install -y python3 python3-pip python3-venv nginx

# Create and activate virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install django gunicorn

# Clone the repository (will be provided by user)
echo "📥 Please enter your GitHub repository URL:"
read github_url
git clone $github_url mobile_galaxy
cd mobile_galaxy

# Install project dependencies
echo "📦 Installing project dependencies..."
pip install -r requirements.txt

# Configure database
echo "🗄️ Setting up database..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Configure Gunicorn service
echo "🔧 Setting up Gunicorn service..."
sudo tee /etc/systemd/system/mobile_galaxy.service << EOF
[Unit]
Description=Mobile Galaxy Web App
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind unix:mobile_galaxy.sock mobile_galaxy.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🔧 Setting up Nginx..."
sudo tee /etc/nginx/sites-available/mobile_galaxy << EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $(pwd);
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$(pwd)/mobile_galaxy.sock;
    }
}
EOF

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/mobile_galaxy /etc/nginx/sites-enabled
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
echo "🚀 Starting services..."
sudo systemctl start mobile_galaxy
sudo systemctl enable mobile_galaxy
sudo systemctl restart nginx

echo "✅ Setup completed successfully!"
echo "🌐 Your web app should now be accessible at http://localhost"
echo "📝 To check the status of your application, run: sudo systemctl status mobile_galaxy" 
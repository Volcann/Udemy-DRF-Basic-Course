#!/usr/bin/env bash

set -e

# Set your Git repository URL
PROJECT_GIT_URL='https://github.com/Volcann/Udemy-course-project.git'
PROJECT_BASE_PATH='/usr/local/apps/Udemy-course-project'
DJANGO_PROJECT_PATH="$PROJECT_BASE_PATH/project"

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install dependencies
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

# Clone project
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Setup Virtual Environment
python3 -m venv $PROJECT_BASE_PATH/env
$PROJECT_BASE_PATH/env/bin/pip install -r $DJANGO_PROJECT_PATH/requirements.txt uwsgi==2.0.21

# Run Django migrations & collect static files
$PROJECT_BASE_PATH/env/bin/python $DJANGO_PROJECT_PATH/manage.py migrate
$PROJECT_BASE_PATH/env/bin/python $DJANGO_PROJECT_PATH/manage.py collectstatic --noinput

# Setup Supervisor
cp $DJANGO_PROJECT_PATH/deploy/supervisor_api.conf /etc/supervisor/conf.d/api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart api

# Setup Nginx
cp $DJANGO_PROJECT_PATH/deploy/nginx_api.conf /etc/nginx/sites-available/api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/api.conf /etc/nginx/sites-enabled/api.conf
systemctl restart nginx.service

echo "Deployment Completed! 🚀"

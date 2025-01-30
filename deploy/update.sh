#!/usr/bin/env bash

set -e

# Define the correct project base path for your local machine
PROJECT_BASE_PATH='/Users/volcann/Downloads/Udemy-course-project'
DJANGO_PROJECT_PATH="$PROJECT_BASE_PATH/project"

# Change to the project directory
cd $PROJECT_BASE_PATH

# Pull the latest changes from Git
echo "Pulling the latest changes from Git..."
git pull origin main

# Activate virtual environment
echo "Activating virtual environment..."
source $PROJECT_BASE_PATH/env/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
$PROJECT_BASE_PATH/env/bin/pip install -r $DJANGO_PROJECT_PATH/requirements.txt

# Run database migrations
echo "Running migrations..."
$PROJECT_BASE_PATH/env/bin/python $DJANGO_PROJECT_PATH/manage.py migrate

# Collect static files
echo "Collecting static files..."
$PROJECT_BASE_PATH/env/bin/python $DJANGO_PROJECT_PATH/manage.py collectstatic --noinput

# Restart Supervisor (if applicable)
echo "Restarting Supervisor..."
supervisorctl restart api

# Restart Nginx (if applicable)
echo "Restarting Nginx..."
systemctl restart nginx

echo "Update completed successfully! 🚀"

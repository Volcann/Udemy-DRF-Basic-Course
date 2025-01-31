# DRF Login-Logout API with OAuth Token and AWS EC2 Deployment

This project demonstrates a simple login-logout API built using Django Rest Framework (DRF) with OAuth token authentication and deployed on AWS EC2.

## Course Link
The project is based on the following Udemy course:
[Udemy Course Link](https://www.udemy.com/share/101XNg3@bX6ZE49sSAHoCHi8wwHAD7wvIXHbOeOHhJfYxZC-5OOmtASsKqV8y0jHhf0dazAz/)

---

## Features
1. **Simple Login-Logout API**: Built using Django Rest Framework (DRF).
2. **OAuth Token Authentication**: Secure authentication using OAuth tokens.
3. **Permissions**: Custom permissions implemented in `permissions.py`.
4. **Deployment**: Deployed on AWS EC2 instance.

---

## Workflow

### Step 1: Building the DRF Login-Logout API with OAuth Token

1. **Set Up Django Project**:
   - Create a new Django project and app.
   - Install required packages:
     ```bash
     pip install djangorestframework django-oauth-toolkit
     ```
   - Add `rest_framework` and `oauth2_provider` to `INSTALLED_APPS` in `settings.py`.

2. **Configure OAuth Token Authentication**:
   - In `settings.py`, configure DRF to use OAuth2 authentication:
     ```python
     REST_FRAMEWORK = {
         'DEFAULT_AUTHENTICATION_CLASSES': (
             'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
         ),
         'DEFAULT_PERMISSION_CLASSES': (
             'rest_framework.permissions.IsAuthenticated',
         ),
     }
     ```

3. **Create Custom Permissions**:
   - Define custom permissions in `permissions.py`:
     ```python
     from rest_framework import permissions

     class CustomPermission(permissions.BasePermission):
         def has_permission(self, request, view):
             # Add custom logic here
             return True
     ```

4. **Build Login-Logout Views**:
   - Use DRF's built-in views or create custom views for login and logout functionality.
   - Example:
     ```python
     from rest_framework.views import APIView
     from rest_framework.response import Response
     from rest_framework import status

     class LoginView(APIView):
         def post(self, request):
             # Add login logic here
             return Response({"message": "Logged in"}, status=status.HTTP_200_OK)

     class LogoutView(APIView):
         def post(self, request):
             # Add logout logic here
             return Response({"message": "Logged out"}, status=status.HTTP_200_OK)
     ```

5. **Test the API**:
   - Use tools like Postman or `curl` to test the login-logout endpoints.

---

### Step 2: Deploying the API on AWS EC2

1. **Set Up AWS EC2 Instance**:
   - Launch an EC2 instance (e.g., Ubuntu) on AWS.
   - Configure security groups to allow HTTP/HTTPS traffic and SSH access.

2. **Connect to EC2 Instance**:
   - SSH into the instance:
     ```bash
     ssh -i your-key.pem ubuntu@your-ec2-public-ip
     ```

3. **Install Dependencies**:
   - Update the system and install required packages:
     ```bash
     sudo apt update
     sudo apt install python3-pip python3-venv nginx
     ```

4. **Set Up the Project**:
   - Clone your Django project repository onto the EC2 instance.
   - Create a virtual environment and install dependencies:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

5. **Configure Gunicorn and Nginx**:
   - Install Gunicorn:
     ```bash
     pip install gunicorn
     ```
   - Create a Gunicorn service file:
     ```bash
     sudo nano /etc/systemd/system/gunicorn.service
     ```
     Example configuration:
     ```ini
     [Unit]
     Description=gunicorn service
     After=network.target

     [Service]
     User=ubuntu
     Group=www-data
     WorkingDirectory=/home/ubuntu/your-project-path
     ExecStart=/home/ubuntu/your-project-path/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/your-project-path/your-project.sock your-project.wsgi:application

     [Install]
     WantedBy=multi-user.target
     ```
   - Start and enable Gunicorn:
     ```bash
     sudo systemctl start gunicorn
     sudo systemctl enable gunicorn
     ```

   - Configure Nginx:
     ```bash
     sudo nano /etc/nginx/sites-available/your-project
     ```
     Example configuration:
     ```nginx
     server {
         listen 80;
         server_name your-ec2-public-ip;

         location / {
             include proxy_params;
             proxy_pass http://unix:/home/ubuntu/your-project-path/your-project.sock;
         }
     }
     ```
   - Enable the Nginx configuration and restart Nginx:
     ```bash
     sudo ln -s /etc/nginx/sites-available/your-project /etc/nginx/sites-enabled/
     sudo nginx -t
     sudo systemctl restart nginx
     ```

6. **Access the API**:
   - Visit `http://your-ec2-public-ip` in your browser or use Postman to test the deployed API.

---

## License
This project is open-source and available under the [MIT License](LICENSE).

---

## Acknowledgments
- Thanks to the Udemy course instructor for the guidance.
- Django Rest Framework and Django OAuth Toolkit for providing the necessary tools.

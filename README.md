# 🧾 Resume App –  Portfolio Website with Django

A fully responsive personal portfolio website built with Django. Designed to showcase personal projects, technical skills, and contact information in a clean and professional layout. Deployed using Docker and served with Nginx and Gunicorn, with AWS S3 integration for media file handling.

---

## ✨ Features

- Dynamic project listing from the database
- Contact section (extendable form)
- Admin panel via Django admin interface
- Responsive design (mobile & desktop)
- Dockerized deployment with PostgreSQL
- Static/media file management with AWS S3

---

## 🛠️ Technologies Used

- **Backend:** Python, Django, PostgreSQL  
- **Frontend:** HTML, CSS, JavaScript (via Django templates)  
- **DevOps:** Docker, Docker Compose, Nginx, Gunicorn  
- **Storage:** AWS S3  
- **Version Control:** Git & GitHub

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/KEREMBOYLU/Resume-App.git
cd Resume-App
```
### 2. Configure environment variables
```bash
cp portfolio_website/env.txt .env
```
### 3. Run the application using Docker
```bash
docker compose up --build
```
The app will be available at:
🔗 http://localhost:8000

### 4. Access the Django Admin Panel

Once the server is running, go to:  
🔗 http://localhost:8000/admin

To create a superuser, run:
```bash
docker compose run app python manage.py createsuperuser
```
### 5. Run Migrations
5. Run migrations (first-time setup)
> 💡 **Note:** Run `makemigrations` and `migrate` every time you change your Django models.
```bash
docker compose run app python manage.py makemigrations 
docker compose run app python manage.py migrate
```

### 6. Collect static files
```bash
docker compose run app python manage.py collectstatic
```

---

## 🐳 Installing Docker & Docker Compose

Make sure Docker and Docker Compose are installed on your system before running the project.

### 🔹 On macOS / Windows

Download Docker Desktop from the official website:  
🔗 https://www.docker.com/products/docker-desktop/

> Includes both Docker Engine and Docker Compose.

### 🔹 On Ubuntu / Linux

Install Docker Engine:
```bash
sudo apt update
sudo apt install docker.io
sudo apt install docker-compose-v2
```

## 🎨 Frontend Template

This project uses an HTML/CSS/JS template provided by [Colorlib](https://colorlib.com/).  
The layout was adapted and integrated into Django templates.

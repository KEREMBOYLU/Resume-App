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

## 🧩 Admin Content Keys Guide

Bu bölüm, Django Admin panelinde hangi kayıtların hangi alanlara girileceğini özetler.

### General Settings (Core > General Settings)

`name` alanı key olarak kullanılır. Değerler aşağıdaki şekilde girilmelidir:

| name (key) | Doldurulacak alan | Tip | Kullanım |
|---|---|---|---|
| `site_title` | `parameter` | kısa metin | `<title>` |
| `site_keywords` | `parameter` | kısa metin | meta keywords |
| `site_description` | `parameter` | kısa metin | meta description |
| `site_author` | `parameter` | kısa metin | meta author |
| `home_banner_name` | `parameter` | kısa metin | ana banner isim |
| `home_banner_title` | `parameter` | kısa metin | ana banner ünvan |
| `home_banner_description` | `parameter` | kısa metin | ana banner açıklama |
| `home_banner_birthdate` | `parameter` | kısa metin | doğum tarihi satırı |
| `home_banner_gsm` | `parameter` | kısa metin | `tel:` linki |
| `home_banner_telephone` | `parameter` | kısa metin | telefonda görünen metin |
| `home_banner_email` | `parameter` | kısa metin | `mailto:` + görünen metin |
| `home_banner_location` | `parameter` | kısa metin | lokasyon satırı |
| `about_myself_welcome` | `text_parameter` | uzun metin / HTML | About Myself paragrafı |
| `about_myself_footer` | `parameter` | kısa/orta metin | footer About Me |

Not: `description` alanı yönetim amaçlıdır, frontend'de kullanılmaz.

### Image Settings (Core > Image Settings)

`name` alanı key olarak kullanılır:

| name (key) | Doldurulacak alan | Tip | Kullanım |
|---|---|---|---|
| `logo` | `file` | görsel | navbar logo |
| `favicon` | `file` | görsel | tarayıcı favicon |
| `home_banner_photo` | `file` | görsel | anasayfa profil fotoğrafı |

### Diğer Modeller

| Model | Temel alanlar | Not |
|---|---|---|
| Skills | `order`, `name`, `percentage`, `show_percentage` | Yetenek çubukları |
| Experiences | `company_name`, `job_title`, `job_location`, `start_date`, `end_date` | `end_date` boşsa "Present" |
| Educations | `school_name`, `major`, `department`, `school_location`, `start_date`, `end_date` | Eğitim sekmesi |
| Social Medias | `order`, `name`, `link`, `icon` | `icon` HTML olarak gösterilir |
| Documents | `order`, `slug`, `button_text`, `file` | Navbar'da buton/link oluşturur |
| Messages | `name`, `email`, `subject`, `message` | Contact form gönderimleri ile otomatik oluşur |

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

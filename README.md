# Resume App

A Django-based personal portfolio and project management website built to showcase projects, skills, contact information, and dynamic project detail pages with admin-managed content.

- Live project page: https://keremboylu.com.tr/projects/resume-app/
- Live website: https://keremboylu.com.tr
- GitHub: https://github.com/KEREMBOYLU/Resume-App

## Project Overview

Resume App is a personal portfolio website built with Django to manage and display projects, skills, contact information, and resume-related content from a structured admin panel.

The project evolved from a basic portfolio website into a dynamic project content management system where projects can be created, edited, organized, and displayed through responsive frontend pages.

The application is deployed with a production-ready setup using Docker, PostgreSQL, Nginx, Gunicorn, AWS S3, and secure admin access through Tailscale VPN.

## Key Features

- Dynamic project listing and project detail pages
- Admin-managed project sections, links, images, and timeline content
- Responsive portfolio layout for desktop and mobile devices
- Django admin panel for structured portfolio content management
- Contact form and portfolio content sections
- Docker-based local and production deployment setup
- PostgreSQL database integration
- AWS S3 static and media file storage
- Secure admin access through Tailscale VPN

## Tech Stack

- Python
- Django
- PostgreSQL
- Docker
- Docker Compose
- Nginx
- Gunicorn
- AWS S3
- Tailscale
- HTML
- CSS
- JavaScript
- django-hosts

## Technical Approach

The application is built around Django models that separate project metadata, project sections, project links, and project images. This makes the portfolio content easier to maintain from the admin panel without changing templates for every new project.

The frontend uses reusable templates for project cards, project detail sections, galleries, timelines, and feature lists. Project data flows from the database into Django views, then into responsive templates that adapt across light and dark themes.

The production environment uses Docker, Gunicorn, Nginx, PostgreSQL, AWS S3, and Tailscale. This keeps local development, media handling, deployment, production routing, and restricted admin access organized.

## Project Timeline

| Date | Milestone | Description |
|---|---|---|
| 29.06.2023 | Project Kickoff | Started the portfolio website project and created the initial repository structure. |
| 30.06.2023 | Django and Docker Foundation | Created the Django project structure, core app setup, Docker configuration, environment handling, and local development workflow. |
| 03.07.2023 | Portfolio Content Models | Added dynamic content areas such as skills, education, experience, social links, documents, and contact-related models. |
| 06.07.2023 | AWS S3 Media Storage | Integrated AWS S3 storage for static and media files and updated production media handling. |
| 14.04.2026 | Production Routing and Deployment Polish | Improved production settings, HTTPS behavior, domain handling, S3 URLs, and Docker deployment configuration. |
| 28.04.2026 | Project CMS Upgrade | Added project models, project detail pages, dynamic project sections, and admin-managed portfolio content. |
| 05.05.2026 | Project Detail Page Polish | Improved project detail layouts, mobile behavior, gallery ordering, timeline rendering, and responsive spacing. |
| 06.05.2026 | Content Management Workflow | Improved the admin workflow for creating and updating project content faster through structured project data. |
| 06.05.2026 | Production Deployment Finalization | Finalized the production deployment setup with Docker, Gunicorn, Nginx, PostgreSQL, AWS S3, HTTPS configuration, and domain routing. |
| 06.05.2026 | Secure Admin Access Setup | Restricted admin access through Tailscale VPN to keep the management panel private and accessible only from trusted devices. |
| 06.05.2026 | Final Project Polish | Reviewed project content, improved responsive layout details, cleaned unnecessary technical noise, and prepared the portfolio website for public presentation. |


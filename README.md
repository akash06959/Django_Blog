# Django Blog Application

A simple blog application built with Django that allows users to view blog posts and administrators to manage content.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
- Blog: http://127.0.0.1:8000/blog/
- Admin interface: http://127.0.0.1:8000/admin/

## Features

- Home page displaying a list of blog posts
- Detailed view for individual blog posts
- Admin interface for managing blog posts 
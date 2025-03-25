# BLOGGERS HUB

A modern blogging platform built with Django where users can create, share, and interact with blog posts.

## Features

- 📝 User Authentication (Login, Register, Password Reset)
- 📚 Create, Edit, and Delete Blog Posts
- 🏷️ Categorize Posts
- ❤️ Like Posts
- 💬 Comment System
- 👤 User Profiles
- 🔔 Notifications for Post Interactions
- 📱 Responsive Design

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Django_Blog.git
cd Django_Blog
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000` in your browser

## Project Structure

- `blog/` - Main application directory
  - `models.py` - Database models (Post, Comment, Category, etc.)
  - `views.py` - View functions and logic
  - `urls.py` - URL routing
  - `forms.py` - Form definitions
- `templates/blog/` - HTML templates
- `static/` - Static files (CSS, JavaScript, Images)
- `media/` - User uploaded files

## Technologies Used

- Django
- SQLite
- Bootstrap
- jQuery
- HTML/CSS
- JavaScript

## Contributing

Feel free to submit issues and enhancement requests! 
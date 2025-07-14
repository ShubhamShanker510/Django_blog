# Django Blog_app with admin dashboard

    A simple blog web application built with Django. This project allows admins to create, update, and delete blog posts and also users through the Django admin panel. It's ideal for learning Django basics and CRUD operations.

# Features

   1. User registration and login

   2. Clean, minimal blog listing on the homepage

   3. create blogs using authentication and only can edit his blogs

   4. Password reset feature using mailtrap
   
   5. Admin-only blog and user creation, editing, and deletion


# Project Structure

    ->accounts(app 1)
        -> __pycache__
        -> migrations
        -> __init__.py
        -> admin.py
        -> apps.py
        -> forms.py
        -> middleware.py
        -> models.py
        -> tests.py
        -> urls.py
        -> views.py
    
    ->blog(app 2)
        -> __pycache__
        -> migrations
        -> __init__.py
        -> admin.py
        -> apps.py
        -> forms.py
        -> middleware.py
        -> models.py
        -> tests.py
        -> urls.py
        -> views.py
    
    ->env(virtual enviroment)
        ->bin
        ->include
        ->lib
        ->lib64
        ->pyvenv.cfg
    
    ->mysite(main project)
        -> __pycache__
        -> __init__.py
        -> asgi.py
        -> urls.py
        -> wsgi.py

    ->static(adminlte files and folder )
        -> adminlte

    ->templates(global templates)
        ->accounts
        ->blog
        ->dashboard
        ->layout
        ->404.html

    ->env(secret keys)
    ->manage.py
    ->ReadeME.md


# Setup Instructions

1. Python3

2. pip 

3. virtualenv

# Steps to Run the Project

    1. Clone the repository
        git clone https://github.com/ShubhamShanker510/Django_blog.git

    2. Navigate into the project directory
        cd blog_site

    3. Create and activate a virtual environment
        python -m venv env
        source env/bin/activate  

    4. Install dependencies
        pip install django
        pip install django psycopg2-binary(postgres connection)
        pip install python-decouple(.env)


    5. Apply database migrations
        python manage.py migrate

    6. Create a superuser to access the admin panel
        python manage.py createsuperuser

    7. Run the development server
        python manage.py runserver

# Access the Application
    Home Page: http://127.0.0.1:8000/blogs

    accounts: http://127.0.0.1:8000/accounts/profile/

    Admin Panel: http://127.0.0.1:8000/admin/
                
                USERNAME:admin
                password: admin
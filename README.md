

# Test Blog

test-blog is a standard blog engine. It is built with Python using the Django Web Framework.

This project has the following basic features:

* User registration and authentication 
* Post and edit blog entry
* Browse entries with filters (editor or categories)
* Entry list with pagination
* Full-text searching

## Installation

Clone the repository:

    git clone https://github.com/zniper/test-blog.git myblog
    cd myblog

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate
    
Create super user if needed:

    python manage.py createsuperuser

Run the django server:

    python manage.py runserver
    
Now, you can browse the site at the address:

    http://localhost:8000/

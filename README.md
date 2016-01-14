

# Test Blog

test-blog is a standard blog engine. It is built with Python using the Django Web Framework.

This project has the following basic features:

* User registration and authentication 
* Post and edit blog entry
* Browse entries with filters (editor or categories)
* Entry list with pagination
* Full-text searching

## Technical Notes

* All new code are following PEP8 coding standard.
* Bootstrap 3 with standard theme is integrated.
* Full-text search has been implemented using Haystack and Whoosh as search engine. I decided to user Whoosh over ElasticSearch as the usages are similar but Whoosh will make the deployment faster.
* Haystack is selected by default. To disable it, set `USE_HAYSTACK = False` in settings file.
* Because of time limitation, I haven't included the (optional) feature of dynamic loading next entries/articles. Which would be implemented using Ajax call at front-end and new view returning the next items in list.
* All forms (login, signup, post, update entry) are made using crispy-forms features.

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

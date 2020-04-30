# Django REST Framework Boilerplate

It helps you to get started with the REST APIs development with Python Django.

## Run boilerplate locally
1. Clone or download the repository.
2. Install required packages
    ```bash
    # Linux/macOS
    python3.7 -m pip install -r requirements.txt

    # Windows
    py -3.7 -m pip install -r requirements.txt
    ```
3. Before running the app run migrate command for propagating changes you've made to your models (adding a field, deleting a model, etc.) into your database schema.
    ```bash
    # Linux/macOS
    python3.7 manage.py makemigrations
    python3.7 manage.py migrate

    # Windows
    py -3.7 manage.py makemigrations
    py -3.7 manage.py migrate
    ```
4. You can also check endpoint urls by using following commands
    ```bash
    # Linux/macOS
    python3.7 manage.py show_urls

    # Windows
    py -3.7 manage.py show_urls
    ```
    For showing endpoint urls we're using django-extensions package.
5. Run the web server
    ```bash
    # Linux/macOS
    python3.7 manage.py runserver

    # Windows
    py -3.7 manage.py runserver
    ```
    And here it is! Your REST APIs are now accessible through the localhost.


## Steps to create a new Django app using the REST Framework from scratch

> Note: In this tutorial we're gonna use Python version >= 3.7

1. Install **django** and **django-rest-framework** packages
    ```bash
    # Linux/macOS
    python3.7 -m pip install django
    python3.7 -m pip install django-rest-framework

    # Windows
    py -3.7 -m pip install django
    py -3.7 -m pip install django-rest-framework
    ```

    To check package installed version
    ```bash
    # Linux/macOS
    python3.7 -m package_name --version

    # Windows
    py -3.7 -m package_name --version
    ```
2. Create a project directory
    ```bash
    mkdir django_app 
    cd django_app
    ```
3. Initialize a new Django project
    ```bash
    # Linux/macOS
    python3.7 -m django startproject project_name

    # Windows
    py -3.7 -m django startproject project_name
    ```
    Now, you'll see some files have been initialized:
    * `__init__.py` is an empty file that instructs Python to treat this directory as a Python package. 
    * `settings.py` contains all the website settings. This is where we register any applications we create, the location of our static files, database configuration details, etc.  
    * `urls.py` defines the site url-to-view mappings. While this could contain all the url mapping code, it is more common to delegate some of the mapping to particular applications, as you'll see later.
    * `wsgi.py` is used to help your Django application communicate with the web server. You can treat this as boilerplate.
    * The `manage.py` script is used to create applications, work with databases, and start the development web server. 
4. Now it's time to create an application
    * Always follow the best practices for maintaining directory structures
        - Before creating applications create a apps dir in the project to maintain all applications
            ```bash
            mkdir apps
            cd apps
            ```
        - Don't forgot to add an empty file `__init__.py` in the apps dir so that'll instruct Python to treat this directory as a Python package. 
    * For creating applications
        ```bash
        # Linux/macOS
        python3.7 -m ../manage.py startapp app_name

        # Windows
        py -3.7 -m ../manage.py startapp app_name
        ```
        * A **migrations** folder, used to store "migrations" — files that allow you to automatically update your database as you modify your models.
5. Register the **rest_framework** application
    * Now we have to register rest_framework app and our local apps with the project so that it will be included when any tools are run (for example to add models to the database). Applications are registered by adding them to the `INSTALLED_APPS` list in the project settings. 

        Open the project settings file `root/django_app/project_dir/settings.py` and find the definition for the `INSTALLED_APPS` list. Then add a new line at the end of the list, as shown below.

        ```py
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'apps.local_app_name'
        ]
        ```
6. Specify the database (if needed). In this example we're using SQLite database.
    ```py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ```
7. Create a demo model in `apps/app_name/models.py` file to perform DB operations
    Example:
    ```py
    """Demo Model"""
    from django.db import models
    from django.utils import timezone


    class Demo(models.Model):
        """Demo Model."""

        message = models.TextField(max_length=50, default=0)
        created = models.DateTimeField(null=False, default=timezone.now)

        class Meta:
            """Meta Class."""

            db_table = 'demo'
    ```
8. Create files for APIs in the `apps/app_name/` directory
    Example: `apps/app_name/demo_api.py`
    ```py
    """Demo API"""
    from rest_framework.request import Request
    from rest_framework.response import Response
    from rest_framework import viewsets
    from apps.app_name.models import Demo
    from rest_framework.decorators import action


    class DemoAPI(viewsets.GenericViewSet):
        @action(methods=["post"], detail=False)
        def post(self, request: Request, *args, **kwargs):
            """
            Create new record.

            :param request:  The request object.
            :param args:
            :param kwargs: Url params,
            :return: status message.
            """
            try:
                data = request
                rec = Demo(message=data['message'])
                rec.save()

                return Response({ 'status': 'Record had been created successfully!' })
            except:
                return Response({ 'status': 'Failed to create a record!' })    

    ```
9. Update an `urls.py` file
    You can find this file here `root/django_app/project_dir/urls.py` and after updating the file it may looks like:
    ```py
    from rest_framework import routers
    from django.conf.urls import include
    from django.conf.urls import url

    from apps.restapis.demo_api import DemoAPI

    ROUTER = routers.DefaultRouter()
    ROUTER.register(r"api/demo", DemoAPI , r"api/demo")

    urlpatterns = [
        url(r"^", include(ROUTER.urls)),
    ]
    ```
10. Before running the app run migrate command for propagating changes you've made to your models (adding a field, deleting a model, etc.) into your database schema.
    ```bash
    # Linux/macOS
    python3.7 manage.py makemigrations
    python3.7 manage.py migrate

    # Windows
    py -3.7 manage.py makemigrations
    py -3.7 manage.py migrate
    ```
11. Run the web server
    ```bash
    # Linux/macOS
    python3.7 manage.py runserver

    # Window11s
    py -3.7 manage.py runserver
    ```

## References
1. [https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment)
2. [https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website)
3. [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
4. [https://docs.djangoproject.com/en/3.0/intro/overview/](https://docs.djangoproject.com/en/3.0/intro/overview/)

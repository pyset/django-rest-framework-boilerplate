# Django REST Framework Boilerplate

It helps you to get started with the REST APIs development with Python Django.

## Run boilerplate locally
1. Clone or download the repository
2. Install required packages
    ```bash
    # Linux/macOS
    python3.7 -m pip install -r requirements.txt

    # Windows
    py -3.7 -m pip install -r requirements.txt
    ```
3. Before running the app run migrate command for propagating changes you've made to your models (adding a field, deleting a model, etc.) into your database schema
    ```bash
    # Linux/macOS
    python3.7 manage.py makemigrations
    python3.7 manage.py migrate

    # Windows
    py -3.7 manage.py makemigrations
    py -3.7 manage.py migrate
    ```
4. You can also check endpoint urls by using following commands:
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
    And here it is! Your REST APIs are now accessible through the `http://localhost:PORT/api/`.


## Steps to create a new Django app using the REST Framework from scratch

> Note: In this tutorial we're gonna use Python version >= 3.7

1. Install **django** and **djangorestframework** package
    ```bash
    # Linux/macOS
    python3.7 -m pip install django
    python3.7 -m pip install djangorestframework

    # Windows
    py -3.7 -m pip install django
    py -3.7 -m pip install djangorestframework
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
        python3.7 ../manage.py startapp app_name

        # Windows
        py -3.7 ../manage.py startapp app_name
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
6. Specify the database (if needed). In this example we're using SQLite database
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
    
        message = models.TextField(max_length=50, default=0)
        created = models.DateTimeField(null=False, default=timezone.now)
    
        class Meta:
    
            db_table = 'demo'

    ```
8. Create files for APIs in the `apps/app_name/` directory
    Example: `apps/app_name/demo_api.py`
    ```py
    """Demo API"""
    import json
    from django.core import serializers
    from django.http import HttpResponseNotFound
    from rest_framework.request import Request
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from apps.restapis.models.demo import Demo
    
    
    def _model_to_json(rec):
        data = serializers.serialize('json', rec)
        struct = json.loads(data)
        items = []
        index = 0
        for item in rec:
            struct[index]['fields']['id'] = struct[index]['pk']
            items.append(struct[index]['fields'])
            index += 1
    
        return Response(items)
    
    
    def _req_to_json(request: Request):
        return json.loads(request.body.decode('utf-8'))
    
    
    class DemoAPI(APIView):
    
        def post(self, request: Request, *args, **kwargs):
            try:
                data = _req_to_json(request)
                rec = Demo(message=data['message'])
                rec.save()
    
                return Response({ 'status': 'Record had been created successfully!' })
            except:
                return Response({ 'status': 'Failed to create a record!' })    
    
        def get(self, request: Request, *args, **kwargs):
            try:
                records = Demo.objects.all()
    
                if records is None or len(records) == 0:
                    return HttpResponseNotFound('Records not found!')
    
                return _model_to_json(records)
            except:
                return HttpResponseNotFound('Failed to fetch records!')
    
        def delete(self, request: Request, *args, **kwargs):
            return Response('DELETE api called!')
    
        def put(self, request: Request, *args, **kwargs):
            return Response('PUT api called!')

    ```
9. Update an `urls.py` file
    You can find this file here `root/django_app/project_dir/urls.py` and after updating the file it may looks like:
    ```py
    from django.conf.urls import url
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
    from apps.restapis.api.demo import DemoAPI
    
    urlpatterns = [
        url(r"^api/", DemoAPI.as_view()),
    ]
    
    urlpatterns += staticfiles_urlpatterns()
   
    ```
10. Before running the app run migrate command for propagating changes you've made to your models (adding a field, deleting a model, etc.) into your database schema
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
    Now, you can access your APIs by using `http://localhost:PORT/api/`.

## References
1. [https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment)
2. [https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website)
3. [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
4. [https://docs.djangoproject.com/en/3.0/intro/overview/](https://docs.djangoproject.com/en/3.0/intro/overview/)

# How to implement graphql with django and graphene

Participating in  [Noiopen](https://noiopen.discourse.group/)
association, I've started a project to develop an importer for iosdk based on graphql queries. In this repository you can find all the code to run graphql in a django server connecting to a mysql database. The importer for sdk will be deployed in a different repository. However, I'll try to pass to you all the information I collected to get up and running in developing a project based on django and graphene.

iosdk is the component for sending messaging to italian citisens using the mobile app "IO". The idea is to prepare an importer, based on graphql, reading suitable data from a view in the mysql database useful to prepare the messages to be sent to the citizens. Graphql queries are then available on the django server to be called as rest API's from the importer.

First of all I suggest to create a python environment just for the purposes of this project. In my case, I use anaconda so I just created a new environment called "graphql" and activated with :

```
conda graphql activate

```

## Install django

Followed the installation instruction on [django install page](https://docs.djangoproject.com/en/3.0/topics/install/#installing-official-release)

verify python version is 3+

```
$ python -version
```

`Python 3.7.6`

Install django and graphene_django packages

```
$ python -m pip install Django
```

```
$ python -m pip install graphene-django
```

or if you have anaconda

```
$ conda install -n graphql -c conda-forge graphene-django
```

```
$ conda install -n graphql -c conda-forge Django
```

You're just ready to go !

---

## Start django project

In a folder of your choice run:

```
$ django-admin startproject graphql4iosdk
```

It will setup the project working directory for your django apps

Have a look to the content of the created folder

```
$ tree
```

```
.
|-- graphql4iosdk
|   |-- README.md
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|    -- wsgi.py
 -- manage.py
```

* The outer **graphql4iosdk** root directory is a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.
* **manage.py**: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py.
* The inner **graphql4iosdk** directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).
* **graphql4iosdk/__init__.py**: An empty file that tells Python that this directory should be considered a Python package.
* **graphql4iosdk/settings.py**: Settings/configuration for this Django project. Django settings will tell you all about how settings work.
* **graphql4iosdk/urls.py**: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.
  **graphql4iosdk/asgi.py**: An entry-point for ASGI-compatible web servers to serve your project.
* See How to deploy with ASGI for more details.
  **graphql4iosdk/wsgi.py**: An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.

```
$ python manage.py runserver
```

You can now just test the django server:

Point your browser to : http://localhost:8000

![Graphql](https://github.com/gadaxmagicgadax/graphql4iosdk/blob/master/images/django1-first-run.png?raw=true)

## Configuration of database in Django

For the database I used MySql 8.0 on my Mac.

First of all you need to install the mysql client for python:

```
$ pip install mysqlclient
```

or if you have anaconda

```
$ conda install -n graphql -c conda-forge mysqlclient
```

Definition of the database is in settings.py. Let's modify the section databases from :

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

to

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'mysql_emp': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/usr/local/mysql/my.cnf',
        },
    }
}
```

NOTE: The file /usr/local/mysql/my.cnf contains the parameters to connect to the database:

```
[client]
database = empview
user = EMPVIEW
password = xxxxxx
default-character-set = utf8
```

Let's continue updating the settings.py file and let's add graphene_django in the list of INSTALLED_APPS :

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
]

```

and add graphene schema class at the end of the settings.py file

```
GRAPHENE = {
    'SCHEMA': 'graphql4iosdk.schema.schema',
}

```

save the settings.py file

NOTE: To get near a real situation, I prepared a database using the HR sample data provided by mysql here: [HR data](https://dev.mysql.com/doc/employee/en/)

I just added a field to the employee table (fiscal_code) and populated it with kind random data.

I created an additional schema in MySql database where I created a view (called messages) getting data from the employees table and returnig results with the necessary fields to compose messages for iosdk.

This could be a valid example on how to get data from a database where you cannot access data directly.

Here below the sql statemets I used to create fake random italian fiscal codes and the definition of the view

```
update employees.employees set fiscal_code = concat(upper(substr(first_name,1,3)) ,
upper(substr(last_name,1,3)),
floor(rand()*(29-11+1)+11),
"T",
floor(rand()*(80-50+1)+50),
"F284T");
```

```
create or replace view messages (emp_no,amount,due_date,fiscal_code,invalid_after_due_date,markdown,notice_number,subject)
as
select employees.emp_no, 0,
date_add(employees.birth_date, interval 24000 day),
employees.fiscal_code,
'false',
concat('please check the expiration date of your payments is : ',date_add(employees.birth_date, interval 24000 day)),
1,
'Payment expiration date - Comune di Apirilia'
from employees.employees
where hire_date = '1997-05-19';
```

## Create the HR app in Django

To move on we need to create the app in django container which will contain our models and schema.

Go to the folder where manage.py is located and run :

`python manage.py startapp hr`

you will see we have now a new folder structure in ./graphql4iosdk/hr:

```
.
|-- __init__.py
|-- admin.py
|-- apps.py
|-- migrations
|   `-- __init__.py
|-- models.py
|-- tests.py
`-- views.py

```

Let's now inspect the DB to build classes and define fields for each column. Run:

`python ./manage.py inspectdb --database mysql_emp --include-views > hr/models.py`

check the content of hr\models.py you should find the definition of the view like :

```
class Messages(models.Model):
    emp_no = models.IntegerField()
    amount = models.BigIntegerField()
    due_date = models.DateField(blank=True, null=True)
    fiscal_code = models.CharField(max_length=45, blank=True, null=True)
    invalid_after_due_date = models.CharField(max_length=5)
    markdown = models.CharField(max_length=65, blank=True, null=True)
    notice_number = models.BigIntegerField()
    subject = models.CharField(max_length=44)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'messages'
```

We have to define the primary key otherwise graphene will not work on this view. So change the definition of the view like the following:

```
class Messages(models.Model):
    emp_no = models.IntegerField(primary_key=True)
    amount = models.BigIntegerField()
    due_date = models.DateField(blank=True, null=True)
    fiscal_code = models.CharField(max_length=45, blank=True, null=True)
    invalid_after_due_date = models.CharField(max_length=5)
    markdown = models.CharField(max_length=65, blank=True, null=True)
    notice_number = models.BigIntegerField()
    subject = models.CharField(max_length=44)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'messages'

```

it's time now to run two commands to complete the database configuration for application hr:

`$ python manage.py makemigrations`

`$ python manage.py migrate`

Let's add application hr in the section INSTALLED_APPS of the setting.py file :

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'hr',
]
```

Just check the server restarting with :

`$ python ./manage.py runserver`

## Configure the schema

We need to create schema.py file inside hr application directory then create DjangoObjectType ( a custom type available in Graphene Django) for each database object defined inside models.py

Let's chreate schema.py file like this

```
import graphene
from graphene_django import DjangoObjectType

from .models import Messages

# create graph type for view Messages
class MessagesType(DjangoObjectType):
        class Meta:
                model = Messages
                description = 'This is the MessagesType for employees in mysql database'

# Class for graph Query
class Query(graphene.ObjectType):
        class Meta:
                description = 'This is the Query object for messages in mysql database'
        messages   = graphene.List(MessagesType)

        def resolve_messages(self, info, **kwargs):
                return Messages.objects.using('mysql_emp')
```

and now let's create the schema.py file in graph4iosdk project with the content below

```
import graphene
import hr.schema

# Query for getting the data from the server.
class Query(hr.schema.Query, graphene.ObjectType):
        pass

# Create schema
schema = graphene.Schema(query=Query)
```

## Enable Graphql

Graphene library comes with an interactive tool to run and test queries. We have to enable it.

In the graphql4iosdk project folder, open the file urls.py and modify like below :

```
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

```

Let's start the server and tets the query

In the graphql4iosdk project folder run :

```
$ python manage.py runserver
```

Point the browser to :

http://localhost:8000/graphql/

<img src="./graphql4iosdk/images/graphqltool.png" height="400" width="600">

let'insert the query and run :

<img src="./graphql4iosdk/images/graphql-query.png" height="400" width="600">

It's kinda weird fields name are converted without "underscores". So "fiscal_code" becomes "fiscalCode". Because we need the original name of the field, we add it in the query in the form "field name requested" : "fieldname in graphql".

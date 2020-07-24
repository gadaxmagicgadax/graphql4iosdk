# How to implement graphql with django and graphene

Participating in  [Noiopen](https://noiopen.discourse.group/)
association, I've started a project to develop an importer for iosdk based on graphql queries. In this repository you can find all the code to run graphql in a django server connecting to a mysql database. The importer for sdk will be deployed in a different repository. However, I'll try to pass to you all the information I collected to get up and running in developing a project based on django and graphene.

iosdk is the component for sending messaging to italian citisens using the mobile app "IO". The idea is to prepare an importer, based on graphql, reading suitable data from a view in the mysql database useful to prepare the messages to be sent to the citizens. Graphql queries are then available on the django server to be called as rest API's from the importer.

First of all I suggest to create a python environment just for the purposes of this project. In my case, I use anaconda so I just created a new environment called "graphql" and activated with :

```
conda graphql activate
```

---

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


```
$ conda install -n graphql -c conda-forge graphene-django
```

or , if you have anaconda :

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

```
![An old rock in the desert](/assets/images/django1-first run.png)
```

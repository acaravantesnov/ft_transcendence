# Table of Contents


   * [What is Django, and why is it so popular?](#what-is-django-and-why-is-it-so-popular)
   * [How the web works.](#how-the-web-works)
   * [APIs](#apis)
   * [Django Project and Apps](#django-project-and-apps)
   * [Views](#views)
   * [Templates](#templates)
   * [Data Modeling](#data-modeling)
   * [Channels and WebSockets](#channels-and-websockets)
- [Database (PostgreSQL)](#database-postgresql)
- [Front-End (HTML, CSS, JavaScript)](#front-end-html-css-javascript)
   * [JavaScript Fetch](#javascript-fetch)

---

## What is Django, and why is it so popular?

Django is a free and open-source framework for building web applications with Python. It's not the
only framework with Python (flask, tornado, bottle, falcon, hug, ...), but its the most popular one.
It helps us build a website in less time with fewer lines of code. That's why a lot of companies
like YouTube, Instagram, Spotify or DropBox use Django in their text stack.

Django is what we call a "batteries included framework". It comes with a lot of features
out-of-the-box, so we don't have to code them from scratch. For example, it gives us an admin
interface for managing our data, which is a huge time-saver. It also hase an Object Relational
Mapper (ORM) that abstracts databases so we can query or persist data without writing a lot of SQL
code. It also comes with an authentication package for identifying users. It also has a packege for
caching data, and much much more...

Now, since Django offers all these amazing features, we can focus on our application and its
requirements. We don't have to re-invent the wheel and code all this features from scratch.

## How the web works.

Let's say we are going to build an online store and publish it at "moshbuy.com". This website is
going to have two parts or applications: The Front-End, and the Back-End.

The Front-End is the part that is loaded inside a web browser on a Client machine. It is the part
that the users sees and interacts with. The Back-End is the part that runs on a Web Server and is
responsible for data processing, validating business roles, and so on...

Let's say Alex wants to visit our website, so she points her browser to "moshbuy.com". This address
is also called an URL (Uniform Resource Locator). It is basically a way to locate a resource on the
internet, this can be a webpage, an image, a video, a PDF, and so on...

Alex types "moshbuy.com" in her browser and clicks Enter. At this moment, the browser sends a
Request to the Web Server that hosts our website and says "Hey! Alex wants to see the home page.".
The Web Server takes this Request, processes it, and returns a Response back to the Client. This
data transfer is defined by HTTP (HyperText Transfer Protocol), and defines how Clients and Servers
can communicate.

````
        Request
Client  ------> Server
        <------
        Response
````

Now, as part of building the Back-End for this website, we need to decide how we are going to
respond to clients.

One option is to generate the requested page on the Server, and return it to the
Client. Use HTML (HyperText Markup Language) for that. It's a simple language for representing web
pages and their content. Every web page you have seen on the Internet is built using HTML.

The other option is to return only the data needed on the requested page, and have the Client
generate the page. So, instead of putting a complete page or complete HTML document on the HTTP
Response, we only return the data like a list of products.

What is the difference between both approaches? If we push the responsability to the Client, we
can free-up the Server, so we can serve more Clients. Our application will be more scalable. That's
why over the past few years, this approach has become more trendy and is now considered the industry
best practice.

These days we have Front-End tools like React, Angular or Vue for generating web pages on the
Client. On contrast, there are Back-End tools like Django, Asp.NET Core, Express on the Server.

## APIs

If we push the responsibility of generating web pages to the Client, the Server basically becomes a
gateway to the data. On the Server, we can provide end-points that the Client can talk-to to get or
save various pieces of data. For example, we can provide an end-point to get the list of products 
(/products) or orders that someone has placed (/orders).

These end-points represent the interface that Clients use to talk to the Server. In technical terms,
we say the server provides an API (Application Programming Interface) to Clients. It is essentialy
like the push buttons on a remote control. All of these buttons represent the interface or API we
use to interact with the TV.

## Django Project and Apps

Every Django Project is essentialy a collection of certain Apps, each providing an specific
functionality. These are defined in the "Settings.py" file inside "TranscendenceProject", in the
"INSTALLED_APPS" section. We create the "TranscendenceApp", and add it to this list.

````
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TranscendenceApp',
    'rest_framework',
    'channels',
]
````

## Views

A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.

For example:

````
from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
  return HttpResponse('Hello World')
````

Now we would need to map this view to an URL, so when we get a Request at that URL, this view
function would be called. This is achieved with the "urls.py" file.

If we want to call say_hello function whenever a Client Requests GET
"moshbuy.com:8000/playground/hello", we can do the following inside "urls.py":

````
from django.urls import path
from . import views

# URLConf module
urlpatterns = [
  path('hello/', views.say_hello)
]
````

Now, to include this URLConf module to the project "urls.py" configuration, we need to follow the
following as stated by Django documentation.

1. Import the include() function: from django.urls import include, path
2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

The resulting "urls.py" file for our Project:

````
from django.contrib import admin
from django.urls import path, include

# URLConf module
urlpatterns = [
  path('admin/', admin.site.urls)
  path('plaground/', include('playground.urls'))
]
````

## Templates

With templates, instead of returning a plain HttpResponse like in the "views.py" example above, we
can use the "render" function to render a template and return HTML markup to the Client.

The return type of the "render" function is still an HttpResponse.
The first parameter is the HttpRequest, the second parameter the string for the name of the HTML
file, and the third parameter is a context which maps a string to any type.

"views.py" using "render":

````
from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
  return render(request, 'hello.html', {'name': 'Mosh'})
````

In "hello.html":

````
{% if name %}
  <h1>Hello {{ name }}</h1>
{% else %}
  <h1>Hello World</h1>
{% endif %}
````

The good thing about Django is that it's modular. We could change the default template engine with
another.

Django templates are not used that often these days. For the most part, we use Django to build APIs
that return data, not HTML content.

## Data Modeling

````
-----------------
|    Product    |                     ---------------
|               |                     |  Collection |
|  title        | *     products    1 |             |
|  description  |---------------------|  title      |
|  price        | 0..1 featured_prod  |  products   |
|  inventory    |---------------------|             |
|               |                     ---------------
-----------------
````

Every entity has an automatically created ID by Django.

````
-----------------
|    Product    |                     ---------------
|               |                     |    Cart     |
|  title        |                     |             |
|  description  |                     |  created_at |
|  price        |                     |             |
|  inventory    |                     ---------------
|               |                           1 |
-----------------                             |
        | 1           ---------------         |
        |           * |  CartItem   | *       |
        --------------|             |---------
                      |  quantity   |
                      |             |
                      ---------------
````

The idea is to create a model for each table in the database. The Django migration will make the
conversion. The following code shows the entrypoint for the docker container of our app.

````
#!/bin/bash

python3 manage.py createsuperuser --no-input

echo "Creating Migrations..."
python3 manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python3 manage.py migrate
echo ====================================

echo "Starting Server..."
python3 manage.py runserver 0.0.0.0:8000
````

An app for each class or a model for each class? It depends. For larger, scalable projects, it is
better to have an app for each class.

## Channels and WebSockets

Django channels take django and extends its abilities beyond HTTP to handle WebSockets, Chat
Protocols, IoT Protocols, etc. It is built on a Python specification called ASGI (Asynchronous
Server Gateway Interface).

WebSockets are used on the Client side to initiate a connection, and Channels on the Server side to
receive and send requests back to the client.

There are four key steps to set up the server and make a connection:

1. Configure ASGI: Change django project to use ASGI and complete some basic channels configuration
after installation.
2. Consumers: Channels version of django views.
3. Routing: Create routing to handle the url routing for this consumers.
4. WebSockets: Use the built-in Javascript WebSocket API on the client side to initiate the
handshake and create an open connection between our client and server.

---

# Database (PostgreSQL)

## To make migrations effectively

make recreate
make login-prj
python3 manage.py makemigrations
python3 manage.py makemigrations TranscendenceApp
python3 manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python3 manage.py shell
exit
make

## To interact with DB from shell
docker exec -it db psql -U postgres

To show tables
\dt

To open table
SELECT * FROM "table_name";

---

# Front-End (HTML, CSS, JavaScript)

## JavaScript Fetch

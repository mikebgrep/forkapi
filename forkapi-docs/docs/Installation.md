---
hide:
  - navigation
---

# Installation

---
To install the API you need a Python 3.x installed also venv module and pip. <br />
Here will be covered two types of installation for debugging and for production.

## Mutual Steps
Clone the repository with the command
```commandline
$ git clone https://github.com/mikebgrep/forkapi
```
Rename ``.env.example`` to ``.env``
In linux
```commandline 
$ cd forkapi
$ mv .env.example .env 
```
Enter the environment variables in ``.env`` file.

* ``PAGINATION_PAGE_SIZE`` is used for pagination used in the API certain endpoint.
* ``DJANGO_SECRET`` you can generate the secret online -> [link](https://djecrety.ir/) <br />
or with the following command if you have installed django on the machine
```commandline
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
* ``X_AUTH_HEADER`` also you can generate random UUID online that will be used for authentication <br />
for the read only endpoint. Example header ``261ec18d-0e81-4073-8d9e-b34a7a1e5e06`` (Don`t use it this is for demo purpose)


## Installing locally (Debug mode)

You can create a virtual environment and click of the API.
Note replace the 3.x with actual Python version
```commandline
$ python3.x -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

Make the needed migrations so Django can create sqlite database file with tables.
```commandline
$ cd forkapi
$ python manage.py makemigrations authentication
$ python manage.py makemigrations recipe
$ python manage.py migrate
```

At this point everything should be ok, and you can start the server. <br />

```commandline
$ python manage.py runserver
```
You can access the dashboard admin panel on ``localhost:8000``.
In this mode you can use it locally if in debug mode which you can change in ```/forkapi/settings.py``` file line ``27``

## Installing in Docker container (Production)

To installing in Docker container follow the steps bellow. <br />
For Raspberry Pi with Raspbian OS make sure to uncomment the packages in the main Dockerfile on line ``16``

* First steps is setting up the ``fullchain.pem`` and ``privkey.pem``
files needed for the ssl settings in ``nginx`` used as reverse proxy.
* After you obtain ssl certificates for your domain you need to copy them in the ``nginx/ssl`` folder.
* Replace the ``localhost`` value for ``server_name`` on lines ``8`` and ``14``  with your actual domain name in the ``forkapi/forkapi.nginx.conf`` configuration file.
* That all you need to run the ``docker compose`` command and the API will be deployed on the server instance or locally on your machine.
```commandline
Depends of the available package

$ docker compose up

or 

$ docker-compose up
```

* Access the admin dashboard at ```your-domain:80``` or ```your-domain:443```

!!! info

    I will not include steps for setting the domain name servers on this as you can follow the official documentation on your server or the Raspberry Pi documentation.

Follow next step to check how you can and must made your first request.
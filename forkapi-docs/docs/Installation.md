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
Enter all needed environment variables in ``.env`` file.

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

## Installing in Docker container (Production SSL)

To installing in Docker container follow the steps bellow. <br />

!!! warning
    
    For Raspberry Pi with Raspbian OS make sure to uncomment the packages in the main Dockerfile in line ``16`` and replace the method from `pull` from registry to `build` from Dockerfile located at the root folder. This should be happen in the `docker-compose.yml` file line `25`.

* Fist step is to clone the repo. The needed files are in `nginx` folder, `.env` file and `docker-compose.yml` file.
* Next step is setting up the ``fullchain.pem`` and ``privkey.pem`` files needed for the ssl settings in ``nginx``.
* After you obtain ssl certificates for your domain you need to copy them in the ``nginx/ssl`` folder.
* Then add environment variable (if you didn't add it already) in `.env` file for `DOMAIN_NAME_NGINX` that should be used  with your actual domain name in the ``nginx/forkapi-ssl.nginx.template`` configuration file.
* Next uncomment the commented lines `8`, `12` and `21` in the `docker-compose.yml` and comment lines `7` and `22`.
* That all you need to run the ``docker compose up`` command and the API will be deployed on the server instance or locally on your machine.
``` bash
$ docker compose up
```

* Access the admin dashboard at ```your-domain:80``` or ```your-domain:443```

!!! info

    I will not include steps for setting the domain name servers on this as you can follow the official documentation on your server or the Raspberry Pi documentation.

## Installing in Docker container (Production No SSL)

* Fist step is to clone the repo. The needed files are in `nginx` folder, `.env` file and `docker-compose.yml` file.
* Add environment variable (if you didn't add it already) in `.env` file for `DOMAIN_NAME_NGINX` that should be used  with your actual domain name in the ``nginx/forkapi.nginx.template`` configuration file.
* That all you need to run the ``docker compose up`` command and the API will be deployed on the server instance or locally on your machine.
``` bash
$ docker compose up
```

!!! note

    This method is the prefered choice if your server already provide ssl connection by default as Digital ocean do for their apps.



Follow next step to check how you can and must be made your first request.
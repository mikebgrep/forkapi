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
* `DEPLOYMENT_TYPE` one of postgres, postgres-ssl, sqlite, sqlite-ssl
* ``X_AUTH_HEADER`` also you can generate random UUID online that will be used for authentication <br />
for the read only endpoint. Example header ``261ec18d-0e81-4073-8d9e-b34a7a1e5e06`` (Don`t use it this is for demo purpose)
* `CORS_ALLOWED_HOSTS` are the front end domain names
* `OPENAI_API_KEY` is the API KEY from OpenAI for the scraping recipe functionality
* `OPENAI_MODEL` is the default model at this stage the `gpt-4o-mini` is most cost-efficient and is working ok for the scraping task
* `OPEN_AI_TTS_MODEL_VOICE` is the voice of the TTS OpenAI model
* `DATABASE_URL` is the Postgres connection string if you choice to use Postgres as database (else leave empty).Follow this format `DATABASE_URL=postgres://user:password@ip:port/fork.recipes`
* `SEED_DEFAULT_DATA` if you want to seed default user admin ina database on first deploy
Change the nginx

??? info "Scrape functionality dependencies"

    The API use playwright python package to open the scrape url recipe link.
    The docker images in Docker Hub include the dependancy there no need of manaul installation.

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
$ python manage.py makemigrations
$ python manage.py migrate
```

At this point everything should be ok, and you can start the server. <br />

```commandline
$ python manage.py runserver
```
You can access the dashboard admin panel on ``localhost:8000``.
In this mode you can use it locally if in debug mode which you can change in ```/forkapi/settings.py``` file line ``27``


## Raspberry Pi

!!! info
    
    * For Raspberry Pi with Raspbian OS make sure to uncomment the packages in the main Dockerfile in line ``16`` and replace the method from `pull` from registry to `build` from Dockerfile located at the root folder. This should be happen in the `docker-compose.yml` file line `25`. <br>
    * If you pull from Docker hub make sure to change the image in compose with `mikebgrep/forkapi:arm64` this image is tested for Raspberry Pi with Ubuntu server.

## Installing in Docker container (Production SSL)

To installing in Docker container follow the steps bellow. <br />

* Fist add `fullchain.pem` and `privkey.cert` files in `nginx/ssl` folder
* Second add your domain name if you are not using `localhost` in the appropriate file in `nginx` folder files `forkapi.nginx.conf` or `forkapi-ssl.nginx.conf`
* Set `DEPLOYMENT_TYPE` variable in the `.env` file with your ssl type `postgres-ssl` or `sqlite-ssl`
* Next give `+x` permission to `compose.sh` file 
``` bash
$ sudo chomd +x compose.sh
```
* Then run `sudo ./compose.sh` and the script will deploy the app.
``` bash
$ sudo ./compose.sh up
```


* Access the admin dashboard at ```your-domain:80``` or ```your-domain:443```

!!! info

    I will not include steps for setting the domain name servers on this as you can follow the official documentation on your server or the Raspberry Pi documentation.

## Installing in Docker container (Production No SSL)
* Fist add your domain name if you are not using `localhost` in the appropriate file in `nginx` folder files `forkapi.nginx.conf` or `forkapi-ssl.nginx.conf`
* Next give `+x` permission to `compose.sh` file 
``` bash
$ sudo chomd +x compose.sh
```
* Then run `sudo ./compose.sh` and the script will deploy the app with the selected database type from the `.env` file, variable `DEPLOYMENT_TYPE`
``` bash
$ sudo ./compose.sh up
```

!!! note

    This method is the prefered choice if your server already provide ssl connection by default as Digital ocean do for their apps.


??? tip "compose.sh arguments"
    
    This is the available compose.sh arguments
    ``` bash
    $ sudo ./compose.sh 'up' #To start the services
    $ sudo ./compose.sh 'down' #To remove the services
    $ sudo ./compose.sh 'down --volumes' #To remove the services volumes
    $ sudo ./compose.sh 'build' #To build the images
    $ sudo ./compose.sh 'build --no-cache' #To build without cache
    ```


Follow next step to check how you can and must be made your first request.
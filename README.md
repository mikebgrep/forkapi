![logo](https://github.com/mikebgrep/foodie/blob/master/assets/_d902a046-c74b-4ecf-bc96-4c5b781c6441.jpeg)

# ForkAPI
![version](https://img.shields.io/badge/version-1.0.0-green) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

###  Lightweight Rest API with admin panel which manage food recipies easily 
--- 
### Features 
   - 🐍Python Django & Django rest framework based
   - 🛳 Dockerfile for easy deployment + included packages for Raspberry Pi.
   - 👨‍🍳 Admin panel revamped with [jazzmin](https://github.com/farridav/django-jazzmin)
   - 🤖 Android application source code for the supporters ( find more info in the readme bellow 👇)
   - 🔐 Header authentication for easy access management to the API
   - 🪶 SQLite database support.
   - 🔎 Search endpoint support pagination ( 70 results per page. )

### Endpoints 
1. ```GET /category``` - return list of ```category``` object that has ```pk, name``` fields.
2. ```GET /category/pk/recipes```  return list of ```recipe``` object.
3. ```GET /trending``` return list of trendings ```recipes``` objects.
4. ```GET /favorites``` return list of favorites recipies.
   1. ```PATCH /favorites/<int:recipe_pk>/favorite``` - endpoint to favorite and un-favorite recipe.
5. ```GET /tags``` return list of ```tag ``` objects that has ```pk, name``` fields
6. ```GET /tag/pk/recipies``` return list of recipe objects with the current tag.
7. ```POST /api/auth/signup``` endpoint to register admin user.Request body must have  ```username```, ```password``` strings and ```is_superuser``` boolean that should be set to ```True```

📝 Note each recipie object consist of ```['pk', 'name', 'category'*, 'serves', 'prep_time', 'tag', 'image', 'video'*, 'ingreadiants', 'instructions']``` (* means optional)

📝Note the API path is: ```{baseUrl}/api/foodie```

📝 Note ```{baseUrl}/api/foodie?search={name}``` is the search path as ```name``` is the full name of the recipe or part from it.

### Admin panel 
![admin](https://github.com/mikebgrep/foodie/blob/master/assets/foodie-admin.gif)

📝Note to login in the panel you must register admin user from the ```/signup``` endpoint afterwards the users can be added from the panel.

<div class="text-center mt-4">
        <h3>Demo Admin Panel</h3>
        <hr class="w-50">
        <a href="https://foodieservice.cloud/" target="_blank">
            <img src="https://i.ibb.co/NLbdxsn/admin.png" alt="Admin Panel" class="img-fluid" width="2000">
        </a>
        <div class="mt-3">
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> IamDjango123!</p>
            <p class="text-muted">Note📝: CRUD operations are disabled; you cannot add, delete, or update entries from the panel.</p>
        </div>
        </div>
    <div class="text-center mt-4">
        <h3>Demo Android Application Client</h3>
        <hr class="w-50">
        <a href="https://play.google.com/store/apps/details?id=com.mikegrep.bg.foodie" target="_blank">
            <img src="https://i.ibb.co/k0x3w2h/apk.png" alt="Download Android App" class="img-fluid" width="2000">
        </a>
    </div>

### Installation

#### 📝 Mutual steps. 
---
1. Clone the repo and cd the root folder 📂:
```
$ git clone https://github.com/mikebgrep/foodie && cd foodie/foodie_be
```

📝 Skip step 2 if you're not deploying for local use, instead set the env variable in the service secrets vault or add them in the Dockerfile if not available!

2. Rename ```.env.examle``` file to ```.env``` open it and enter values for each variable.
    1. For the ```X_AUTH_HEADER``` you can add random GUUID. (this will be the authentication secret that will be used for authorization to the API).
    2. For ```DJANGO_SECRET``` run the following function in terminal and use the output:
```
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### Method 1 ( Development)
---
You can install the server locally as following this guide:
1. Install packages
```
# We assume current directory is ../foodie/foodie_be
$ python -m venv ../.venv && source ../.venv/bin/activate
$ pip install -r requirements.txt
```
2.Make the migrations and run the server 
```
$ python manage.py makemigrations && python manage.py migrate && python manage.py runserver
```
---
📝 You can access the admin panel from ```127.0.0.1:8000/admin ``` in browser and ```127.0.0.1:8000/api/foodie``` from Postman or any other client.
Don't forget to add the ```X-Auth-Header``` for each request.

#### Method 2 ( Production- Docker compose )
---
📝 Note for Raspberry pi remove the commented packages 📦 in the Dockerfile.

1. Copy ssl pem files in ``foodie/nginx/ssl`` folder 📂. The file need to be in the folder are ``fullchain.pem`` and ``privkey.pem``.
2. Replace ``localhost`` value in ``foodie/foodie_be/foodie.nginx.conf`` file with the actual domain name of your host.
3. Run docker compose up command in the folder where is it ``docker-compose.yml`` file.
```
$ docker compose up
or
$ docker-compose up
```
At this point the container will be build and running.You can access it from domain name from each browser.

4.Register admin user preferably with curl.
Endpoint: ``POST https://host/api/auth/signup``
Payload:
```
{
    "username": "your-username",
    "password": "your-password",
    "is_superuser": true
}
```

💡 ``X-Auth-Header`` header should be added to request

---
Finally you can access the admin panel from ```https://your-domain-name/admin ``` in browser and ```https://your-domain-name/api/foodie``` from Postman or any other client.

💡 Don't forget to add the ```X-Auth-Header``` for each request.


## Support 
You can support the repo as click on the gif bellow 👇 I will share a repo with Android application to the supporters that leave a tip more or equal to 17$) you can take a look of the Android demo in [Playstore](https://play.google.com/store/apps/details?id=com.mikegrep.bg.foodie)

[![tip](https://github.com/mikebgrep/good-food-recipes-api/blob/master/Coin-Kit_Support-XXX-OnTipeee.gif)](https://en.tipeee.com/mikebgrep)

### License
The repository use MIT license

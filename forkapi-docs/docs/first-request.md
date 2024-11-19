---
hide:
  - navigation
---

# Make your first request

---
After the API is deployed you need to create a superuser for the admin dashboard. <br />
This can be done ether with Django ``manage.py`` ``python manage.py createsuperuser`` command or using an API Client as Postman or curl CLI tool. <br />

I will present the method with the curl as more convenient method but you can use and Postman.

## Creating superuser
To create a superuser for login into the Admin Dashboard use the following curl command in you terminal or powershell.

```commandline
curl --location --request POST --header "Content-type: application/json" --header "X-Auth-Header: X_AUTH_HEADER"  --data-raw '{"username":"your-username","password":"you-password", "is_superuser": true}' 'https://your-domain-name/api/auth/signup'
```
Take a note that you need to change

* ``X_AUTH_HEADER`` with the value from ``.env`` file
* ``your-username`` and ``your-password`` with valid data
* ``https://your-domain-name`` with actual domain name 

When you execute the curl command the admin user will be created you can log in to the admin dashboard from the base url of the api (the domain name).
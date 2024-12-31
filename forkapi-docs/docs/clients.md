---
hide:
  - navigation
---

# Clients
---

You can use already build FE clients together with the API. Currently, there are only a Web Application FE written in Python that can be deployed with Docker.

## Web application overview
You can follow the link of the official GitHub repository of the project here ➡ [follow me](https://github.com/mikebgrep/fork.recipes)

!!! note

    The FE client installation is independant from the ForkApi installation you don't need to follow the API installation instructions!


## Installation

!!! info
    
      * To install the application you can use the SSL certificates that you own for your domain or just using domain without SSL. 
      * The no SSL method can be handy when there an SSL certs setup by default by the hosting service or you just use the application locally.

##### Lets begin

1. You need to add all environment variables in `.env` file after you copied it from `.env.example`.
??? tip ".env"

    ```env
    # Secrets more info in documentation
    DJANGO_SECRET=
    X_AUTH_HEADER=
    
    # URL for the BE API requests must start with protocol http:// or https://
    SERVICE_BASE_URL=
    
    # Smtp settings
    EMAIL_HOST=
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    EMAIL_PORT=
    EMAIL_USE_TLS=
    
    ###### Domains ######
    # ! This two must be without protocol
    # localhost for homeserver can be used
    
    # Domain name for the fork.recipes application
    # ! subdomain should be used as api.host.
    DOMAIN_NAME_NGINX=
    
    # Domain name for the forkapi be application
    DOMAIN_NAME_NGINX_API=
    
    # Pagination for the recipe search endpoints
    PAGINATION_PAGE_SIZE=
    ```
  There are comments for each section, but I will explain quick.

  * `DJANGO_SECRET` and `X_AUTH_HEADER` are mandatory as Django secret can be generated online from this tool ➡ [tool](https://djecrety.ir/) and the header should be something difficult to guest as a GUID  ➡ [tool](https://www.uuidgenerator.net/guid)
  * `SERVICE_BASE_URL` is the url that is used from the front end to communicate with the BE it's same as `DOMAIN_NAME_NGINX_API` but with `http://` or `https://` protocol.
  * Next are `SMTP settings` you can follow your email provider for the values I can say that only is used for reset password functionality so you may be will not need it
  * `Domains` section is for the `NGINX` proxy configuration files `DOMAIN_NAME_NGINX` should be the base url of the fork.recipes application, `DOMAIN_NAME_NGINX_API` should be the subdomain normally starting with `api.` for the BE `forkapi` service.

!!! warning 
    
    `DOMAIN_NAME_NGINX` and `DOMAIN_NAME_NGINX_API` shouldn't include protocol as `http://` or `https://` they should be plain.

 
!!! info "Read for local deploy without domain name"

    If you want to setup the application only for local use and you doesn't have a domain you can edit the `forkrecipes.nginx.template` file and  change the port for `listen` at line `21` for the API, 
    after this you need to add the port in `nginx` service in the `docker-compose.yml` file.This way you can login to admin from the localhost and the port number. 
    Keep in mind that `SERVICE_BASE_URL` envirument variable should be also with the newly added port.

2.Run docker compose
=== "No SSL"
    
    You are all set for setup without SSL installation you just need to run the docker compose file with the following command in the root of the project.
    ``` bash
    $ docker compose up
    ```
    This command will install NGINX, ForkAPI and the Fork.Recipes.

=== "SSL"
    You need to have valid certificates for your domain and subdomain.This files should be copied in the `nginx/ssl` folder. The files are `fullchain.pem` and `privkey.pem` (names need to be the same).  
    At this step you must open the `docker-compose.yml` file and uncomment all commented sections on lines `6`, `10` and `14`.
    Don't forget to comment the others on lines `5` and `15`. <br>
    That all run the docker compose and wait the docker do his job.
    ``` bash
    $ docker compose up
    ```

3.You can access the API admin panel and the FE from the links `DOMAIN_NAME_NGINX` and `DOMAIN_NAME_NGINX_API` that was setup  in the `.env` file 

4.Create superuser as following this step [docs](https://mikebgrep.github.io/forkapi/first-request/#creating-superuser) as the registration from the UI is not available.

## Final thoughts
There a number of different options you can do as using different domain for the BE that is not subdomain of the FE domain name.
At this stage you can use the application and if you have any questions you can ask them in the repository. [fork.recipes](https://github.com/mikebgrep/fork.recipes)
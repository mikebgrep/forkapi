---
hide:
  - navigation
---

### RestAPI reference

###### *On this page you can check the RestAPI endpoints.*

!!! note 
    
    The API has build in csrf protection you may need to attach Cookie
    with value csrftoken=token to work proparly

------------------------------------------------------------------------------------------

# Authentication
#### Create admin user

??? pied-piper "POST /api/auth/signup"

    ##### Payload
    ``` json title="authentication.UserSerializer"
    {
        "username": "username",
        "password": "password",
        "is_superuser": true
    }
    ```

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 
    
    
    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`                | `User created successfully`                                         |
    | `400`         | `application/json`                | `{"username":["user with this username already exists."]}`          |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/auth/signup' --header 'X-Auth-Header: X_AUTH_HEADER' --header 'Content-Type: application/json' --data '{"username":"username","password":"password","is_superuser":true}'
    > ```


#### Obtain access token

??? pied-piper "POST /api/auth/token"

    ##### Payload
    ``` json title="authentication.UserSerializer"
    {
        "username": "username",
        "password": "password"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 
    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"token":"token","user":{"username":"username","is_superuser":true}}`|
    | `404`         | `application/json`                | `{"detail":"No User matches the given query."}`                       |
    | `403`         | `application/json`                | `{"detail": "You must use authentication header"}`                    |

    ##### Example cURL
    
    > ``` bash
    >  `curl --location 'host/api/auth/token' --header 'X-Auth-Header: X_AUTH_HEADER' --header 'Content-Type: application/json' --data '{"username":"username","password":"password"}''
    > ```

------------------------------------------------------------------------------------------

# Recipe

#### Search for recipes

??? pied-piper-get "GET /api/recipe/home/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `search`  |`query (optional)` | `string`        | `Part or fulll name of the recipe.Recipe object`                      | 
    | `page`    |`query (optional)` | `int`           | `Page number if there a mutilple pages result`                        | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.Recipe obj list]}`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`     |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'http://host:port/api/recipe/home/?name=name&page=1' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```

#### Get favorite recipes

??? pied-piper-get "GET /api/recipe/home/favorites/"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.Recipe obj list]}` |
    | `404`         | `application/json`                | `{"detail":"No Recipe matches the given query."}`                                  |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'http://host:port/api/recipe/home/favorites/' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```



#### Get trending recipes

??? pied-piper-get "GET /api/recipe/trending"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Recipe objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'localhost:8080/api/recipe/trending' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```


#### Update favorite status

??? pied-piper-patch "PATCH /api/recipe/int:pk/favorite"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be favorited or unfavorited`                   | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`        | `"Success favorite recipe"`                                |
    | `201`         | `application/json`        | `"Success unfavorite recipe"`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}     |
    | `404`         | `application/json`                | `Not Found`          |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/recipe/1/favorite' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```


#### Create recipe

??? pied-piper "POST /api/recipe/"

    ##### Payload
    ``` json title="recipe.Recipe object"
    {
        "image": file,
        "name": string,
        "serves": int,
        "video": file (optional),
        "category": <int:pk>,
        "tag": <int:pk>,
        "prep_time": int,
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`multipart/form-data`|  `Recipe object`  | `Recipe multipart/form-data object`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{recipe.Recipe object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'localhost:8080/api/recipe/'  --header 'Authorization: Token d8916a5f6cf16d2c6a87bc7461bc4680245609f0' --form 'image=@"/path/image.jpg"' --form 'name="Test recipe creation"' --form 'serves="5"' --form 'category="1"' --form 'tag=1' --form 'prep_time="45"'
    > ```


#### Update recipe main info (without ingredients and steps)

??? pied-piper-put "PUT /api/recipe/int:pk"

    ##### Payload
    ``` json title="recipe.Recipe object"
    {
        "image": file,
        "name": string,
        "serves": int,
        "video": file (optional),
        "category": <int:pk>,
        "tag": <int:pk>,
        "prep_time": int,
    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be updated`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`multipart/form-data`|  `Recipe object`  | `Recipe multipart/form-data object`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Recipe object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/recipe/1' --header 'Authorization: Token d8916a5f6cf16d2c6a87bc7461bc4680245609f0' --form 'image=@"/path/image.jpg"' --form 'name="Update name"' --form 'serves="4"' --form 'category="1"' --form 'tag="1"' --form 'prep_time="21"'
    > ```


#### Delete recipes

??? pied-piper-delete "DELETE /api/recipe/pk:int/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be deleted`                   | 


    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `204`         | `application/json`                |                                                                     |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/recipe/<int:pk>/' --header 'Authorization: Token d8916a5f6cf16d2c6a87bc7461bc4680245609f0' 
    > ```

------------------------------------------------------------------------------------------

# Category

#### Get all categories

??? pied-piper-get "GET /api/recipe/trending"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Category objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/category' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```


#### Get all categories recipes 

??? pied-piper-get "GET /api/recipe/category/int:pk/recipes"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Category primary key`                   | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Recipe objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/category/1/recipes' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Create category

??? pied-piper "POST /api/recipe/category/add"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "name": string
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{recipe.Category object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/category/add' --header 'Authorization: token 443c104be8c6daeeaf86df634e69b97668b99900' --data '{"name":"Greek"}'
    > ```

#### Update category

??? pied-piper-put "PUT /api/recipe/category/int:pk"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "name": string,

    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Category primary key`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Recipe object}`|
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |
    | `404`         | `application/json`                | `{"detail":"No Category matches the given query."}`                       |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/recipe/category/6' --header 'Authorization: token 443c104be8c6daeeaf86df634e69b97668b99900'  --header 'Content-Type: application/json'  --data '{"name":"Italiano"}'
    > ```

------------------------------------------------------------------------------------------

# Tag

#### Get all tags 

??? pied-piper-get "GET /api/recipe/tags"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Tag objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/tags' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Get all recipes from tag 

??? pied-piper-get "GET /api/recipe/tag/int:pk/recipes"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Tag primary key`                   | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.Recipe obj list]}`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/tag/<int:pk>/recipes' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Create tag

??? pied-piper "POST /api/recipe/tag/add"

    ##### Payload
    ``` json title="recipe.Tag object"
    {
        "name": string
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{recipe.Category object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/tag/add' --header 'Authorization: token 443c104be8c6daeeaf86df634e69b97668b99900' --data '{"name":"Summer vibes"}'
    > ```

#### Update tag

??? pied-piper-put "PUT /api/recipe/tag/int:pk"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "name": string,

    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Tag primary key`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Tag object}`|
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |
    | `404`         | `application/json`                | `{"detail":"No Category matches the given query."}`                       |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/recipe/tag/1' --header 'Authorization: token 443c104be8c6daeeaf86df634e69b97668b99900'  --header 'Content-Type: application/json'  --data '{"name":"Summer Vibes"}'
    > ```


------------------------------------------------------------------------------------------

# Ingredients

??? pied-piper "POST /api/recipe/int:pk/ingredients"

    ???+ Info 
        
        Override already existing ingredients for the recipe

    ##### Payload
    ``` json title="recipe.Igredient object list"
    [
        {
            "name": "string,
            "quantity": string,
            "metric": "string
        },
        {
            "name": "string,
            "quantity": string,
            "metric": "string
        },
    ....
    ]
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to which to link the ingredients`                   | 
    
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `[{recipe.Ingrediant object}]`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/ingredients' --header 'Authorization: token 443c104be8c6daeeaf86df634e69b97668b99900' --data '[{"name":"Kasher salt","quantity":"1/5","metric":"tbsp","recipe":24}]'
    > ```

------------------------------------------------------------------------------------------

# Steps

??? pied-piper "POST /api/recipe/int:pk/steps"

    ???+ Info 
        
        Override already existing steps for the recipe

    ##### Payload
    ``` json title="recipe.Step object list"
    [
        {
            "text": string
        },
        {
            "text": string
        },
    ....
    ]
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to which to link the steps`                   | 
    
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint example "token 443c104be8c6daeeaf86df634e69b97668b99900"`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `[{recipe.Step object}]`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/ingredients' --header 'Authorization: token 443c104be8c6daeeaf86df634e69b97668b99900' --data '[{"text":"Heat the oven","recipe":1}]'
    > ```
